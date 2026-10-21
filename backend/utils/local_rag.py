"""Tra cứu kho tài liệu nội bộ không cần khóa nhúng (embedding).

Chatbot trả lời pháp luật theo kiểu RAG: tìm các đoạn tài liệu liên quan trong kho rồi đưa cho AI viết câu trả lời.
Module này xếp hạng BM25 thuần Python trên các tài liệu (txt, docx, pdf), chạy cục bộ, không gọi dịch vụ ngoài.

Hai nguồn tài liệu:
  1. Thư mục data_docs (nằm trong git): mặc định coi là tầng 2 (tài liệu hướng dẫn).
  2. Kho tải lên từ trang quản trị (data/kho_tai_lieu, không nằm trong git, không bị ghi đè khi cập nhật code).
     Mỗi tài liệu có tầng và trạng thái trong manifest.json:
       tầng 1 = văn bản quy phạm pháp luật hiện hành (ưu tiên cao nhất),
       tầng 2 = tài liệu hướng dẫn, tập huấn, nghiệp vụ,
       tầng 3 = tài liệu tham khảo (ưu tiên thấp nhất).
     Tài liệu ở trạng thái "inactive" (hết hiệu lực, bị thay thế, đang chờ duyệt) không được dùng để trả lời.

Chỉ mục được lưu ở data/local_rag_index.pkl và tự dựng lại khi tài liệu hoặc manifest thay đổi.
"""
import json
import math
import os
import pickle
import re
import threading
from collections import Counter

_BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(_BACKEND, "data_docs")
KHO_DIR = os.path.join(_BACKEND, "data", "kho_tai_lieu")
MANIFEST_PATH = os.path.join(KHO_DIR, "manifest.json")
CACHE_PATH = os.path.join(_BACKEND, "data", "local_rag_index.pkl")
_EXTS = (".txt", ".docx", ".pdf")
CHUNK_CHARS = 900
K1, B = 1.5, 0.75
TIER_WEIGHT = {1: 1.25, 2: 1.0, 3: 0.85}
TIER_LABEL = {1: "Văn bản pháp luật", 2: "Tài liệu hướng dẫn", 3: "Tài liệu tham khảo"}
DEFAULT_TIER = 2

_lock = threading.Lock()
_index = None

_STOP = {"và", "của", "các", "là", "có", "cho", "được", "trong", "khi", "một", "những", "này", "đó", "để", "với", "theo",
         "thì", "hay", "hoặc", "như", "không", "bị", "từ", "đến", "tại", "về", "nào", "gì", "sao", "bao", "nhiêu",
         "phải", "cần", "tôi", "bạn", "xin", "hỏi", "thế", "ra", "vào", "ở", "đã", "sẽ", "đang", "nên", "cũng"}
_TOKEN_RE = re.compile(r"\d+(?:[/.]\d+)*|[^\W\d_]+", re.UNICODE)


def _tokens(text: str) -> list:
    out = []
    for t in _TOKEN_RE.findall((text or "").lower()):
        if len(t) > 1 and t not in _STOP:
            out.append(t)
    return out


def read_text(path: str) -> str:
    """Đọc chữ từ tệp txt, docx, pdf. Trả chuỗi rỗng nếu không đọc được (ví dụ PDF bản quét)."""
    try:
        low = path.lower()
        if low.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        if low.endswith(".docx"):
            import docx2txt
            return docx2txt.process(path) or ""
        if low.endswith(".pdf"):
            from pypdf import PdfReader
            return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    except Exception as e:
        print(f"[local_rag] Không đọc được {os.path.basename(path)}: {e}")
    return ""


_read = read_text   # tên cũ


def _chunks(text: str) -> list:
    """Gộp các đoạn văn thành khối khoảng CHUNK_CHARS ký tự, giữ ranh giới đoạn."""
    paras = [p.strip() for p in re.split(r"\n\s*\n|\r\n\s*\r\n", text) if p.strip()]
    out, cur = [], ""
    for p in paras:
        while len(p) > CHUNK_CHARS * 1.6:          # đoạn quá dài: cắt theo câu hoặc độ dài
            cut = p.rfind(". ", 0, CHUNK_CHARS)
            cut = cut + 1 if cut > 200 else CHUNK_CHARS
            if cur:
                out.append(cur); cur = ""
            out.append(p[:cut].strip())
            p = p[cut:].strip()
        if len(cur) + len(p) + 1 > CHUNK_CHARS and cur:
            out.append(cur); cur = p
        else:
            cur = (cur + "\n" + p) if cur else p
    if cur:
        out.append(cur)
    return [c for c in out if len(c) > 40]


# ------------------------------------------------------------------ manifest của kho tải lên
def load_manifest() -> dict:
    """{tên tệp lưu: {title, tier, status, effective_date, note, original_name, uploaded_at, chars, chunks}}"""
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_manifest(data: dict) -> None:
    os.makedirs(KHO_DIR, exist_ok=True)
    tmp = MANIFEST_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MANIFEST_PATH)


def count_chunks(text: str) -> int:
    return len(_chunks(text))


def _sources() -> list:
    """Danh sách nguồn đang được dùng: (đường dẫn, kích thước, thời gian sửa, tầng, nhãn hiển thị)."""
    out = []
    if os.path.isdir(DOCS_DIR):
        for fn in sorted(os.listdir(DOCS_DIR)):
            if fn.lower().endswith(_EXTS) and not fn.startswith(("~$", ".")):
                p = os.path.join(DOCS_DIR, fn)
                out.append((p, os.path.getsize(p), int(os.path.getmtime(p)), DEFAULT_TIER, fn))
    for fn, meta in sorted(load_manifest().items()):
        p = os.path.join(KHO_DIR, fn)
        if meta.get("status") != "active" or not os.path.isfile(p):
            continue
        tier = meta.get("tier") if meta.get("tier") in TIER_WEIGHT else DEFAULT_TIER
        label = meta.get("title") or meta.get("original_name") or fn
        if meta.get("effective_date"):
            label += f", hiệu lực từ {meta['effective_date']}"
        out.append((p, os.path.getsize(p), int(os.path.getmtime(p)), tier, label))
    return out


def _signature() -> tuple:
    return tuple(_sources())


def _build(sig: tuple) -> dict:
    docs, tiers = [], []
    for path, _size, _mt, tier, label in sig:
        text = read_text(path)
        for c in _chunks(text):
            docs.append((label, c))
            tiers.append(tier)
    tfs = [Counter(_tokens(c)) for _, c in docs]
    df = Counter()
    for tf in tfs:
        df.update(tf.keys())
    lens = [sum(tf.values()) for tf in tfs]
    return {"sig": sig, "docs": docs, "tiers": tiers, "tfs": tfs, "df": dict(df), "lens": lens,
            "avgdl": (sum(lens) / len(lens)) if lens else 1.0}


def _get_index() -> dict:
    global _index
    sig = _signature()
    with _lock:
        if _index is not None and _index["sig"] == sig:
            return _index
        try:
            with open(CACHE_PATH, "rb") as f:
                cached = pickle.load(f)
            if cached.get("sig") == sig and "tiers" in cached:
                _index = cached
                return _index
        except Exception:
            pass
        _index = _build(sig)
        try:
            os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
            with open(CACHE_PATH, "wb") as f:
                pickle.dump(_index, f)
        except Exception as e:
            print(f"[local_rag] Không lưu được chỉ mục: {e}")
        return _index


def reindex() -> dict:
    """Dựng lại chỉ mục ngay (gọi sau khi tải lên hoặc đổi trạng thái tài liệu)."""
    global _index
    with _lock:
        _index = None
    idx = _get_index()
    return {"chunks": len(idx["docs"]), "documents": len(idx["sig"])}


def search(question: str, k: int = 4) -> list:
    """Trả về tối đa k đoạn liên quan nhất: [(nhãn tài liệu, nội dung, điểm, tầng)]."""
    idx = _get_index()
    if not idx["docs"]:
        return []
    q_tokens = [t for t in _tokens(question)]
    if not q_tokens:
        return []
    n = len(idx["docs"])
    q_terms = Counter(q_tokens)
    doc_numbers = set(re.findall(r"\d{2,4}/\d{4}|\d{2,3}\.\d{1,2}", question))   # số hiệu văn bản: 105/2025, 66.18...

    scores = []
    for i, tf in enumerate(idx["tfs"]):
        s = 0.0
        dl = idx["lens"][i] or 1
        for term, qf in q_terms.items():
            f = tf.get(term)
            if not f:
                continue
            df = idx["df"].get(term, 1)
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            s += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * dl / idx["avgdl"])) * (1 + 0.15 * (qf - 1))
        if s > 0 and doc_numbers:
            text_l = idx["docs"][i][1].lower()
            s += 1.5 * sum(1 for d in doc_numbers if d in text_l)
        if s > 0:
            s *= TIER_WEIGHT.get(idx["tiers"][i], 1.0)      # văn bản pháp luật hiện hành được ưu tiên hơn tài liệu tham khảo
            scores.append((s, i))
    scores.sort(reverse=True)
    if not scores:
        return []
    top = scores[0][0]
    out, seen = [], set()
    for s, i in scores:
        if s < top * 0.35 or len(out) >= k:   # bỏ các đoạn quá yếu so với đoạn tốt nhất
            break
        src, text = idx["docs"][i]
        key = text[:80]
        if key in seen:
            continue
        seen.add(key)
        out.append((src, text, round(s, 2), idx["tiers"][i]))
    return out


def search_context(question: str, k: int = 4) -> str:
    """Chuỗi ngữ cảnh đưa cho AI; rỗng nếu không tìm thấy gì liên quan."""
    try:
        hits = search(question, k)
    except Exception as e:
        print(f"[local_rag] Lỗi tra cứu: {e}")
        return ""
    return "\n\n".join(f"[{TIER_LABEL.get(tier, 'Tài liệu nội bộ')}: {src}]:\n{text}" for src, text, _, tier in hits)
