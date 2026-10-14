"""AI prompt builder for fire risk analysis.

Cập nhật pháp lý 2025:
- Luật PCCC số 55/2024/QH15 (thay Luật PCCC 2001 sửa đổi 2013)
- QCVN 06:2022/BXD kèm Sửa đổi 1:2023
- Nghị định 105/2025/NĐ-CP (thay NĐ 136/2020/NĐ-CP)
- QCVN 10:2025/BCA (thay TCVN 3890:2009): ban hành 04/11/2025, hiệu lực 30/12/2025
- QCVN 25:2025/BCT: An toàn điện
- QCVN 25:2025/BKHCN: Thiết bị điện gia đình
"""

import json


# Current legal references (2024-2025)
CURRENT_LEGAL_REFERENCES = [
    "Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15",
    "QCVN 06:2022/BXD kèm Sửa đổi 1:2023 QCVN 06:2022/BXD: Quy chuẩn kỹ thuật quốc gia về An toàn cháy cho nhà và công trình",
    "Nghị định 105/2025/NĐ-CP ngày 15/5/2025 quy định chi tiết một số điều và biện pháp thi hành Luật PCCC và CNCH",
    "QCVN 10:2025/BCA: Quy chuẩn kỹ thuật quốc gia về trang bị, bố trí phương tiện phòng cháy, chữa cháy, cứu nạn, cứu hộ cho nhà và công trình (ban hành 04/11/2025, hiệu lực 30/12/2025)",
    "QCVN 25:2025/BCT: Quy chuẩn kỹ thuật quốc gia về An toàn điện",
    "QCVN 25:2025/BKHCN: Quy chuẩn kỹ thuật quốc gia về Thiết bị điện dùng cho lắp đặt điện trong gia đình và hệ thống điện tương tự",
]


def build_analysis_prompt(assessment_data: dict) -> str:
    """Build a structured prompt for AI analysis of fire risk assessment."""
    
    facility_info = f"""
CƠ SỞ ĐƯỢC ĐÁNH GIÁ:
- Tên cơ sở: {assessment_data.get('facility_name', 'N/A')}
- Loại hình: {assessment_data.get('facility_type', 'N/A')}
- Địa chỉ: {assessment_data.get('facility_address', 'N/A')}
- Diện tích: {assessment_data.get('facility_area', 'N/A')} m²
- Số người làm việc: {assessment_data.get('worker_count', 'N/A')}
"""
    
    scores_info = "KẾT QUẢ ĐÁNH GIÁ THEO NHÓM:\n"
    for cs in assessment_data.get("category_scores", []):
        scores_info += f"- {cs['category_name']}: {cs['score_obtained']}/{cs['max_score']} ({cs['percentage']}%) - Mức nguy cơ: {cs['risk_level']}\n"
    
    total_info = f"""
TỔNG ĐIỂM NGUY CƠ: {assessment_data.get('total_score', 0)}/{assessment_data.get('max_possible_score', 0)}
TỶ LỆ NGUY CƠ: {assessment_data.get('risk_percentage', 0)}%
MỨC NGUY CƠ TỔNG: {assessment_data.get('risk_level', 'N/A')}
"""
    
    risky_answers = [a for a in assessment_data.get("detailed_answers", []) if a.get("score", 0) >= 2]
    safe_answers = [a for a in assessment_data.get("detailed_answers", []) if a.get("score", 0) == 0]
    
    answers_info = f"CÁC ĐIỂM TỒN TẠI NGUY CƠ CẦN PHÂN TÍCH ({len(risky_answers)} điểm vi phạm/nguy cơ):\n"
    for ans in risky_answers:
        answers_info += f"- [NGUY CƠ] {ans.get('question_text', '')}: {ans.get('answer_text', '')} (Điểm: {ans.get('score', 0)})\n"
    
    answers_info += f"\nCÁC TIÊU CHÍ AN TOÀN ĐẠT YÊU CẦU ({len(safe_answers)} tiêu chí tốt):\n"
    for ans in safe_answers[:5]:
        answers_info += f"- [TỐT] {ans.get('question_text', '')}: {ans.get('answer_text', '')}\n"
    
    legal_refs = "\n".join(f"  - {r}" for r in CURRENT_LEGAL_REFERENCES)
    
    prompt = f"""Bạn là chuyên gia tư vấn kỹ thuật an toàn Phòng cháy chữa cháy và Cứu nạn cứu hộ (PCCC&CNCH), thực hiện nhiệm vụ theo định hướng chỉ đạo của Phòng Cảnh sát PCCC và CNCH - Công an thành phố Bắc Ninh.
Hãy phân tích kết quả khảo sát nguy cơ cháy nổ sau đây và đưa ra báo cáo chuyên sâu, CHI TIẾT, CỤ THỂ, TRANG TRỌNG bằng tiếng Việt.

{facility_info}

{scores_info}

{total_info}

{answers_info}

CĂN CỨ PHÁP LÝ HIỆN HÀNH (2024-2025):
{legal_refs}

QUY TẮC BẮT BUỘC (STRICT GOVERNMENT RULES - KHÔNG ĐƯỢC VI PHẠM):
0. CHUẨN MỰC HÀNH VĂN NGƯỜI THẬT (0% AI / HUMAN WRITING):
   - Tuyệt đối CẤM sử dụng dấu gạch ngang dài (em dash "—"). Luôn dùng dấu phẩy, dấu chấm, dấu hai chấm hoặc ngoặc đơn.
   - Tuyệt đối CẤM các từ nối sáo rỗng robot: "Trong bối cảnh...", "Không thể phủ nhận rằng...", "Đóng vai trò vô cùng quan trọng...", "Mang lại lợi ích đáng kể...", "Giải pháp toàn diện", "Đột phá", "Tối ưu hóa".
   - Tuyệt đối CẤM cấu trúc giả tạo "không chỉ... mà còn...", không ép danh sách phải đủ 3 ý, không dùng ngôn ngữ quảng cáo tô vẽ.
   - Độ biến thiên câu (burstiness): Trộn câu ngắn gọn dứt khoát (2-5 từ) và câu phân tích kỹ thuật. Viết như một cán bộ kiểm tra PCCC dày dạn kinh nghiệm thực tế đang chỉ dẫn trực tiếp cho chủ cơ sở.
1. VĂN PHONG VÀ TƯ CÁCH: Sử dụng văn phong hành chính nhà nước chuẩn mực, đĩnh đạc, khách quan, mang tính hướng dẫn chuyên môn kỹ thuật. Tuyệt đối KHÔNG dùng từ ngữ cảm tính, tiếng lóng, ẩn dụ tùy tiện (nghiêm cấm dùng các từ như "tử huyệt", "báo động đỏ").
2. NGHIÊM CẤM BỊA ĐẶT VĂN BẢN QUY PHẠM PHÁP LUẬT: Tuyệt đối chỉ viện dẫn các văn bản pháp luật thực tế đang có hiệu lực tại Việt Nam: Luật PCCC và CNCH số 55/2024/QH15; Nghị định 105/2025/NĐ-CP; Nghị định 106/2025/NĐ-CP; Nghị định 144/2021/NĐ-CP; QCVN 06:2022/BXD kèm Sửa đổi 1:2023; QCVN 10:2025/BCA; QCVN 25:2025/BCT; QCVN 25:2025/BKHCN; Thông tư 149/2020/TT-BCA. Nghiêm cấm tự sáng tác số hiệu luật, điều khoản giả mạo!
3. PHÂN ĐỊNH BẢN CHẤT NGUY CƠ:
   - Sự cố hệ thống, thiết bị điện (>50%) và bất cẩn nguồn lửa/nguồn nhiệt (15%) là nguyên nhân trực tiếp dẫn đến cháy.
   - Tồn tại về lối thoát nạn và trang bị PCCC là điều kiện an toàn, phương tiện cứu người và hạn chế hậu quả khi xảy ra cháy, KHÔNG PHẢI là nguyên nhân phát sinh cháy.
4. THỜI HẠN KHẮC PHỤC:
   - Các tồn tại có nguy cơ trực tiếp dẫn đến cháy (dây điện hở, thiết bị phát nhiệt quá mức, rò rỉ gas, hàn cắt không che chắn): Phải ghi rõ thời hạn là "Khắc phục ngay (trong 24h - 48h)", tuyệt đối không để 30 hay 60 ngày!
   - Các tồn tại về bổ sung phương tiện, bảo dưỡng thiết bị: 15 - 30 ngày.
   - Cải tạo kết cấu, thẩm duyệt: theo lộ trình kế hoạch.
5. ĐỔI MỤC ĐIỂM MẠNH: Đặt tên là "ƯU ĐIỂM" (ghi nhận các mặt cơ sở làm tốt, không vội kết luận đạt chuẩn khi chưa kiểm tra thực địa).

YÊU CẦU PHÂN TÍCH (viết CHI TIẾT, không viết chung chung):

1. ĐÁNH GIÁ TỔNG QUAN: Nhận xét tổng thể về tình trạng an toàn PCCC của cơ sở (3-5 câu), đánh giá mức độ rủi ro khách quan theo quy chuẩn hiện hành.

2. ƯU ĐIỂM (Phân tích chi tiết): 
   - Dựa vào các nhóm có tỷ lệ nguy cơ THẤP (dưới 25%), nêu cụ thể các biện pháp tốt mà cơ sở đang duy trì.
   - Liệt kê 3-5 ưu điểm cụ thể.

3. TỒN TẠI & NGUY CƠ CHÁY NỔ TIỀM ẨN:
   - Dựa vào các nhóm có điểm nguy cơ cao, chỉ ra nguy cơ trực tiếp và hậu quả nếu xảy ra sự cố.
   - Đối với nhóm điện: viện dẫn quy định về an toàn điện.
   - Liệt kê 3-5 tồn tại cụ thể.

4. KHUYẾN CÁO CHI TIẾT: Đưa ra 8-12 khuyến cáo CỤ THỂ, THỰC TẾ, DỄ THỰC HIỆN:
   - Hành động từng bước rõ ràng.
   - Các tồn tại có nguy cơ phát sinh cháy cao phải ghi rõ "Khắc phục ngay" (trong 24h - 48h).
   - Biện pháp khắc phục chi tiết, vật tư cần trang bị, nơi mua sắm uy tín.
   - Ước tính chi phí thực tế theo thị trường Việt Nam.
   - Người chịu trách nhiệm cụ thể.
   - Căn cứ pháp lý chính xác (Điều, Khoản).

5. DANH MỤC TỰ KIỂM TRA AN TOÀN HÀNG NGÀY: 5-8 việc chủ cơ sở/người phụ trách tự kiểm tra đầu giờ hoặc cuối ngày.

6. KẾ HOẠCH KHẮC PHỤC THEO LỘ TRÌNH:
   - 30 ngày đầu: Ưu tiên xử lý ngay các nguy cơ cháy nổ cao (trong 24-48h đầu), dọn thông lối thoát, kiểm tra hệ thống điện.
   - 30-60 ngày: Bảo dưỡng, bổ sung trang thiết bị, huấn luyện nghiệp vụ PCCC.
   - 60-90 ngày: Hoàn thiện hồ sơ quản lý PCCC, tự kiểm tra định kỳ.

7. THAM CHIẾU VĂN BẢN QUY PHẠM PHÁP LUẬT: Viện dẫn chính xác văn bản hiện hành.

Hãy trả về kết quả dưới dạng JSON với cấu trúc:
{{
    "overall_assessment": "string - đánh giá tổng quan 3-5 câu, có viện dẫn pháp luật",
    "strengths": ["string - điểm mạnh chi tiết, có so sánh với quy chuẩn"],
    "critical_weaknesses": ["string - điểm yếu nghiêm trọng với hậu quả và viện dẫn pháp lý"],
    "detailed_recommendations": [
        {{
            "title": "string - tiêu đề ngắn gọn",
            "description": "string - mô tả chi tiết từng bước hành động, bước kiểm tra cụ thể, vật tư cần thiết",
            "priority": "urgent|high|medium|low",
            "deadline": "string - thời hạn (VD: Ngay lập tức, 7 ngày, 30 ngày)",
            "category": "string - nhóm liên quan",
            "legal_basis": "string - căn cứ pháp lý cụ thể đến điều khoản",
            "estimated_cost": "string - ước tính chi phí (VD: 500.000-1.000.000 VNĐ)",
            "responsible_party": "string - người/đơn vị chịu trách nhiệm"
        }}
    ],
    "daily_checklist": ["string - mục kiểm tra hàng ngày/hàng tuần"],
    "improvement_plan": {{
        "30_days": [
            {{
                "task": "string - tên công việc",
                "detail": "string - mô tả chi tiết 2-4 câu, các bước cụ thể cần làm",
                "responsible": "string - người/đơn vị chịu trách nhiệm",
                "cost": "string - chi phí ước tính VNĐ",
                "criteria": "string - tiêu chí hoàn thành",
                "legal_basis": "string - căn cứ pháp lý"
            }}
        ],
        "60_days": ["cùng cấu trúc object như 30_days"],
        "90_days": ["cùng cấu trúc object như 30_days"]
    }},
    "legal_references": ["string - chỉ pháp luật hiện hành 2024-2025"],
    "risk_summary": "string - tóm tắt ngắn 1 câu"
}}
"""
    return prompt


def build_fallback_analysis(assessment_data: dict) -> dict:
    """Generate rule-based analysis when AI is not available."""
    
    risk_level = assessment_data.get("risk_level", "medium")
    risk_pct = assessment_data.get("risk_percentage", 50)
    category_scores = assessment_data.get("category_scores", [])
    detailed_answers = assessment_data.get("detailed_answers", [])
    
    # Higher percentage = more risk, so worst categories = highest percentage
    weak_cats = sorted(category_scores, key=lambda c: c.get("percentage", 0), reverse=True)
    strong_cats = sorted(category_scores, key=lambda c: c.get("percentage", 100))
    
    overall = {
        "critical": f"Cơ sở có mức nguy cơ cháy nổ RẤT CAO (tỷ lệ nguy cơ {risk_pct}%). Cần hành động khắc phục NGAY LẬP TỨC theo Luật PCCC 55/2024.",
        "high": f"Cơ sở có mức nguy cơ cháy nổ CAO (tỷ lệ nguy cơ {risk_pct}%). Cần lập kế hoạch khắc phục khẩn cấp theo quy định tại Nghị định 105/2025/NĐ-CP.",
        "medium": f"Cơ sở có mức nguy cơ cháy nổ TRUNG BÌNH (tỷ lệ nguy cơ {risk_pct}%). Cần cải thiện một số vấn đề để đáp ứng QCVN 06:2022/BXD.",
        "low": f"Cơ sở có mức nguy cơ cháy nổ THẤP (tỷ lệ nguy cơ {risk_pct}%). Tiếp tục duy trì các biện pháp an toàn hiện tại."
    }
    
    # Detailed strengths
    strengths = []
    for cat in strong_cats[:4]:
        pct = cat.get("percentage", 0)
        name = cat.get("category_name", "")
        if pct <= 20:
            strengths.append(f"{name}: Tỷ lệ nguy cơ ở mức thấp ({pct}%). Cơ sở thực hiện tốt các biện pháp an toàn trong nhóm này theo định hướng QCVN 06:2022/BXD.")
        elif pct <= 30:
            strengths.append(f"{name}: Tỷ lệ nguy cơ {pct}%, cơ bản chấp nhận được, cần tiếp tục duy trì và kiểm tra định kỳ.")
    if not strengths:
        strengths = ["Cơ sở đã chủ động thực hiện khảo sát đánh giá nguy cơ cháy nổ theo tinh thần Luật PCCC và CNCH 55/2024."]
    
    # Detailed weaknesses
    weaknesses = []
    for cat in weak_cats[:4]:
        pct = cat.get("percentage", 0)
        name = cat.get("category_name", "")
        name_lower = name.lower()
        if pct >= 60:
            if "điện" in name_lower:
                weaknesses.append(f"{name}: Tỷ lệ nguy cơ {pct}%, mức độ nghiêm trọng. Nguy cơ cháy do sự cố thiết bị điện rất cao. Cần rà soát và khắc phục ngay theo QCVN 25:2025/BCT và QCVN 25:2025/BKHCN trong 24h - 48h.")
            else:
                weaknesses.append(f"{name}: Tỷ lệ nguy cơ {pct}%, mức độ nghiêm trọng. Chưa đáp ứng yêu cầu kỹ thuật theo QCVN 06:2022/BXD. Cần có biện pháp xử lý kịp thời để tránh nguy cơ vi phạm Nghị định 105/2025/NĐ-CP.")
        elif pct >= 40:
            weaknesses.append(f"{name}: Tỷ lệ nguy cơ {pct}%. Cần sớm cải thiện để phòng ngừa sự cố phát sinh.")
    if not weaknesses:
        weaknesses = ["Chưa phát hiện điểm nguy cơ nghiêm trọng vượt ngưỡng. Cơ sở cần duy trì kiểm tra an toàn PCCC định kỳ theo Nghị định 105/2025/NĐ-CP."]
    
    # Generate detailed recommendations from answers
    detailed_recs = _generate_fallback_recommendations(detailed_answers, weak_cats)
    
    priority_actions = []
    for cat in weak_cats[:5]:
        pct = cat.get("percentage", 0)
        if pct >= 25:
            priority = "urgent" if pct >= 70 else "high" if pct >= 50 else "medium"
            deadline = "7 ngày" if priority == "urgent" else "30 ngày" if priority == "high" else "60 ngày"
            priority_actions.append({
                "action": f"Khắc phục các vấn đề trong lĩnh vực \"{cat['category_name']}\" (tỷ lệ nguy cơ {pct}%)",
                "priority": priority,
                "deadline": deadline
            })
    
    return {
        "overall_assessment": overall.get(risk_level, overall["medium"]),
        "strengths": strengths,
        "critical_weaknesses": weaknesses,
        "detailed_recommendations": detailed_recs,
        "priority_actions": priority_actions,
        "improvement_plan": {
            "30_days": [
                {"task": "Khắc phục ngay các nguy cơ cháy nổ nghiêm trọng nhất", "detail": "Tự tay rà soát cơ sở: sờ từng ổ cắm xem có nóng không, ngửi xem tủ điện có mùi khét không, kiểm tra lối thoát có bị chặn không. Ngắt nguồn các mạch bất thường. Dọn hàng hóa/xe máy ra xa tủ điện và lối thoát.", "responsible": "Chủ cơ sở tự làm", "cost": "0đ (tự kiểm tra)", "criteria": "100% điểm nguy cơ cao được xử lý hoặc cách ly", "legal_basis": "Luật PCCC 55/2024"},
                {"task": "Mời thợ điện kiểm tra hệ thống", "detail": "Thuê thợ điện địa phương kiểm tra dây dẫn, aptomat, nối đất. Thay ổ cắm hỏng (15.000-50.000đ/cái), thay aptomat đúng dòng (80.000-200.000đ/cái, hãng Sino, LS). Lắp RCCB 30mA cho mạch ẩm ướt (400.000-800.000đ, hãng Schneider/ABB).", "responsible": "Thợ điện địa phương", "cost": "500.000 - 3.000.000đ (tùy quy mô)", "criteria": "Hệ thống điện không nóng, CB không nhảy, có RCCB", "legal_basis": "QCVN 25:2025/BCT"},
                {"task": "Mua bình chữa cháy", "detail": "Mua bình ABC 4kg (300.000-600.000đ/bình) tại cửa hàng PCCC hoặc trên Shopee/Lazada. Tối thiểu 1 bình/50m² sàn. Treo ở độ cao 0,8-1,5m, nơi dễ thấy và dễ lấy. Kiểm tra kim đồng hồ ở vùng xanh hàng tháng.", "responsible": "Chủ cơ sở tự mua", "cost": "300.000 - 600.000đ/bình", "criteria": "Đủ số lượng, treo đúng vị trí, kim vùng xanh", "legal_basis": "QCVN 10:2025/BCA"},
                {"task": "Dọn thông thoáng lối thoát nạn", "detail": "Tự dọn xe máy, hàng hóa, đồ đạc cản trở lối thoát. Không khóa cửa thoát nạn trong giờ hoạt động. Lắp đầu báo khói độc lập (150.000-300.000đ/cái trên Shopee, loại pin 10 năm) tại hành lang, phòng ngủ.", "responsible": "Chủ cơ sở tự làm", "cost": "0đ dọn dẹp + 150.000-300.000đ/đầu báo khói", "criteria": "Lối thoát rộng ≥ 1,2m, không bị cản trở", "legal_basis": "QCVN 06:2022/BXD (Sửa đổi 1:2023)"},
                {"task": "Phổ biến kiến thức PCCC cho mọi người", "detail": "Dạy gia đình/nhân viên: cách gọi 114, cách dùng bình chữa cháy (Rút chốt → Hướng vòi vào gốc lửa → Bóp cò → Quét ngang), đường thoát nạn. Xem video hướng dẫn trên YouTube kênh 'PCCC Việt Nam' để thực hành.", "responsible": "Chủ cơ sở", "cost": "0đ (tự phổ biến)", "criteria": "100% người biết gọi 114 và biết dùng bình chữa cháy", "legal_basis": "Luật PCCC 55/2024"}
            ],
            "60_days": [
                {"task": "Lắp thêm đầu báo khói và đèn chiếu sáng sự cố", "detail": "Gắn đầu báo khói độc lập (loại pin 10 năm) vào trần mỗi phòng: 150.000-300.000đ/cái mua trên Shopee/Lazada. Mua đèn sự cố có pin (200.000-400.000đ/đèn) lắp tại hành lang, cầu thang. Tự lắp được bằng khoan và vít.", "responsible": "Chủ cơ sở tự lắp", "cost": "500.000 - 2.000.000đ (tùy số lượng)", "criteria": "Mỗi phòng/tầng có ít nhất 1 đầu báo khói, hành lang có đèn sự cố", "legal_basis": "Nghị định 105/2025/NĐ-CP"},
                {"task": "In sơ đồ thoát nạn và dán tại mỗi tầng", "detail": "Vẽ sơ đồ thoát nạn đơn giản bằng Word hoặc nhờ tiệm in (50.000-100.000đ/bản A3 ép nhựa). Dán ở cầu thang, hành lang mỗi tầng. Chỉ cần ghi rõ: lối thoát, vị trí bình chữa cháy, vị trí tủ điện, số gọi 114.", "responsible": "Chủ cơ sở tự làm", "cost": "50.000 - 200.000đ", "criteria": "Mỗi tầng có sơ đồ, mọi người biết đường thoát", "legal_basis": "Luật PCCC 55/2024"},
                {"task": "Thay dây điện cũ và aptomat không đạt chuẩn", "detail": "Thay dây điện trên 15 năm bằng dây Cadivi/Goldcup đúng tiết diện (dây 2.5mm² cho ổ cắm, 4mm² cho ĐHKK). Dây Cadivi 2.5mm² khoảng 8.000-12.000đ/mét. Lắp aptomat LS/Sino đúng dòng (80.000-200.000đ/cái). Luồn dây trong ống PVC (3.000-5.000đ/mét).", "responsible": "Thợ điện địa phương", "cost": "2.000.000 - 10.000.000đ (tùy quy mô)", "criteria": "Dây mới, luồn ống, CB đúng dòng, RCCB 30mA khu ẩm", "legal_basis": "QCVN 25:2025/BCT, QCVN 25:2025/BKHCN"},
                {"task": "Thực hành dùng bình chữa cháy", "detail": "Lấy 1 bình chữa cháy cũ/hết hạn để thực hành cho gia đình/nhân viên. Hướng dẫn theo quy tắc PASS: Rút chốt → Hướng vòi vào GỐC lửa (cách 1-2m) → Bóp cò → Quét ngang. Mỗi người thử 1 lần. Liên hệ PCCC địa phương để hỗ trợ miễn phí nếu cần.", "responsible": "Chủ cơ sở + PCCC quận/huyện", "cost": "0đ (PCCC địa phương hỗ trợ miễn phí)", "criteria": "100% người biết dùng bình chữa cháy", "legal_basis": "Nghị định 105/2025/NĐ-CP"}
            ],
            "90_days": [
                {"task": "Đánh giá lại bằng FRAS", "detail": "Vào fras-ai.com làm lại bài đánh giá nguy cơ cháy nổ. So sánh kết quả trước và sau khắc phục. Nếu tỷ lệ nguy cơ vẫn cao, kiểm tra lại các mục chưa khắc phục.", "responsible": "Chủ cơ sở", "cost": "0đ (FRAS miễn phí)", "criteria": "Tỷ lệ nguy cơ giảm ít nhất 30% so với lần đầu"},
                {"task": "Lập checklist kiểm tra hàng tháng", "detail": "In ra bảng checklist đơn giản gồm: (1) Sờ ổ cắm có nóng không, (2) Ngửi tủ điện có mùi khét không, (3) Kiểm tra bình chữa cháy kim còn xanh, (4) Lối thoát có thông thoáng, (5) Đèn EXIT có sáng. Dán bảng tại tủ điện, mỗi tháng tick 1 lần.", "responsible": "Chủ cơ sở", "cost": "0đ (tự in)", "criteria": "Checklist được kiểm tra đều đặn hàng tháng"},
                {"task": "Lắp van ngắt gas tự động (nếu dùng bếp gas)", "detail": "Mua van ngắt gas tự động khi rò rỉ (200.000-400.000đ trên Shopee/Lazada) hoặc đầu dò gas kèm van ngắt (500.000-1.000.000đ). Tự lắp vào sau van bình gas. Kiểm tra ống dẫn gas: nếu cũ trên 3 năm thì thay mới (50.000-80.000đ/ống).", "responsible": "Chủ cơ sở tự lắp", "cost": "200.000 - 1.000.000đ", "criteria": "Van tự ngắt khi rò gas, ống dẫn còn mới", "legal_basis": "Nghị định 105/2025/NĐ-CP"},
                {"task": "Mua thang dây thoát nạn (nhà từ 2 tầng trở lên)", "detail": "Mua thang dây thoát hiểm 5-10m (300.000-800.000đ trên Shopee/Lazada) treo sẵn tại ban công hoặc cửa sổ tầng cao. Hướng dẫn gia đình cách sử dụng. Thay thế cho lối thoát thứ hai khi cầu thang bị cháy.", "responsible": "Chủ cơ sở tự mua", "cost": "300.000 - 800.000đ", "criteria": "Mỗi tầng có ít nhất 1 phương tiện thoát nạn dự phòng", "legal_basis": "Luật PCCC 55/2024"}
            ]
        },
        "legal_references": CURRENT_LEGAL_REFERENCES,
        "risk_summary": f"Tỷ lệ nguy cơ: {risk_pct}%. Mức nguy cơ: {risk_level.upper()}."
    }


def _generate_fallback_recommendations(detailed_answers, weak_cats):
    """Generate detailed recommendations from risky answers."""
    recs = []
    seen_titles = set()
    
    for ans in detailed_answers:
        score = ans.get("score", 0)
        if score < 2:
            continue
        
        q_text = ans.get("question_text", "")
        a_text = ans.get("answer_text", "")
        
        # Generate recommendation based on answer content
        rec = _answer_to_recommendation(q_text, a_text, score)
        if rec and rec["title"] not in seen_titles:
            seen_titles.add(rec["title"])
            recs.append(rec)
    
    return recs[:8]  # Max 8 recommendations


def _answer_to_recommendation(question: str, answer: str, score: int) -> dict:
    """Convert a risky answer into a specific recommendation."""
    q_lower = question.lower()
    a_lower = answer.lower()
    
    priority = "urgent" if score >= 4 else "high" if score >= 3 else "medium"
    deadline = "Ngay lập tức" if score >= 4 else "7 ngày" if score >= 3 else "30 ngày"
    
    if "dây" in q_lower and "điện" in q_lower:
        return {"title": "Thay thế dây điện không đạt chuẩn", "description": "Kiểm tra toàn bộ hệ thống dây điện theo QCVN 25:2025/BCT. Thay dây cũ, nứt, bong tróc vỏ cách điện. Luồn dây trong ống bảo vệ PVC. Kiểm tra xem dây có nóng bất thường không bằng cách sờ nhẹ khi đang sử dụng.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BCT, QCVN 25:2025/BKHCN"}
    if "aptomat" in q_lower or "cầu dao" in q_lower:
        return {"title": "Lắp đặt aptomat đúng tiêu chuẩn", "description": "Lắp aptomat đúng dòng định mức cho từng mạch theo QCVN 25:2025/BCT. Kiểm tra nút TEST hàng tháng. Kiểm tra aptomat có tự ngắt khi quá tải không. Sử dụng thiết bị đạt chuẩn QCVN 25:2025/BKHCN.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BCT"}
    if "rò điện" in q_lower or "rccb" in q_lower:
        return {"title": "Lắp thiết bị chống rò điện", "description": "Lắp RCCB 30mA cho toàn bộ mạch điện, đặc biệt khu vực ẩm ướt theo quy định tại QCVN 25:2025/BCT. Nhấn nút TEST mỗi tháng để kiểm tra hoạt động.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BCT"}
    if "nối đất" in q_lower or "tiếp đất" in q_lower:
        return {"title": "Kiểm tra hệ thống nối đất", "description": "Đo điện trở nối đất, yêu cầu không quá 4 ohm theo QCVN 25:2025/BCT. Bổ sung dây nối đất cho thiết bị chưa có. Kiểm tra hệ thống chống sét.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BCT"}
    if "ổ cắm" in q_lower:
        return {"title": "Sửa chữa ổ cắm điện", "description": "Thay ổ cắm hỏng, méo, biến dạng. Không cắm chồng ổ nối dài. Sờ ổ cắm khi đang dùng, nếu thấy nóng thì ngắt ngay. Ngửi xem có mùi khét không. Sử dụng ổ cắm đạt chuẩn QCVN 25:2025/BKHCN.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BKHCN"}
    if "tủ điện" in q_lower:
        return {"title": "Dọn dẹp khu vực tủ điện", "description": "Di chuyển vật liệu dễ cháy ra xa tủ điện tối thiểu 1 mét. Lắp khóa và biển cảnh báo nguy hiểm. Đảm bảo thông thoáng khu vực tủ điện theo QCVN 06:2022/BXD.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 06:2022/BXD (Sửa đổi 1:2023)"}
    if "nóng" in q_lower or "khét" in q_lower:
        return {"title": "Xử lý hiện tượng nóng bất thường, mùi khét", "description": "NGUY HIỂM: Ngắt mạch có hiện tượng nóng, mùi khét ngay lập tức. Kiểm tra: sờ ổ cắm, ngửi mùi khét, nghe tiếng kêu từ công tắc. Gọi thợ điện có chứng chỉ theo QCVN 25:2025/BCT.", "priority": "urgent", "deadline": "Ngay lập tức", "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BCT"}
    if "quá tải" in q_lower or "tải điện" in q_lower:
        return {"title": "Xử lý quá tải hệ thống điện", "description": "Tính toán lại công suất tải trên từng mạch điện. Không sử dụng nhiều thiết bị công suất lớn trên một mạch. Nâng cấp dây dẫn và aptomat phù hợp theo QCVN 25:2025/BCT.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BCT"}
    if "chống sét" in q_lower or "sét" in q_lower:
        return {"title": "Kiểm tra hệ thống chống sét", "description": "Kiểm tra kim thu sét, dây dẫn sét, cọc tiếp đất. Đo điện trở tiếp đất chống sét. Bảo dưỡng hệ thống chống sét định kỳ theo QCVN 25:2025/BCT.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BCT"}
    if "gas" in q_lower or "bếp" in q_lower:
        return {"title": "An toàn bếp gas", "description": "Lắp van ngắt gas tự động và đầu dò rò rỉ gas. Đặt bình gas xa nguồn nhiệt tối thiểu 1,5 mét. Kiểm tra ống dẫn gas có bị giòn, nứt không.", "priority": priority, "deadline": deadline, "category": "An toàn lửa, nhiệt", "legal_basis": "Nghị định 105/2025/NĐ-CP"}
    if "hút thuốc" in q_lower:
        return {"title": "Kiểm soát hút thuốc", "description": "Quy định khu vực hút thuốc riêng ngoài trời. Đặt thùng gạt tàn kim loại. Treo biển cấm hút thuốc trong nhà xưởng.", "priority": priority, "deadline": deadline, "category": "An toàn lửa, nhiệt", "legal_basis": "Luật PCCC 55/2024"}
    if "bình chữa cháy" in q_lower:
        return {"title": "Bổ sung bình chữa cháy", "description": "Trang bị bình chữa cháy ABC 4kg: 1 bình trên 50 m2 sàn. Treo ở độ cao 0,8 đến 1,5 mét, nơi dễ tiếp cận. Kiểm tra áp suất bằng đồng hồ hàng tháng.", "priority": priority, "deadline": deadline, "category": "Trang thiết bị PCCC", "legal_basis": "Nghị định 105/2025/NĐ-CP"}
    if "thoát" in q_lower or "lối thoát" in q_lower:
        return {"title": "Thông thoáng lối thoát hiểm", "description": "Dọn sạch lối thoát ngay. Lắp đèn EXIT và đèn chiếu sáng sự cố. KHÔNG khóa cửa thoát nạn trong giờ hoạt động. Chiều rộng tối thiểu 1,2 mét.", "priority": "urgent", "deadline": "Ngay lập tức", "category": "Thoát nạn", "legal_basis": "QCVN 06:2022/BXD (Sửa đổi 1:2023)"}
    if "huấn luyện" in q_lower:
        return {"title": "Tổ chức huấn luyện PCCC", "description": "Huấn luyện 100% nhân viên: sử dụng bình chữa cháy, quy trình thoát nạn, gọi 114. Thực tập ít nhất 1 lần mỗi năm.", "priority": priority, "deadline": deadline, "category": "Đào tạo PCCC", "legal_basis": "Luật PCCC 55/2024"}
    if "xe điện" in q_lower or "sạc" in q_lower:
        return {"title": "An toàn sạc xe điện, thiết bị điện", "description": "Không sạc xe điện, điện thoại qua đêm. Sử dụng bộ sạc chính hãng đạt chuẩn QCVN 25:2025/BKHCN. Đặt vị trí sạc xa vật liệu dễ cháy. Rút sạc khi đầy pin.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BKHCN"}
    
    # Generic
    return {"title": f"Khắc phục: {question[:60]}", "description": f"Vấn đề phát hiện: {answer[:100]}. Cần có biện pháp khắc phục cụ thể theo quy định hiện hành.", "priority": priority, "deadline": deadline, "category": "Khác", "legal_basis": "Luật PCCC 55/2024"}
