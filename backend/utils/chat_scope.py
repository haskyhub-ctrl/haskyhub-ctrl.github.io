"""Giới hạn phạm vi của Trợ lý ảo Chi: chỉ trả lời các câu hỏi thuộc lĩnh vực PCCC và CNCH.

Câu hỏi ngoài lĩnh vực được từ chối khéo, không gọi AI (nhanh hơn và không tốn lượt gọi).
Để tránh từ chối nhầm, các trường hợp sau luôn được cho qua: lời chào, lời cảm ơn, câu hỏi về cách dùng hệ thống,
và câu hỏi nối tiếp ngắn khi cuộc trò chuyện trước đó đang nói về PCCC.
"""
import re
import unicodedata

OUT_OF_SCOPE_REPLY = (
    ">> Xin lỗi bạn, câu hỏi này nằm ngoài lĩnh vực mà Chi phụ trách." + chr(10) * 2 +
    "Chi chỉ hỗ trợ các nội dung về phòng cháy, chữa cháy và cứu nạn, cứu hộ: quy định và thủ tục, "
    "an toàn điện, lối thoát nạn, bình chữa cháy, cách xử lý khi có cháy, và cách dùng Hệ thống FRAS-AI. "
    "Bạn có thể hỏi Chi về những nội dung này nhé."
)

OUT_OF_SCOPE_SUGGESTIONS = [
    "Cơ sở của tôi cần trang bị gì về PCCC?",
    "Khi xảy ra cháy tôi phải làm gì?",
    "Cách làm khảo sát an toàn PCCC trên hệ thống?",
]


def _norm(text: str) -> str:
    t = unicodedata.normalize("NFD", (text or "").lower().replace("đ", "d"))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", t).strip()


# Từ "cháy" kiểm tra trên văn bản gốc có dấu, vì khi bỏ dấu "chạy" và "cháy" trùng nhau
_CHAY_RAW = re.compile(r"(?<![a-zà-ỹ])(cháy|cứu hỏa|cứu hộ|cứu nạn)(?![a-zà-ỹ])")

# Từ khóa (đã bỏ dấu) thuộc lĩnh vực PCCC, CNCH, an toàn cháy nổ và việc dùng hệ thống
_TOPIC = re.compile(
    r"(pccc|phong chay|chua chay|cnch|hoa hoan|"
    r"khoi (bay|doc|lua|day|thuoc)|ngat khoi|hit phai khoi|mui khet|"
    r"binh chua|binh bot|binh co2|binh gas|\bgas\b|\blpg\b|xang dau|chat long de|de chay|vat lieu chay|"
    r"bao chay|bao khoi|dau bao|chuong bao|\b114\b|truc nuoc|hong nuoc|voi nuoc|sprinkler|phun nuoc|"
    r"loi thoat|thoat nan|thoat hiem|den exit|den su co|bang chi dan thoat|"
    r"\b(an toan|he thong|day|thiet bi|chap|cap|tai|qua|ro) dien\b|dien (ap|nang|3 pha|ho gia dinh)|dong dien|bang dien|tu dien|"
    r"o cam|aptomat|rccb|cau dao|chap (dien|mach)|qua tai|nguon lua|nguon nhiet|han xi|"
    r"tham duyet|nghiem thu|kiem tra an toan|hau kiem|phuong an chua|dien tap|huan luyen (pccc|chua chay|nghiep vu)|"
    r"co so thuoc dien|dien quan ly|nguy co (chay|cao|thap|trung binh)|muc nguy co|rui ro chay|"
    r"luat 55|55/2024|nghi dinh 105|nghi dinh 347|quy chuan|qcvn|tcvn|347/2026|66\.18|105/2025|"
    r"doi chua chay|thu tuc (hanh chinh )?(pccc|chua chay)|"
    r"(nghi dinh|thong tu|nghi quyet|luat|quyet dinh) (so )?\d{1,3}([/.]\d+)+|\d{1,3}/(20\d{2}|\d{2})/(nd|tt|nq|qh)|co so du lieu|csdl|phan mem khai bao|phieu co so|truyen tin bao chay|thiet bi truyen tin|thuthapdulieu|khai bao (du lieu|thong tin)|cap nhat (du lieu|thong tin|co so)|tai khoan|dang nhap|dang ky tai khoan|quen mat khau|doi mat khau|tam dinh chi|dinh chi hoat dong|phuc hoi hoat dong|giay chung nhan|co so du lieu pccc|khai bao (co so|thong tin)|dieu kien an toan|phuong tien (pccc|chua chay)|"
    r"khao sat|danh gia (nguy co|an toan|co so)|ket qua (khao sat|danh gia)|"
    r"ma co so|ma theo doi|quen mat khau|dang nhap (fras|he thong|co so)|tai khoan (fras|co so)|"
    r"khac phuc (ton tai|nguy co)|ton tai (nguy co|an toan)|fras|tro ly chi|"
    r"nha ong|tuan hoan|so cuu|ky nang (thoat|song con)|bao hiem chay)"
)

# Địa điểm, loại hình chỉ tính là PCCC khi đi kèm yêu cầu, điều kiện, an toàn
_PLACE = re.compile(
    r"(nha tro|nha xuong|nha may|kho hang|kho bai|cua hang|khach san|nha hang|truong hoc|benh vien|chung cu|nha cao tang|nha o|cong trinh|co so san xuat|co so kinh doanh|tram xang)"
)
_NEED = re.compile(r"(can |phai |quy dinh|dieu kien|trang bi|giay phep|thu tuc|ho so|an toan|kiem tra|huong dan|bat buoc)")

_GREETING = re.compile(
    r"^(xin chao|chao|hello|hi|alo|cam on|tks|thanks|thank you|ok|oke|vang|da|duoc roi|tam biet|bye|"
    r"ban la ai|chi la ai|ban giup duoc gi|giup gi|ban lam duoc gi|huong dan|giup toi|toi can giup)\b"
)


def _on_topic(raw: str, msg: str) -> bool:
    return bool(_CHAY_RAW.search(raw) or _TOPIC.search(msg) or (_PLACE.search(msg) and _NEED.search(msg)))


def is_in_scope(message: str, history=None) -> bool:
    """Trả True nếu nên cho Chi trả lời (thuộc lĩnh vực hoặc không thể khẳng định là ngoài lĩnh vực)."""
    raw = (message or "").lower()
    msg = _norm(message)
    if not msg:
        return True
    if _GREETING.match(msg) or _on_topic(raw, msg):
        return True
    # Câu hỏi nối tiếp ngắn khi cuộc trò chuyện đang về PCCC
    if history and len(msg.split()) <= 12:
        past = " ".join(str(m.get("content", "")) for m in history[-6:] if isinstance(m, dict))
        if _on_topic(past.lower(), _norm(past)):
            return True
    return False


_CLASSIFY_PROMPT = """Phân loại câu hỏi của người dân. Câu hỏi có thuộc phạm vi hỗ trợ của Trợ lý PCCC Công an thành phố Bắc Ninh không?
Phạm vi gồm: phòng cháy, chữa cháy, cứu nạn cứu hộ, an toàn cháy nổ, quy định và thủ tục liên quan; việc sử dụng các hệ thống của lực lượng PCCC (Cơ sở dữ liệu về PCCC và CNCH, phần mềm khai báo, thiết bị truyền tin báo cháy, Hệ thống FRAS-AI, ứng dụng Báo cháy 114), kể cả lỗi tài khoản, đăng nhập, cập nhật dữ liệu trên các hệ thống đó; kiểm tra, huấn luyện, xử phạt vi phạm trong lĩnh vực PCCC.
Ngoài phạm vi: mọi chủ đề khác (giá cả, giải trí, y tế, giao thông, thời tiết, lập trình, tài chính...).

Câu hỏi: {question}
Trả về DUY NHẤT JSON: {{"in_scope": true hoặc false}}"""


def classify_with_ai(message: str):
    """Hỏi AI nhanh khi từ khóa không khớp. Trả True, False, hoặc None nếu AI không phản hồi (khi đó cho qua, để tránh từ chối nhầm)."""
    try:
        from utils.rag_search import _call_llm, _extract_json_block
        raw = _call_llm(_CLASSIFY_PROMPT.format(question=message[:600]), temperature=0.0, max_tokens=40, is_json=True, fast=True, timeout=10.0)
        data = _extract_json_block(raw) or {}
        v = data.get("in_scope")
        return bool(v) if isinstance(v, bool) else None
    except Exception:
        return None


def out_of_scope_response() -> dict:
    return {
        "reply": OUT_OF_SCOPE_REPLY,
        "suggestions": list(OUT_OF_SCOPE_SUGGESTIONS),
        "references": [],
        "source_type": "scope",
    }


DISCLAIMER = (
    "Thông tin trên chỉ mang tính tham khảo. Để được hướng dẫn cụ thể và đầy đủ hơn, "
    "bạn vui lòng liên hệ cán bộ Cảnh sát PCCC và CNCH."
)


DISCLAIMER_MARK = "~~ "      # ký hiệu để giao diện hiển thị câu chốt bằng chữ nhỏ, nghiêng, màu xám


def with_disclaimer(result: dict, message: str = "") -> dict:
    """Thêm câu chốt tham khảo vào cuối câu trả lời chuyên môn (bỏ qua lời chào, lời cảm ơn, câu từ chối ngoài lĩnh vực)."""
    if not isinstance(result, dict) or result.get("source_type") == "scope":
        return result
    reply = result.get("reply")
    if not isinstance(reply, str) or not reply.strip():
        return result
    if _GREETING.match(_norm(message)) and len(reply) < 400:
        return result
    if "mang tính tham khảo" in reply:
        return result
    result["reply"] = f"{reply.rstrip()}{chr(10) * 2}{DISCLAIMER_MARK}{DISCLAIMER}"
    return result
