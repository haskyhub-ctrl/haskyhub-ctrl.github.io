"""Tra cứu kho tài liệu nội bộ (thư mục data_docs) không cần khóa nhúng (embedding).

Chatbot trả lời pháp luật theo kiểu RAG: tìm các đoạn tài liệu liên quan trong kho rồi đưa cho AI viết câu trả lời.
Trước đây bước tìm dùng vector ChromaDB và phải có khóa Gemini để nhúng câu hỏi. Module này thay bằng xếp hạng BM25
thuần Python trên chính các tài liệu trong data_docs (txt, docx, pdf), chạy cục bộ, không gọi dịch vụ ngoài.

Chỉ mục được lưu ở data/local_rag_index.pkl (không nằm trong git) và tự dựng lại khi tài liệu thay đổi.
"""
import math
import os
import pickle
import re
import threading
from collections import Counter

_BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(_BACKEND, "data_docs")
CACHE_PATH = os.path.join(_BACKEND, "data", "local_rag_index.pkl")
_EXTS = (".txt", ".docx", ".pdf")
CHUNK_CHARS = 900
K1, B = 1.5, 0.75

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


def _read(path: str) -> str:
    try:
        if path.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        if path.endswith(".docx"):
            import docx2txt
            return docx2txt.process(path) or ""
        if path.endswith(".pdf"):
            from pypdf import PdfReader
            return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    except Exception as e:
        print(f"[local_rag] Không đọc được {os.path.basename(path)}: {e}")
    return ""


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


def _signature() -> tuple:
    sig = []
    if os.path.isdir(DOCS_DIR):
        for fn in sorted(os.listdir(DOCS_DIR)):
            if fn.lower().endswith(_EXTS) and not fn.startswith(("~$", ".")):
                p = os.path.join(DOCS_DIR, fn)
                sig.append((fn, os.path.getsize(p), int(os.path.getmtime(p))))
    return tuple(sig)


def _build(sig: tuple) -> dict:
    docs = []
    for fn, _size, _mt in sig:
        text = _read(os.path.join(DOCS_DIR, fn))
        for c in _chunks(text):
            docs.append((fn, c))
    tfs = [Counter(_tokens(c)) for _, c in docs]
    df = Counter()
    for tf in tfs:
        df.update(tf.keys())
    lens = [sum(tf.values()) for tf in tfs]
    return {"sig": sig, "docs": docs, "tfs": tfs, "df": dict(df), "lens": lens,
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
            if cached.get("sig") == sig:
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


def search(question: str, k: int = 4) -> list:
    """Trả về tối đa k đoạn liên quan nhất: [(tên file, nội dung, điểm)]."""
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
        out.append((src, text, round(s, 2)))
    return out


def search_context(question: str, k: int = 4) -> str:
    """Chuỗi ngữ cảnh đưa cho AI; rỗng nếu không tìm thấy gì liên quan."""
    try:
        hits = search(question, k)
    except Exception as e:
        print(f"[local_rag] Lỗi tra cứu: {e}")
        return ""
    return "\n\n".join(f"[Tài liệu nội bộ: {src}]:\n{text}" for src, text, _ in hits)
