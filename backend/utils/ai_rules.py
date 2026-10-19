"""Bộ quy tắc cho phân tích AI của FRAS (một nguồn duy nhất).

Dùng ở ba nơi:
1. build_analysis_prompt (ai_prompt.py): đưa nguyên văn các quy tắc vào lời nhắc gửi AI.
2. sanitize_analysis: lưới an toàn sau khi AI trả lời, thay các từ ngữ gây cảm giác bị kiểm tra, xử phạt.
3. analysis_library.py: kho tri thức dự phòng dùng cùng giọng văn khi AI không hoạt động.

Tinh thần: hệ thống là công cụ tự kiểm tra, hướng dẫn, đồng hành với người dân và cơ sở; không phải
biên bản kiểm tra, không phải thẩm định pháp lý. Kết quả đọc lên phải khiến người trả lời yên tâm
trung thực lần sau.
"""
import re

# Nhãn mức nguy cơ do HỆ THỐNG tính. AI phải dùng đúng nhãn này, không tự nâng hoặc hạ.
LEVEL_LABELS = {
    "low": "thấp",
    "safe": "thấp",
    "medium": "trung bình",
    "high": "cao",
    "critical": "rất cao",
}

# Mức độ lời văn cho phép theo từng mức nguy cơ
LEVEL_TONE = {
    "low": "ghi nhận tích cực, nhắc duy trì và kiểm tra định kỳ",
    "safe": "ghi nhận tích cực, nhắc duy trì và kiểm tra định kỳ",
    "medium": "nhẹ nhàng, nêu một số điểm nên cải thiện",
    "high": "nghiêm túc nhưng ôn hòa, nêu rõ việc cần làm sớm",
    "critical": "nghiêm túc, nhấn mạnh việc cần làm ngay nhưng vẫn mang tính hướng dẫn",
}

# Nhãn thời hạn chuẩn, tránh mỗi nơi một kiểu
DEADLINE_LABELS = [
    "Làm ngay (trong 24-48 giờ)",
    "Trong 7 ngày",
    "Trong 15 ngày",
    "Trong 30 ngày",
    "Trong 60 ngày",
    "Trong 90 ngày",
]

ANALYSIS_RULES = [
    # --- Căn cứ dữ liệu ---
    "CHỈ DỰA VÀO DỮ LIỆU: chỉ nêu những gì thể hiện trong câu trả lời khảo sát. Không thêm thiết bị, hoạt động, "
    "sự cố hay nguyên nhân mà câu trả lời không nói tới (ví dụ không tự suy ra 'quá tải điện', 'tự chế', "
    "'không có đèn sự cố' khi câu trả lời chỉ nói đèn đã mờ).",
    "DÙNG ĐÚNG MỨC ĐỘ CỦA CÂU TRẢ LỜI: câu trả lời nói 'một phần', 'đôi khi', 'chưa đầy đủ' thì không viết thành 'hoàn toàn "
    "không có', 'thường xuyên', 'không bảo đảm'. Giữ nguyên sắc thái.",
    "ĐÚNG LOẠI HÌNH: gọi cơ sở đúng như loại hình ghi trong dữ liệu. Câu trả lời thuộc hoạt động mà loại hình thực tế "
    "có thể không có (ví dụ karaoke trong một tiệm tạp hóa) thì viết 'nếu có' hoặc bỏ qua, không đưa vào khuyến nghị riêng.",
    "NÓI RÕ LÀ THEO THÔNG TIN CƠ SỞ CUNG CẤP: kết quả chưa qua kiểm tra thực địa, không kết luận 'đạt chuẩn' hay 'không đạt'.",
    # --- Giọng điệu ---
    "GIỌNG HƯỚNG DẪN, ĐỒNG HÀNH: dùng 'tồn tại', 'điểm cần cải thiện', 'nên', 'khuyến nghị', 'cần ưu tiên'. "
    "Viết như người cán bộ PCCC đang chỉ dẫn tận tình cho chủ nhà.",
    "TUYỆT ĐỐI KHÔNG dùng các từ gây cảm giác bị kiểm tra, xử phạt: vi phạm, xử phạt, chế tài, bị phạt, đình chỉ, sai phạm, "
    "trái quy định, không tuân thủ, mức phạt. Không nêu số tiền phạt. Không viết 'để tránh bị ...'.",
    "KHÔNG PHÓNG ĐẠI: không dùng 'đặc biệt nghiêm trọng', 'cực kỳ nguy hiểm', 'báo động đỏ', 'tử huyệt', 'bất cứ lúc nào', "
    "'cản trở nghiêm trọng'. Mức độ lời văn phải khớp mức nguy cơ do hệ thống tính (thấp, trung bình, cao, rất cao); "
    "không tự nâng hoặc hạ mức đó.",
    "KHÔNG DÙNG 'tiêu chuẩn', 'đạt chuẩn', 'không đạt': thay bằng 'phù hợp', 'chưa phù hợp', 'cần bổ sung'. Tên tiêu chuẩn kỹ thuật "
    "chỉ xuất hiện ở trường legal_basis.",
    # --- Đầy đủ ---
    "KHÔNG BỎ SÓT: mọi câu trả lời mức nguy cơ rất cao (3 điểm) phải được nêu trong phần tồn tại và có khuyến nghị tương ứng "
    "(được phép gộp các câu cùng chủ đề). Sau đó mới tới các câu 2 điểm quan trọng nhất.",
    "ƯU ĐIỂM CÓ THẬT: chỉ lấy từ các câu trả lời an toàn (0 điểm), nêu đúng sự việc, không tâng bốc ('nghiêm túc', "
    "'tuân thủ tốt', 'đạt chuẩn'). Nếu chưa có ưu điểm đáng kể thì ghi nhận việc cơ sở chủ động tự khảo sát.",
    # --- Khuyến nghị ---
    "KHUYẾN NGHỊ CỤ THỂ, LÀM ĐƯỢC: nêu từng bước, vật tư phổ thông, người thực hiện. Không nêu giá tiền, tên hãng, nơi bán.",
    "SỐ LƯỢNG THIẾT BỊ PHẢI CÓ CĂN CỨ: chỉ nêu con số khi suy ra được từ diện tích, số tầng trong dữ liệu "
    "(gợi ý chung: mỗi tầng ít nhất 1 bình chữa cháy; mỗi 50 m2 sàn tối thiểu 1 bình bột 4 kg). Không tự đưa số lớn.",
    "THỨ TỰ ƯU TIÊN: nguy cơ trực tiếp gây cháy (điện, nguồn nhiệt, rò rỉ gas) làm ngay trong 24-48 giờ; bổ sung phương tiện, "
    "bảo dưỡng trong 7-30 ngày; thoát nạn và trang bị là điều kiện cứu người, không phải nguyên nhân gây cháy.",
    "THỜI HẠN CHỈ DÙNG CÁC NHÃN: " + "; ".join(DEADLINE_LABELS) + ".",
    "KHÔNG LẶP: kế hoạch 30/60/90 ngày là lộ trình tổng hợp, không chép lại nguyên văn từng khuyến nghị.",
    # --- Pháp lý ---
    "CĂN CỨ PHÁP LÝ LÀ THAM KHẢO: chỉ ghi ở trường legal_basis, chỉ dùng văn bản có trong danh mục cho sẵn, chỉ ghi số Điều/Khoản "
    "khi chắc chắn; không viện dẫn điều khoản xử phạt, không nêu mức phạt, không đưa căn cứ pháp lý vào phần mô tả tồn tại.",
    # --- Hình thức ---
    "VĂN PHONG: tiếng Việt, câu rõ ràng, không dùng dấu gạch ngang dài, không dùng từ sáo rỗng ('trong bối cảnh', "
    "'không thể phủ nhận', 'giải pháp toàn diện', 'tối ưu hóa'); không in đậm, không biểu tượng.",
    "ĐỊNH DẠNG: trả về đúng một khối JSON hợp lệ theo cấu trúc yêu cầu, không kèm chữ ngoài JSON.",
]


def rules_as_prompt() -> str:
    """Các quy tắc đánh số, để đưa vào lời nhắc gửi AI."""
    return "\n".join(f"{i}. {r}" for i, r in enumerate(ANALYSIS_RULES, 1))


# ---------------------------------------------------------------------------------
# Lưới an toàn sau khi AI trả lời
# ---------------------------------------------------------------------------------
# Thứ tự quan trọng: cụm dài trước, cụm ngắn sau.
_REPLACEMENTS = [
    (r"(?i)tồn tại vi phạm", "Tồn tại"),
    (r"(?i)hành vi vi phạm", "tình trạng chưa phù hợp"),
    (r"(?i)vi phạm nghiêm trọng", "chưa bảo đảm yêu cầu an toàn"),
    (r"(?i),?\s*(để\s+)?tránh\s+(bị\s+)?(xử phạt|bị phạt|đình chỉ)[^.;\n]*", ""),
    (r"(?i)xử phạt vi phạm hành chính", "hướng dẫn khắc phục"),
    (r"(?i)đình chỉ hoạt động", "tạm dừng hoạt động để khắc phục"),
    (r"(?i)đình chỉ", "tạm dừng"),
    (r"(?i)mức phạt[^.;\n]*", ""),
    (r"(?i)chế tài", "biện pháp"),
    (r"(?i)xử phạt", "xử lý"),
    (r"(?i)sai phạm", "tồn tại"),
    (r"(?i)vi phạm", "chưa phù hợp"),
    (r"(?i)đặc biệt nghiêm trọng", "cần ưu tiên xử lý"),
    (r"(?i)(không|chưa)\s+(bảo đảm|đảm bảo)\s+tiêu chuẩn", "chưa phù hợp"),
    (r"(?i)(bảo đảm|đảm bảo|đúng|đủ)\s+tiêu chuẩn", "phù hợp"),
    (r"(?i)(không|chưa)\s+đạt chuẩn", "chưa phù hợp"),
    (r"(?i)đạt chuẩn", "phù hợp"),
    (r"(?i)cản trở nghiêm trọng", "cản trở"),
    (r"(?i),?\s*bất cứ lúc nào", ""),
    (r"(?i)nghiêm trọng", "đáng chú ý"),
    (r"(?i)cực kỳ nguy hiểm", "cần ưu tiên xử lý"),
    (r"—|–", ","),
]
_COMPILED = [(re.compile(p), r) for p, r in _REPLACEMENTS]

# Trường chứa tên văn bản pháp luật: giữ nguyên, không thay chữ
_KEEP_FIELDS = {"legal_basis", "legal_references", "legal_reference"}


def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    for pat, repl in _COMPILED:
        text = pat.sub(repl, text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    return text.strip()


def sanitize_analysis(obj, _key=None):
    """Làm sạch đệ quy mọi chuỗi trong kết quả phân tích (trừ trường tên văn bản pháp luật)."""
    if _key in _KEEP_FIELDS:
        return obj
    if isinstance(obj, str):
        return sanitize_text(obj)
    if isinstance(obj, list):
        return [sanitize_analysis(x, _key) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize_analysis(v, k) for k, v in obj.items()}
    return obj
