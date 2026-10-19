"""Kho tri thức phân tích của FRAS.

Mục đích: khi dịch vụ AI không hoạt động, hệ thống vẫn trả được một bản phân tích đầy đủ, cùng giọng văn
và cùng cấu trúc với bản do AI viết (người dùng không thấy khác biệt về hình thức).

Kho gồm hai nguồn, gộp lại khi dùng (nguồn học được từ AI ghi đè nguồn dựng sẵn):
- data_docs/analysis_library_seed.json: bản dựng sẵn, đưa vào git, cập nhật bằng build_analysis_library.py
- data/analysis_library_learned.json: các phân tích AI thật vừa viết, tự ghi thêm khi chạy, không nằm trong git
  (nên không bị mất khi cập nhật code lên server)

Mỗi mục gắn với một cặp (câu hỏi, đáp án): tình trạng ghi nhận (issue) và khuyến nghị tương ứng.
Ngoài tra cứu chính xác và gần đúng theo từ, mục mới còn được lập chỉ mục vào ChromaDB (thư mục chroma_analysis)
nếu thư viện và khóa nhúng sẵn có; thiếu thì bỏ qua, kho vẫn chạy bằng tra cứu theo từ.
"""
import hashlib
import json
import os
import re
import threading
from datetime import datetime

from utils.ai_rules import (
    DEADLINE_LABELS, LEVEL_LABELS, LEVEL_TONE, sanitize_analysis, sanitize_text,
)

_BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_PATH = os.path.join(_BACKEND, "data_docs", "analysis_library_seed.json")
LEARNED_PATH = os.path.join(_BACKEND, "data", "analysis_library_learned.json")
CHROMA_DIR = os.path.join(_BACKEND, "chroma_analysis")
CHROMA_COLLECTION = "fras_analysis_library"

_lock = threading.Lock()
_cache = {"sig": None, "entries": {}, "tokens": {}}


# ----------------------------------------------------------------------------- tiện ích văn bản
def _norm(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


_STOP = {"có", "không", "và", "của", "cho", "các", "một", "được", "trong", "khi", "như", "thế", "nào", "hiện",
         "là", "ở", "tại", "với", "đã", "chưa", "những", "này", "đó", "hay", "hoặc", "mức", "bao", "nhiêu"}


def _tokens(text: str) -> set:
    return {w for w in _norm(text).split() if len(w) > 1 and w not in _STOP}


def _overlap(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def entry_key(question_text: str, option_text: str) -> str:
    return hashlib.sha1((_norm(question_text) + "|" + _norm(option_text)).encode("utf-8")).hexdigest()[:16]


def normalize_deadline(text, priority=None) -> str:
    """Đưa thời hạn về một trong các nhãn chuẩn (DEADLINE_LABELS)."""
    t = _norm(text or "")
    if not t:
        return {"urgent": DEADLINE_LABELS[0], "high": DEADLINE_LABELS[1], "medium": DEADLINE_LABELS[3]}.get(priority, DEADLINE_LABELS[3])
    if "ngay" in t.split() or "24" in t or "48" in t or "khẩn" in t:
        return DEADLINE_LABELS[0]
    m = re.search(r"(\d+)\s*(ngày|tuần|tháng)?", t)
    if m:
        n = int(m.group(1))
        unit = m.group(2) or "ngày"
        days = n * 7 if unit == "tuần" else n * 30 if unit == "tháng" else n
        if unit == "ngày" and n <= 2:
            return DEADLINE_LABELS[0]
        for label, limit in zip(DEADLINE_LABELS[1:], (7, 15, 30, 60, 90)):
            if days <= limit:
                return label
        return DEADLINE_LABELS[5]
    return DEADLINE_LABELS[3]


# ----------------------------------------------------------------------------- đọc, ghi kho
def _read_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def load_library() -> dict:
    """Gộp bản dựng sẵn và bản học được (bản học được ghi đè)."""
    sig = tuple(os.path.getmtime(p) if os.path.exists(p) else 0 for p in (SEED_PATH, LEARNED_PATH))
    with _lock:
        if _cache["sig"] == sig:
            return _cache["entries"]
        entries = {}
        entries.update(_read_json(SEED_PATH).get("entries", {}))
        entries.update(_read_json(LEARNED_PATH).get("entries", {}))
        _cache["entries"] = entries
        _cache["tokens"] = {k: _tokens(e.get("question", "") + " " + e.get("option_text", "")) for k, e in entries.items()}
        _cache["sig"] = sig
        return entries


def _write_learned(new_entries: dict):
    os.makedirs(os.path.dirname(LEARNED_PATH), exist_ok=True)
    with _lock:
        current = _read_json(LEARNED_PATH).get("entries", {})
        current.update(new_entries)
        tmp = LEARNED_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"updated": datetime.utcnow().isoformat(), "entries": current}, f, ensure_ascii=False, indent=1)
        os.replace(tmp, LEARNED_PATH)
        _cache["sig"] = None


def lookup(question_text: str, option_text: str, min_overlap: float = 0.6):
    """Tra cứu mục phân tích: chính xác theo khóa, rồi gần đúng theo từ, rồi ChromaDB (nếu có)."""
    entries = load_library()
    e = entries.get(entry_key(question_text, option_text))
    if e:
        return e
    qt = _tokens(question_text + " " + option_text)
    best, best_score = None, 0.0
    for k, toks in _cache["tokens"].items():
        s = _overlap(qt, toks)
        if s > best_score:
            best, best_score = k, s
    if best and best_score >= min_overlap:
        return entries[best]
    return _chroma_lookup(question_text + " " + option_text)


# ----------------------------------------------------------------------------- ChromaDB (cố gắng, không bắt buộc)
def _chroma_store():
    if not os.getenv("GEMINI_API_KEY"):
        return None
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        return Chroma(collection_name=CHROMA_COLLECTION, embedding_function=emb, persist_directory=CHROMA_DIR)
    except Exception:
        return None


def index_chroma(entries: dict) -> bool:
    """Lập chỉ mục các mục vào ChromaDB. Trả về False nếu môi trường chưa sẵn sàng."""
    store = _chroma_store()
    if store is None or not entries:
        return False
    try:
        keys = list(entries.keys())
        texts = [entries[k].get("question", "") + " => " + entries[k].get("option_text", "") for k in keys]
        store.add_texts(texts=texts, metadatas=[{"key": k} for k in keys], ids=keys)
        return True
    except Exception as e:
        print(f"[analysis_library] Không lập chỉ mục ChromaDB: {e}")
        return False


def _chroma_lookup(text: str, max_distance: float = 0.45):
    store = _chroma_store()
    if store is None:
        return None
    try:
        res = store.similarity_search_with_score(text, k=1)
        if res and res[0][1] <= max_distance:
            return load_library().get(res[0][0].metadata.get("key"))
    except Exception:
        pass
    return None


# ----------------------------------------------------------------------------- học từ phân tích AI
def _risky(assessment_data: dict):
    from utils.ai_prompt import numbered_risky_answers
    return numbered_risky_answers(assessment_data)


def learn_from_analysis(assessment_data: dict, analysis: dict) -> int:
    """Lưu các khuyến nghị AI vừa viết vào kho, gắn với câu trả lời mà khuyến nghị đó xử lý."""
    risky = _risky(assessment_data)
    new = {}
    for rec in analysis.get("detailed_recommendations", []) or []:
        if not (rec.get("title") and rec.get("description")):
            continue
        for idx in rec.get("answers") or []:
            if not isinstance(idx, int) or not (1 <= idx <= len(risky)):
                continue
            a = risky[idx - 1]
            key = entry_key(a.get("question_text", ""), a.get("answer_text", ""))
            new[key] = {
                "question": a.get("question_text", ""),
                "option_text": a.get("answer_text", ""),
                "score": a.get("score", 0),
                "category": a.get("category", ""),
                "issue": rec.get("issue") or "",
                "rec": {
                    "title": rec.get("title"),
                    "description": rec.get("description"),
                    "priority": rec.get("priority") or "high",
                    "deadline": normalize_deadline(rec.get("deadline"), rec.get("priority")),
                    "responsible_party": rec.get("responsible_party") or "",
                    "legal_basis": rec.get("legal_basis") or "",
                },
                "source": "ai",
                "updated": datetime.utcnow().isoformat(timespec="seconds"),
            }
    if new:
        new = sanitize_analysis(new)
        _write_learned(new)
        threading.Thread(target=index_chroma, args=(new,), daemon=True).start()
    return len(new)


# ----------------------------------------------------------------------------- đảm bảo đủ câu mức rất cao
def _entry_for_answer(a: dict) -> dict:
    """Mục phân tích cho một câu trả lời: kho tri thức, nếu chưa có thì dựng theo từ khóa."""
    e = lookup(a.get("question_text", ""), a.get("answer_text", ""))
    if e and e.get("rec"):
        return e
    from utils.ai_prompt import _answer_to_recommendation
    base = _answer_to_recommendation(a.get("question_text", ""), a.get("answer_text", ""), a.get("score", 2)) or {}
    return {
        "issue": f"{a.get('question_text', '').rstrip('?')}: {a.get('answer_text', '')}",
        "rec": {
            "title": base.get("title") or "Rà soát và khắc phục nội dung đã ghi nhận",
            "description": base.get("description") or f"Tình trạng ghi nhận: {a.get('answer_text', '')}. Nên rà soát trực tiếp và xử lý từng bước.",
            "priority": "urgent" if a.get("score", 0) >= 3 else "high",
            "deadline": base.get("deadline") or "",
            "responsible_party": "Chủ cơ sở",
            "legal_basis": base.get("legal_basis") or "",
        },
    }


def ensure_red_flag_coverage(assessment_data: dict, analysis: dict) -> dict:
    """Mọi câu mức rất cao (3 điểm) phải được nêu trong tồn tại và có khuyến nghị. Thiếu thì bổ sung từ kho tri thức."""
    risky = _risky(assessment_data)
    recs = analysis.setdefault("detailed_recommendations", [])
    weaknesses = analysis.setdefault("critical_weaknesses", [])
    covered_idx = {i for r in recs for i in (r.get("answers") or []) if isinstance(i, int)}
    rec_tokens = [_tokens((r.get("title") or "") + " " + (r.get("issue") or "") + " " + (r.get("description") or "")) for r in recs]
    weak_tokens = [_tokens(w) for w in weaknesses]
    added = 0
    for i, a in enumerate(risky, 1):
        if a.get("score", 0) < 3:
            continue
        if i in covered_idx:
            continue
        at = _tokens(a.get("question_text", "") + " " + a.get("answer_text", ""))
        if any(_overlap(at, t) >= 0.3 for t in rec_tokens) or any(_overlap(at, t) >= 0.3 for t in weak_tokens):
            continue
        e = _entry_for_answer(a)
        rec = dict(e["rec"])
        rec.update({"answers": [i], "issue": e.get("issue") or ""})
        recs.append(rec)
        if e.get("issue"):
            weaknesses.append(e["issue"])
        added += 1
    if added:
        analysis["coverage_added"] = added
    return analysis


# ----------------------------------------------------------------------------- dựng phân tích từ kho
_CHECKLIST_RULES = [
    (("điện", "ổ cắm", "aptomat", "dây"), "Quan sát bảng điện, ổ cắm, dây dẫn: xác nhận không nóng, không mùi khét, không tiếng kêu lạ."),
    (("gas", "bếp", "bình gas"), "Sau giờ đun nấu hoặc kinh doanh, khóa van bình gas và kiểm tra khu bếp."),
    (("thoát", "lối", "cầu thang", "cửa"), "Kiểm tra lối ra chính, lối phụ và cầu thang: thông thoáng, mở được từ bên trong."),
    (("bình chữa cháy", "chữa cháy"), "Xem đồng hồ bình chữa cháy còn vạch xanh, bình để ở nơi dễ thấy, dễ lấy."),
    (("sạc", "xe điện", "pin"), "Không để xe điện, pin sạc qua đêm khi không có người trông, rút sạc khi đã đầy."),
    (("hàng", "kho", "xếp"), "Kiểm tra hàng hóa không chất sát tủ điện, ổ cắm, nguồn nhiệt và không che lối đi."),
    (("khói", "báo cháy"), "Thử nút kiểm tra của cảm biến khói, chuông báo cháy (nếu có) mỗi tuần một lần."),
    (("máy", "motor", "tủ đông", "tủ mát"), "Nghe và sờ nhẹ các thiết bị chạy liên tục (motor, tủ đông, quạt): phát hiện nóng, rung, mùi khét."),
]
_DEFAULT_CHECKLIST = [
    "Trước khi đóng cửa: ngắt các thiết bị điện không cần thiết, kiểm tra nguồn lửa, nguồn nhiệt.",
    "Rà lối ra: không để đồ, xe, hàng hóa chắn lối đi và cửa thoát.",
    "Biết rõ vị trí bình chữa cháy và số gọi cứu hộ 114 để báo ngay khi cần.",
]

_PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}


def _cat_label(name: str) -> str:
    """Tên nhóm câu hỏi dùng trong văn xuôi: bỏ tiền tố 'Đặc thù:' và chữ in hoa toàn bộ."""
    name = (name or "").strip()
    if name.lower().startswith("đặc thù:"):
        return "nhóm đặc thù " + name.split(":", 1)[1].strip().lower().replace("tttm", "TTTM")
    return name


def _clean_issue(text: str) -> str:
    """Bỏ cụm mở đầu lặp lại 'Theo thông tin cơ sở cung cấp,' ở từng tồn tại (phần tổng quan đã nói một lần)."""
    t = re.sub(r"^\s*(theo thông tin (do )?cơ sở (cung cấp|tự khai báo)|theo (câu trả lời|thông tin) khảo sát)[,:]?\s*", "", text or "", flags=re.I)
    return (t[:1].upper() + t[1:]) if t else t


def _lc_first(s: str) -> str:
    s = (s or "").strip()
    return s[:1].lower() + s[1:] if s else s


def compose_analysis(assessment_data: dict) -> dict:
    """Soạn bản phân tích đầy đủ từ kho tri thức (cùng cấu trúc với bản AI)."""
    from utils.ai_prompt import CURRENT_LEGAL_REFERENCES, facility_type_text, split_answers

    level = assessment_data.get("risk_level", "medium")
    level_text = LEVEL_LABELS.get(level, "trung bình")
    pct = assessment_data.get("risk_percentage", 0)
    name = assessment_data.get("facility_name") or "Cơ sở"
    ftype = facility_type_text(assessment_data.get("facility_type"))
    cats = sorted(assessment_data.get("category_scores", []), key=lambda c: c.get("percentage", 0), reverse=True)
    top = [c for c in cats if c.get("percentage", 0) >= 25][:3]
    red, high, _mid, safe = split_answers(assessment_data)

    # --- tổng quan
    opening = {
        "critical": f"Theo thông tin cơ sở cung cấp, {name} ({ftype}) có tỷ lệ nguy cơ {pct}%, ở mức rất cao.",
        "high": f"Theo thông tin cơ sở cung cấp, {name} ({ftype}) có tỷ lệ nguy cơ {pct}%, ở mức cao.",
        "medium": f"Theo thông tin cơ sở cung cấp, {name} ({ftype}) có tỷ lệ nguy cơ {pct}%, ở mức trung bình.",
    }.get(level, f"Theo thông tin cơ sở cung cấp, {name} ({ftype}) có tỷ lệ nguy cơ {pct}%, ở mức {level_text}. Cơ sở đang làm khá tốt, nên duy trì và kiểm tra định kỳ.")
    focus = ""
    if top:
        focus = " Các nhóm nên chú ý trước là " + "; ".join(f"{_cat_label(c['category_name'])} ({c['percentage']}%)" for c in top) + "."
    counts = ""
    if red or high:
        counts = f" Có {len(red)} nội dung ở mức rất cao và {len(high)} nội dung ở mức cao, được sắp xếp theo thứ tự ưu tiên ở phần khuyến nghị."
    closing = " Kết quả dựa trên câu trả lời của cơ sở, chưa qua kiểm tra thực địa. Sau khi khắc phục, cơ sở có thể cập nhật tiến độ để hệ thống tính lại mức nguy cơ."
    overall = opening + focus + counts + closing

    # --- ưu điểm
    strengths = []
    for a in safe:
        txt = (a.get("answer_text") or "").strip()
        low = txt.lower()
        if not txt or low.startswith("không có") or "hoặc có" in low or "nếu có" in low or "không thuộc" in low:
            continue   # câu trả lời an toàn kiểu "không có thiết bị này" không phải ưu điểm đáng nêu
        strengths.append(f"Ghi nhận: {_lc_first(txt)}.".replace("..", "."))
        if len(strengths) >= 5:
            break
    if not strengths:
        strengths = ["Cơ sở đã chủ động tự khảo sát, đây là bước đầu tốt để nhận diện và giảm nguy cơ cháy nổ."]

    # --- tồn tại và khuyến nghị
    weaknesses, recs, seen_titles = [], [], set()
    risky = red + high
    for i, a in enumerate(risky, 1):
        e = _entry_for_answer(a)
        issue = _clean_issue(e.get("issue") or "")
        if issue and issue not in weaknesses:
            weaknesses.append(issue)
        rec = dict(e["rec"])
        title = rec.get("title") or ""
        if title in seen_titles:
            continue
        seen_titles.add(title)
        rec["answers"] = [i]
        rec["issue"] = issue
        rec["priority"] = rec.get("priority") or ("urgent" if a.get("score", 0) >= 3 else "high")
        rec["deadline"] = normalize_deadline(rec.get("deadline"), rec["priority"])
        recs.append(rec)
    recs.sort(key=lambda r: _PRIORITY_ORDER.get(r.get("priority"), 2))
    recs = recs[:12]
    weaknesses = weaknesses[:10]

    # --- danh mục tự kiểm tra
    blob = " ".join((r.get("title", "") + " " + r.get("issue", "")).lower() for r in recs)
    checklist = [text for kws, text in _CHECKLIST_RULES if any(k in blob for k in kws)][:6]
    for extra in _DEFAULT_CHECKLIST:
        if len(checklist) < 5:
            checklist.append(extra)

    # --- lộ trình
    def titles(rs, n=4):
        out = []
        for r in rs[:n]:
            t = (r.get("title") or "").rstrip(".")
            out.append(t[:1].lower() + t[1:])
        return "; ".join(out)

    urgent = [r for r in recs if r.get("priority") == "urgent"]
    high = [r for r in recs if r.get("priority") == "high"]
    medium = [r for r in recs if r.get("priority") not in ("urgent", "high")]
    p30 = []
    if urgent:
        p30.append({"task": "Xử lý trước các nguy cơ trực tiếp gây cháy",
                    "detail": f"Trong 24-48 giờ đầu: {titles(urgent)}. Việc điện, gas nên nhờ thợ có chuyên môn thực hiện.",
                    "responsible": "Chủ cơ sở, thợ điện có chuyên môn", "criteria": "Các hạng mục đã xử lý xong, tự kiểm tra lại không còn dấu hiệu bất thường", "legal_basis": ""})
    if high:
        p30.append({"task": "Giải tỏa lối ra và bổ sung phương tiện tại chỗ",
                    "detail": f"Hoàn thành trong 7-15 ngày: {titles(high)}.",
                    "responsible": "Chủ cơ sở", "criteria": "Lối ra thông thoáng, thiết bị đã bố trí ở nơi dễ thấy, dễ lấy", "legal_basis": ""})
    p60 = []
    if medium:
        p60.append({"task": "Bảo dưỡng và nâng cấp thiết bị", "detail": f"{titles(medium)}.",
                    "responsible": "Chủ cơ sở", "criteria": "Thiết bị hoạt động ổn định, kiểm tra định kỳ", "legal_basis": ""})
    p60.append({"task": "Phổ biến cho các thành viên cách xử lý khi có sự cố",
                "detail": "Hướng dẫn mọi người trong nhà, nơi làm việc cách gọi 114, dùng bình chữa cháy, ngắt điện và đi ra theo lối thoát. Nên nhờ lực lượng PCCC địa phương hỗ trợ hướng dẫn.",
                "responsible": "Chủ cơ sở", "criteria": "Mọi người đều biết các bước cơ bản", "legal_basis": ""})
    p90 = [
        {"task": "Lập sổ theo dõi và lịch kiểm tra định kỳ",
         "detail": "Ghi lại các hạng mục đã khắc phục, ngày kiểm tra điện, gas, bình chữa cháy; niêm yết sơ đồ lối ra tại nơi dễ thấy.",
         "responsible": "Chủ cơ sở", "criteria": "Có sổ và lịch kiểm tra hằng tháng", "legal_basis": ""},
        {"task": "Tự đánh giá lại bằng FRAS",
         "detail": "Làm lại khảo sát sau khi khắc phục để so sánh mức nguy cơ trước và sau, tiếp tục xử lý các nội dung còn lại.",
         "responsible": "Chủ cơ sở", "criteria": "Tỷ lệ nguy cơ giảm so với lần đầu", "legal_basis": ""},
    ]

    result = {
        "overall_assessment": overall,
        "strengths": strengths,
        "critical_weaknesses": weaknesses or ["Chưa ghi nhận nội dung nguy cơ cao. Cơ sở nên duy trì kiểm tra định kỳ."],
        "detailed_recommendations": recs,
        "daily_checklist": checklist,
        "improvement_plan": {"30_days": p30, "60_days": p60, "90_days": p90},
        "legal_references": CURRENT_LEGAL_REFERENCES,
        "risk_summary": f"Tỷ lệ nguy cơ {pct}%, mức {level_text}.",
        "source": "library",
    }
    return sanitize_analysis(result)
