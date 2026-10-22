"""Chuẩn hóa câu trả lời của Trợ lý Chi trước khi gửi cho người dùng.

Cách trình bày (bộ hiển thị ở frontend/js/chatbot.js đọc các ký hiệu này):
  >> kết luận        ## tiêu đề mục        !! lưu ý        1. bước        - ý        **nhấn mạnh**        {{căn cứ pháp lý}}        bảng | a | b |
"""
import re


def normalize_persona(text: str) -> str:
    """Trợ lý xưng là Tôi hoặc Trợ lý ảo, gọi người dùng là bạn. Tuyệt đối không xưng Chi."""
    t = text
    t = re.sub(r"(?<![\w])[Aa]nh\s*/\s*chị(?![\w])", "bạn", t)
    t = re.sub(r"(?<![\w])[Qq]uý khách(?![\w])", "bạn", t)
    # Loại bỏ triệt để việc tự xưng Chi
    t = re.sub(r"(?<![\w])Chi xin thông tin(?![\w])", "Tôi xin thông tin", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi xin(?![\w])", "Tôi xin", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi có thể(?![\w])", "Tôi có thể", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi chỉ hỗ trợ(?![\w])", "Tôi chỉ hỗ trợ", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi đang(?![\w])", "Tôi đang", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi khuyên(?![\w])", "Tôi khuyên", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi hướng dẫn(?![\w])", "Tôi hướng dẫn", t, flags=re.I)
    t = re.sub(r"(?<![\w])hỏi Chi(?![\w])", "hỏi tôi", t, flags=re.I)
    t = re.sub(r"(?<![\w])cho Chi biết(?![\w])", "cho tôi biết", t, flags=re.I)
    t = re.sub(r"(?<![\w])của Chi(?![\w])", "của Trợ lý ảo", t, flags=re.I)
    t = re.sub(r"(?<![\w])tài liệu của Chi(?![\w])", "tài liệu của hệ thống", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi chưa đủ căn cứ(?![\w])", "Hiện chưa đủ căn cứ", t, flags=re.I)
    t = re.sub(r"(?<![\w])Chi\s+(?=(?:sẽ|đã|rất|muốn|khẳng định|nhận thấy))", "Tôi ", t, flags=re.I)
    return t


def clean_reply(text: str) -> str:
    if not text:
        return ""
    t = text.replace("\r\n", "\n")
    # Tiêu đề markdown kiểu # ### chuyển thành "## "
    t = re.sub(r"^[ \t]*#{1,6}[ \t]*", "## ", t, flags=re.M)
    # Gạch đầu dòng dạng chấm tròn
    t = re.sub(r"^[ \t]*[•●▪]\s*", "- ", t, flags=re.M)
    # Đường kẻ ngang thừa (giữ dòng phân cách của bảng có dấu |)
    t = re.sub(r"^[ \t]*[-=_]{3,}[ \t]*$", "", t, flags=re.M)
    # Dấu gạch ngang dài
    t = re.sub(r"\s[—–]\s", ", ", t)
    t = t.replace("—", ", ").replace("–", "-")
    # Thẻ <br> trong ô bảng: thay bằng dấu chấm phẩy; ngoài bảng: xuống dòng
    t = re.sub(r"^(.*\|.*)$", lambda m: re.sub(r"\s*<br\s*/?>\s*[-•]?\s*", "; ", m.group(1)), t, flags=re.M)
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = normalize_persona(t)
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()
