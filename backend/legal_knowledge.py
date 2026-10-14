"""
Vietnamese Fire Safety Legal Knowledge Base
Provides structured legal context for AI chatbot responses.
"""

LEGAL_DOCUMENTS = """
=== CƠ SỞ PHÁP LÝ PCCC VIỆT NAM (2024-2025) ===

1. LUẬT PHÒNG CHÁY, CHỮA CHÁY VÀ CỨU NẠN, CỨU HỘ SỐ 55/2024/QH15
   (Có hiệu lực từ 01/07/2025, thay thế Luật PCCC 2001)

   Điều 5 – Trách nhiệm PCCC:
   - Mọi cơ quan, tổ chức, hộ gia đình, cá nhân đều có trách nhiệm PCCC
   - Người đứng đầu cơ sở chịu trách nhiệm chính về PCCC tại cơ sở

   Điều 13 – Điều kiện an toàn PCCC đối với cơ sở:
   - Có nội quy, biển cấm, biển báo, sơ đồ chỉ dẫn thoát nạn
   - Hệ thống điện, chống sét phải đảm bảo an toàn
   - Có lực lượng PCCC cơ sở
   - Có phương tiện PCCC phù hợp quy chuẩn
   - Có phương án chữa cháy được phê duyệt

   Điều 17 – Yêu cầu về phương tiện PCCC:
   - Phương tiện phải đảm bảo chất lượng, được kiểm định
   - Bố trí tại vị trí thuận tiện, dễ thấy, dễ lấy
   - Kiểm tra, bảo dưỡng định kỳ theo quy định

   Điều 24 – Huấn luyện PCCC:
   - 100% cán bộ, nhân viên phải được huấn luyện PCCC
   - Tổ chức diễn tập phương án chữa cháy ít nhất 1 lần/năm
   - Nội dung: sử dụng phương tiện, quy trình báo cháy (114), thoát nạn

   Điều 46 – Xử lý vi phạm:
   - Cơ sở vi phạm nghiêm trọng có thể bị đình chỉ hoạt động
   - Người đứng đầu có thể bị truy cứu trách nhiệm hình sự

2. NGHỊ ĐỊNH 105/2025/NĐ-CP (Hướng dẫn Luật PCCC 55/2024)

   Chương II – Điều kiện an toàn PCCC:
   - Cơ sở phải có hồ sơ quản lý PCCC
   - Kiểm tra an toàn PCCC định kỳ: hàng tháng (tự kiểm tra), hàng quý (lực lượng PCCC cơ sở)
   - Khoảng cách an toàn PCCC giữa các công trình

   Chương IV – Phương tiện PCCC:
   - Bình chữa cháy: tối thiểu 1 bình ABC 4kg/50m² sàn
   - Hệ thống báo cháy tự động: bắt buộc với nhà cao ≥5 tầng, diện tích ≥300m²
   - Hệ thống chữa cháy tự động: bắt buộc với nhà cao ≥10 tầng, tầng hầm ≥1 tầng

   Phụ lục V – Mức phạt vi phạm PCCC:
   - Không có nội quy PCCC: 2-5 triệu đồng
   - Không trang bị phương tiện PCCC: 15-25 triệu đồng
   - Không có giấy phép PCCC mà vẫn hoạt động: 30-50 triệu đồng
   - Vi phạm gây cháy: 50-100 triệu đồng + trách nhiệm hình sự

3. QCVN 06:2022/BXD (Sửa đổi 1:2023) – An toàn cháy cho nhà và công trình

   Phần 3 – Yêu cầu lối thoát nạn:
   - Chiều rộng tối thiểu lối thoát: 1,2m (nhà dân dụng), 1,5m (nhà công cộng)
   - Khoảng cách xa nhất từ vị trí bất kỳ đến lối thoát: 25-40m (tùy loại công trình)
   - Cửa thoát nạn phải mở ra phía lối thoát, không được khóa
   - Đèn chiếu sáng sự cố và đèn EXIT tại mỗi lối ra

   Phần 5 – Hệ thống báo cháy và chữa cháy:
   - Đầu báo khói: lắp tại mỗi phòng, tối đa 60m²/đầu báo
   - Đầu báo nhiệt: khu vực bếp, nhà kho
   - Sprinkler: bắt buộc với nhà ≥10 tầng hoặc diện tích sàn ≥300m²

4. QCVN 10:2025/BCA – Trang bị phương tiện PCCC cho nhà và công trình

   Bảng 1 – Định mức bình chữa cháy:
   - Văn phòng: 1 bình ABC 4kg / 50m²
   - Nhà xưởng: 1 bình ABC 6kg / 50m² + 1 bình CO2 5kg / 100m²
   - Kho hàng: 1 bình ABC 6kg / 30m²
   - Nhà ở: tối thiểu 1 bình ABC 2kg/căn hộ

   Bảng 3 – Vị trí lắp đặt:
   - Treo cao 0,8 - 1,5m so với sàn
   - Khoảng cách tối đa giữa 2 bình: 20m
   - Không đặt sau cửa, góc khuất

5. QCVN 25:2025/BCT – An toàn điện trong sản xuất, kinh doanh

   Điều 4 – Hệ thống điện:
   - Dây dẫn phải phù hợp với dòng tải, có vỏ cách điện nguyên vẹn
   - Lắp aptomat (CB) đúng dòng định mức cho từng mạch
   - Lắp RCCB 30mA cho khu vực ẩm ướt (bếp, nhà tắm, ngoài trời)
   - Nối đất cho toàn bộ hệ thống

   Điều 7 – Cấm:
   - Cắm chồng ổ cắm (dùng ổ nối dài nối tiếp)
   - Dùng dây điện tạm, không đạt tiêu chuẩn
   - Để dây điện tiếp xúc với vật liệu dễ cháy
   - Tự ý sửa chữa điện khi không có chuyên môn

6. TIÊU CHUẨN KIỂM TRA ĐỊNH KỲ:

   Hàng ngày:
   - Kiểm tra lối thoát nạn thông thoáng
   - Kiểm tra không có nguồn lửa bất thường

   Hàng tháng:
   - Kiểm tra bình chữa cháy (áp suất, hạn sử dụng)
   - Kiểm tra hệ thống báo cháy (bấm nút test)
   - Kiểm tra đèn EXIT và đèn khẩn cấp

   Hàng quý:
   - Kiểm tra hệ thống điện toàn bộ
   - Kiểm tra hệ thống chống sét
   - Lập biên bản kiểm tra

   Hàng năm:
   - Huấn luyện PCCC cho 100% nhân viên
   - Diễn tập phương án chữa cháy
   - Kiểm định phương tiện PCCC (bình chữa cháy, vòi phun)
   - Gia hạn giấy phép PCCC (nếu có)
"""

FIRE_SAFETY_TIPS = {
    "dien": {
        "title": "An toàn hệ thống điện",
        "tips": [
            "Kiểm tra dây điện: nếu vỏ bọc nứt, bong tróc → thay ngay",
            "Sờ ổ cắm khi đang dùng: nếu NÓNG → ngắt ngay, gọi thợ điện",
            "Mùi khét từ tủ điện/ổ cắm → dấu hiệu chập mạch, ngắt ngay",
            "Không cắm chồng ổ nối dài",
            "Lắp RCCB 30mA cho khu vực ẩm ướt",
        ],
        "legal_ref": "QCVN 25:2025/BCT, Điều 4-7"
    },
    "binh_chua_chay": {
        "title": "Bình chữa cháy",
        "tips": [
            "Trang bị tối thiểu 1 bình ABC 4kg cho mỗi 50m² sàn",
            "Treo ở độ cao 0,8 - 1,5m, nơi dễ tiếp cận",
            "Kiểm tra áp suất bằng đồng hồ hàng tháng",
            "Thay mới khi hết hạn (thường 5-10 năm)",
            "Cách sử dụng: Rút chốt → Hướng vòi → Bóp cò → Quét đáy lửa",
        ],
        "legal_ref": "QCVN 10:2025/BCA, Bảng 1"
    },
    "loi_thoat": {
        "title": "Lối thoát nạn",
        "tips": [
            "Chiều rộng tối thiểu 1,2m",
            "Không khóa cửa thoát nạn trong giờ hoạt động",
            "Lắp đèn EXIT và đèn chiếu sáng sự cố",
            "Niêm yết sơ đồ thoát nạn ở mỗi tầng",
            "Không để hàng hóa cản trở lối thoát",
        ],
        "legal_ref": "QCVN 06:2022/BXD, Phần 3"
    },
}


import os

# Maximum chars per individual document and total additional docs
MAX_CHARS_PER_DOC = 60000
MAX_TOTAL_ADDITIONAL = 400000


def _truncate(text: str, max_chars: int) -> str:
    """Truncate text to max_chars, appending a notice if truncated."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n... [Nội dung đã được rút gọn do quá dài] ..."


def _read_txt(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def _read_pdf(filepath: str) -> str:
    import PyPDF2
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        parts = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                parts.append(extracted)
        return "\n".join(parts)


def _read_docx(filepath: str) -> str:
    import docx
    doc = docx.Document(filepath)
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


# Cache so we don't re-read files on every chat request
_legal_context_cache: str | None = None
_docs_mtime_cache: float = 0.0


def _get_docs_mtime() -> float:
    """Return the most recent mtime across all files in docs/ folder."""
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    if not os.path.isdir(docs_dir):
        return 0.0
    try:
        mtimes = [
            os.path.getmtime(os.path.join(docs_dir, f))
            for f in os.listdir(docs_dir)
        ]
        return max(mtimes) if mtimes else 0.0
    except Exception:
        return 0.0


def get_legal_context_for_chat() -> str:
    """Return the full legal knowledge context for injection into AI prompts.
    Auto-reloads when docs/ folder content changes (file added/modified)."""
    global _legal_context_cache, _docs_mtime_cache

    current_mtime = _get_docs_mtime()
    if _legal_context_cache is not None and current_mtime == _docs_mtime_cache:
        return _legal_context_cache

    if _legal_context_cache is not None and current_mtime != _docs_mtime_cache:
        print(f"🔄 [Legal KB] Phát hiện thay đổi trong docs/, nạp lại...")
        _legal_context_cache = None

    context = LEGAL_DOCUMENTS

    # Read additional documents from docs/ directory
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    READERS = {
        '.txt': ('TXT', _read_txt),
        '.md':  ('TXT', _read_txt),
        '.pdf': ('PDF', _read_pdf),
        '.docx': ('WORD', _read_docx),
    }

    additional_docs = ""
    loaded_count = 0

    for filename in sorted(os.listdir(docs_dir)):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in READERS:
            continue

        filepath = os.path.join(docs_dir, filename)
        label, reader_fn = READERS[ext]

        try:
            raw_text = reader_fn(filepath)
            if not raw_text or not raw_text.strip():
                print(f"⚠️  [Legal KB] File rỗng, bỏ qua: {filename}")
                continue

            truncated = _truncate(raw_text, MAX_CHARS_PER_DOC)
            header = f"\n\n=== TÀI LIỆU BỔ SUNG ({label}): {filename} ===\n"

            # Check total size limit
            if len(additional_docs) + len(header) + len(truncated) > MAX_TOTAL_ADDITIONAL:
                print(f"⚠️  [Legal KB] Đạt giới hạn tổng dung lượng, bỏ qua: {filename}")
                break

            additional_docs += header + truncated
            loaded_count += 1
            orig_len = len(raw_text)
            final_len = len(truncated)
            status = f"({orig_len:,} → {final_len:,} chars)" if orig_len != final_len else f"({final_len:,} chars)"
            print(f"✅ [Legal KB] Đã nạp: {filename} {status}")

        except ImportError as ie:
            print(f"❌ [Legal KB] Thiếu thư viện để đọc {filename}: {ie}")
        except Exception as e:
            print(f"❌ [Legal KB] Lỗi đọc {filename}: {e}")

    if additional_docs:
        context += "\n\n" + additional_docs

    total_len = len(context)
    print(f"📚 [Legal KB] Tổng kết: {loaded_count} tài liệu nạp thành công, tổng {total_len:,} ký tự")

    _legal_context_cache = context
    _docs_mtime_cache = current_mtime
    return context
