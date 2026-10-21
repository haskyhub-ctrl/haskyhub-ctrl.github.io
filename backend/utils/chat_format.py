"""Chuẩn hóa câu trả lời của Trợ lý Chi trước khi gửi cho người dùng.

Cách trình bày (bộ hiển thị ở frontend/js/chatbot.js đọc các ký hiệu này):
  >> kết luận        ## tiêu đề mục        !! lưu ý        1. bước        - ý        **nhấn mạnh**        {{căn cứ pháp lý}}        bảng | a | b |
"""
import re


def normalize_persona(text: str) -> str:
    """Trợ lý xưng là Chi, gọi người dùng là bạn."""
    t = text
    t = re.sub(r"(?<![\w])[Aa]nh\s*/\s*chị(?![\w])", "bạn", t)
    t = re.sub(r"(?<![\w])[Qq]uý khách(?![\w])", "bạn", t)
    t = re.sub(r"(?<![\w])Tôi(?![\w])", "Chi", t)
    t = re.sub(r"(?<![\w])tôi(?![\w])", "Chi", t)
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
    t = normalize_persona(t)
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()
