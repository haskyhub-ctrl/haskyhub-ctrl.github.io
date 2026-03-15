# seed_recommendations.py — Generate unique recommendations per option
# Each recommendation is specific to the answer given, not generic to category

from models import Recommendation


def generate_recommendations_for_option(db, db_opt, option_data, category_name):
    """Generate a unique recommendation based on the specific answer option."""
    score = option_data.get("score", 0)
    risk = option_data.get("risk", "safe")
    opt_text = option_data.get("text", "")
    
    if score < 2 or not opt_text:
        return
    
    # Determine priority and deadline from risk level
    if risk == "critical":
        priority = "urgent"
        deadline = 7
    elif risk == "high":
        priority = "high"
        deadline = 14
    else:
        priority = "medium"
        deadline = 30
    
    # Generate specific recommendation based on option text content
    rec_text = _build_recommendation(opt_text, category_name, risk)
    
    rec = Recommendation(
        question_option_id=db_opt.id,
        recommendation_text=rec_text,
        priority=priority,
        deadline_days=deadline,
        legal_reference=_get_legal_ref(category_name),
    )
    db.add(rec)


def _build_recommendation(opt_text: str, category: str, risk: str) -> str:
    """Build a specific recommendation text from the option text."""
    opt_lower = opt_text.lower()
    
    # Electrical issues
    if "dây điện" in opt_lower and ("cũ" in opt_lower or "nứt" in opt_lower or "bong" in opt_lower):
        return "Thay thế toàn bộ dây điện cũ/hỏng bằng dây đạt chuẩn TCVN, luồn trong ống bảo vệ PVC. Kiểm tra từng đoạn dây, đánh dấu vị trí cần thay."
    if "dây điện" in opt_lower and ("nối" in opt_lower or "băng keo" in opt_lower):
        return "Loại bỏ các mối nối tạm bằng băng keo. Sử dụng hộp nối chuyên dụng hoặc đầu nối bấm chuẩn cho tất cả các điểm nối dây."
    if "aptomat" in opt_lower or "cầu dao" in opt_lower or "cb" in opt_lower:
        if "không có" in opt_lower or "hỏng" in opt_lower:
            return "Lắp đặt ngay aptomat/CB đúng dòng định mức cho từng mạch điện. Mỗi thiết bị công suất lớn cần aptomat riêng."
        return "Kiểm tra và thay thế aptomat không đúng dòng định mức. Thử test aptomat bằng cách nhấn nút TEST hàng tháng."
    if "rccb" in opt_lower or "elcb" in opt_lower or "rò điện" in opt_lower:
        return "Lắp RCCB/ELCB 30mA cho toàn bộ mạch điện, ưu tiên khu vực ẩm ướt (nhà tắm, bếp). Test nút TEST mỗi tháng."
    if "nối đất" in opt_lower or "tiếp địa" in opt_lower:
        return "Thuê đơn vị có chức năng đo điện trở nối đất. Yêu cầu đạt ≤ 4Ω theo TCVN. Bổ sung dây nối đất cho thiết bị chưa có."
    if "ổ cắm" in opt_lower and ("hở" in opt_lower or "méo" in opt_lower or "chồng" in opt_lower):
        return "Thay thế ổ cắm hỏng/méo. Không cắm chồng nhiều ổ nối dài. Dùng ổ cắm có nắp bảo vệ tại nơi ẩm ướt."
    if "tủ điện" in opt_lower:
        return "Di chuyển vật liệu dễ cháy ra xa tủ điện ít nhất 1m. Lắp khóa và biển cảnh báo 'NGUY HIỂM - ĐIỆN CAO ÁP'."
    if "nóng" in opt_lower or "khét" in opt_lower or "tóe lửa" in opt_lower or "cháy đen" in opt_lower:
        return "NGUY HIỂM: Ngắt ngay mạch điện có hiện tượng nóng/khét. Gọi thợ điện kiểm tra nguyên nhân (quá tải, chập mạch, tiếp xúc kém)."
    if "điện mặt trời" in opt_lower:
        return "Kiểm tra hệ thống điện mặt trời: inverter, dây kết nối, aptomat DC riêng. Yêu cầu đơn vị lắp đặt cung cấp giấy chứng nhận."
    if "thiết bị" in opt_lower and ("cũ" in opt_lower or "không rõ" in opt_lower):
        return "Thay thế thiết bị điện không rõ xuất xứ bằng sản phẩm có nhãn CR (hợp quy). Mua từ đại lý chính hãng, giữ hóa đơn."
    
    # Fire/flame issues
    if "gas" in opt_lower or "bình gas" in opt_lower:
        return "Lắp van ngắt gas tự động và đầu dò khí gas LPG. Đặt bình gas nơi thoáng, xa nguồn nhiệt tối thiểu 1.5m."
    if "hàn cắt" in opt_lower or "khò lửa" in opt_lower:
        return "Lập phiếu xin phép hàn cắt. Dọn sạch vật liệu dễ cháy 10m xung quanh. Bố trí 1 bình chữa cháy + 1 người giám sát."
    if "hút thuốc" in opt_lower:
        return "Quy định khu vực hút thuốc riêng ngoài trời, đặt thùng gạt tàn kim loại có nắp. Treo biển CẤM HÚT THUỐC trong nhà."
    if "đốt" in opt_lower or "vàng mã" in opt_lower or "hương" in opt_lower:
        return "Đốt vàng mã trong lư/thùng kim loại có nắp, đặt trên nền bê tông, xa vật liệu dễ cháy 3m. Luôn có người trông coi."
    if "tàn" in opt_lower:
        return "Dùng thùng gạt tàn kim loại có nắp. Đảm bảo tàn thuốc/than tắt hoàn toàn trước khi vứt (nhúng nước)."
    
    # PCCC violations
    if "bình chữa cháy" in opt_lower:
        return "Mua bổ sung bình chữa cháy ABC 4kg: 1 bình/50m². Đặt nơi dễ lấy, cao 0.8-1.5m. Kiểm tra hạn sử dụng hàng quý."
    if "huấn luyện" in opt_lower or "tập huấn" in opt_lower:
        return "Tổ chức huấn luyện PCCC cho 100% nhân viên. Nội dung: sử dụng bình chữa cháy, quy trình thoát nạn, gọi 114."
    if "nội quy" in opt_lower:
        return "Ban hành nội quy PCCC bằng văn bản. Niêm yết tại: cửa ra vào, khu vực nguy hiểm, bảng tin. Cập nhật hàng năm."
    if "thoát" in opt_lower or "lối thoát" in opt_lower:
        return "Dọn sạch lối thoát hiểm ngay. Lắp đèn EXIT phát quang và đèn chiếu sáng sự cố. Không khóa cửa thoát nạn."
    
    # Technical/equipment
    if "bảo dưỡng" in opt_lower or "bảo trì" in opt_lower:
        return "Lập lịch bảo dưỡng theo khuyến cáo nhà sản xuất. Ghi sổ theo dõi: ngày bảo dưỡng, người thực hiện, hạng mục."
    if "chống sét" in opt_lower or "thu lôi" in opt_lower:
        return "Lắp hệ thống chống sét theo TCVN 9385. Đo điện trở tiếp địa hàng năm, yêu cầu ≤ 10Ω."
    if "áp lực" in opt_lower or "khí nén" in opt_lower or "nồi hơi" in opt_lower:
        return "Đăng ký kiểm định thiết bị áp lực theo NĐ 44/2016/NĐ-CP. Van an toàn phải hoạt động tốt, có tem kiểm định."
    
    # Natural/environment
    if "rừng" in opt_lower or "cháy rừng" in opt_lower:
        return "Tạo băng cản lửa 10m quanh cơ sở. Cắt cỏ khô, dọn lá rụng mùa khô. Bố trí bể chứa nước chữa cháy."
    if "mùa khô" in opt_lower:
        return "Ban hành kế hoạch PCCC mùa khô: tăng tần suất kiểm tra điện, hạn chế nguồn lửa, bố trí trực PCCC 24/7."
    
    # Self-ignition
    if "tự cháy" in opt_lower or "tự phát" in opt_lower or "chất đống" in opt_lower:
        return "Bảo quản vật liệu dễ tự cháy nơi thông thoáng, không chất đống. Kiểm tra nhiệt độ kho định kỳ hàng ngày."
    if "rác" in opt_lower or "phế phẩm" in opt_lower:
        return "Thu gom rác thải hữu cơ hàng ngày vào thùng kim loại có nắp. Không để tích tụ quá 24 giờ."
    
    # Vehicle/transport
    if "xe" in opt_lower or "phương tiện" in opt_lower:
        return "Bố trí bãi đỗ xe riêng biệt, xa khu sản xuất/kho hàng. Không để xe trong lối thoát hiểm."
    if "xăng" in opt_lower or "dầu" in opt_lower or "nhiên liệu" in opt_lower:
        return "Bảo quản xăng dầu trong kho riêng, xa nguồn nhiệt/điện. Dùng can chuyên dụng có nắp kín, gắn nhãn cảnh báo."
    
    # Security/history
    if "sự cố" in opt_lower or "suýt cháy" in opt_lower:
        return "Điều tra nguyên nhân sự cố trước đây, lập biện pháp phòng ngừa tái phát. Tăng cường tuần tra PCCC."
    if "phá hoại" in opt_lower or "tranh chấp" in opt_lower:
        return "Tăng cường an ninh: camera giám sát, bảo vệ 24/7. Phối hợp công an địa phương trong phòng ngừa."
    
    # Generic fallback based on the option text itself
    return f"Khắc phục: {opt_text[:120]}. Liên hệ đơn vị chuyên môn để được tư vấn giải pháp cụ thể."


def _get_legal_ref(category_name: str) -> str:
    """Get relevant legal reference for category."""
    cat_lower = category_name.lower()
    if "điện" in cat_lower:
        return "QCVN 25:2025/BCT, QCVN 25:2025/BKHCN"
    if "lửa" in cat_lower or "nhiệt" in cat_lower:
        return "Nghị định 105/2025/NĐ-CP"
    if "pccc" in cat_lower:
        return "Luật PCCC 55/2024, QCVN 10:2025/BCA"
    if "kỹ thuật" in cat_lower:
        return "Nghị định 105/2025/NĐ-CP"
    if "thiên nhiên" in cat_lower:
        return "QCVN 06:2022/BXD (Sửa đổi 1:2023)"
    return "Luật PCCC 55/2024"
