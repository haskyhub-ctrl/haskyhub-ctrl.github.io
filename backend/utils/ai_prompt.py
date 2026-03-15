"""AI prompt builder for fire risk analysis.

Cập nhật pháp lý 2025:
- Luật PCCC số 55/2024/QH15 (thay Luật PCCC 2001 sửa đổi 2013)
- QCVN 06:2022/BXD kèm Sửa đổi 1:2023
- Nghị định 105/2025/NĐ-CP (thay NĐ 136/2020/NĐ-CP)
- QCVN 10:2025/BCA (thay TCVN 3890:2009) — ban hành 04/11/2025, hiệu lực 30/12/2025
- QCVN 25:2025/BCT — An toàn điện
- QCVN 25:2025/BKHCN — Thiết bị điện gia đình
"""

import json


# Current legal references (2024-2025)
CURRENT_LEGAL_REFERENCES = [
    "Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15",
    "QCVN 06:2022/BXD kèm Sửa đổi 1:2023 QCVN 06:2022/BXD — Quy chuẩn kỹ thuật quốc gia về An toàn cháy cho nhà và công trình",
    "Nghị định 105/2025/NĐ-CP ngày 15/5/2025 quy định chi tiết một số điều và biện pháp thi hành Luật PCCC và CNCH",
    "QCVN 10:2025/BCA — Quy chuẩn kỹ thuật quốc gia về trang bị, bố trí phương tiện phòng cháy, chữa cháy, cứu nạn, cứu hộ cho nhà và công trình (ban hành 04/11/2025, hiệu lực 30/12/2025)",
    "QCVN 25:2025/BCT — Quy chuẩn kỹ thuật quốc gia về An toàn điện",
    "QCVN 25:2025/BKHCN — Quy chuẩn kỹ thuật quốc gia về Thiết bị điện dùng cho lắp đặt điện trong gia đình và hệ thống điện tương tự",
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
    
    answers_info = "CÂU TRẢ LỜI CHI TIẾT:\n"
    for ans in assessment_data.get("detailed_answers", []):
        answers_info += f"- Câu hỏi: {ans.get('question_text', '')}\n"
        answers_info += f"  Trả lời: {ans.get('answer_text', '')} (Điểm nguy cơ: {ans.get('score', 0)})\n"
    
    legal_refs = "\n".join(f"  - {r}" for r in CURRENT_LEGAL_REFERENCES)
    
    prompt = f"""Bạn là chuyên gia Phòng cháy chữa cháy và Cứu nạn cứu hộ (PCCC&CNCH) tại Việt Nam với 20 năm kinh nghiệm.
Hãy phân tích kết quả đánh giá nguy cơ cháy nổ sau đây và đưa ra báo cáo chuyên sâu bằng tiếng Việt.

{facility_info}

{scores_info}

{total_info}

{answers_info}

CĂN CỨ PHÁP LÝ HIỆN HÀNH (2024-2025):
{legal_refs}

YÊU CẦU PHÂN TÍCH:

1. ĐÁNH GIÁ TỔNG QUAN: Nhận xét tổng thể về tình trạng an toàn cháy nổ của cơ sở (2-3 câu).

2. ĐIỂM MẠNH (Phân tích chi tiết): 
   - Dựa vào các nhóm có tỷ lệ nguy cơ THẤP (dưới 25%), giải thích CỤ THỂ tại sao cơ sở làm tốt ở lĩnh vực đó.
   - So sánh với yêu cầu của QCVN 06:2022/BXD (Sửa đổi 1:2023) và Luật PCCC 55/2024.
   - Nêu rõ biện pháp nào cơ sở đang thực hiện đúng.
   - Liệt kê 3-5 điểm mạnh cụ thể.

3. ĐIỂM YẾU NGHIÊM TRỌNG (Phân tích chi tiết):
   - Dựa vào các nhóm có tỷ lệ nguy cơ CAO (trên 40%), chỉ ra RỦI RO CỤ THỂ.
   - Nêu hậu quả có thể xảy ra nếu không khắc phục.
   - Đối với nhóm "Sự cố hệ thống, thiết bị điện": viện dẫn QCVN 25:2025/BCT và QCVN 25:2025/BKHCN.
   - Liệt kê 3-5 điểm yếu nghiêm trọng.

4. KHUYẾN CÁO CHI TIẾT: Đây là phần QUAN TRỌNG NHẤT. Đưa ra 5-8 khuyến cáo CỤ THỂ, CHI TIẾT, bao gồm:
   - Hành động cụ thể (ví dụ: "Thay dây dẫn điện cũ đoạn từ tủ điện đến khu vực bếp")
   - Kiểm tra cụ thể (ví dụ: "Kiểm tra công tắc điện có tiếng kêu tạch tạch không", "Sờ cục sạc xem có nóng bất thường không")
   - Biện pháp khắc phục rõ ràng
   - Thời hạn thực hiện (Ngay lập tức / 7 ngày / 30 ngày / 90 ngày)
   - Mức ưu tiên (urgent/high/medium/low)
   - Căn cứ pháp lý (viện dẫn cụ thể điều khoản liên quan từ danh sách pháp lý ở trên)
   - Đối với lĩnh vực điện: áp dụng QCVN 25:2025/BCT về kiểm tra an toàn điện, tiếp đất, chống sét, cách điện; và QCVN 25:2025/BKHCN về thiết bị điện gia đình đúng tiêu chuẩn.

5. KẾ HOẠCH CẢI THIỆN: Lộ trình cải thiện 30-60-90 ngày

6. THAM CHIẾU PHÁP LÝ: Sử dụng ĐÚNG các quy định pháp luật hiện hành đã liệt kê ở trên. KHÔNG sử dụng các văn bản đã hết hiệu lực (Luật PCCC 2001, TCVN 3890:2009).

Hãy trả về kết quả dưới dạng JSON với cấu trúc:
{{
    "overall_assessment": "string - đánh giá tổng quan 2-3 câu",
    "strengths": ["string - điểm mạnh chi tiết, có so sánh với quy chuẩn"],
    "critical_weaknesses": ["string - điểm yếu nghiêm trọng với hậu quả và viện dẫn pháp lý"],
    "detailed_recommendations": [
        {{
            "title": "string - tiêu đề ngắn gọn",
            "description": "string - mô tả chi tiết hành động, bước kiểm tra cụ thể",
            "priority": "urgent|high|medium|low",
            "deadline": "string - thời hạn (VD: Ngay lập tức, 7 ngày, 30 ngày)",
            "category": "string - nhóm liên quan",
            "legal_basis": "string - căn cứ pháp lý cụ thể"
        }}
    ],
    "improvement_plan": {{
        "30_days": ["string"],
        "60_days": ["string"],
        "90_days": ["string"]
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
            strengths.append(f"{name}: Tỷ lệ nguy cơ chỉ {pct}% — Cơ sở thực hiện tốt các quy định an toàn trong lĩnh vực này, đáp ứng yêu cầu theo QCVN 06:2022/BXD")
        elif pct <= 30:
            strengths.append(f"{name}: Tỷ lệ nguy cơ {pct}% — Mức chấp nhận được, cần duy trì và cải thiện thêm")
    if not strengths:
        strengths = ["Cơ sở đã thực hiện khảo sát đánh giá nguy cơ cháy nổ, cho thấy sự quan tâm đến an toàn PCCC theo Luật PCCC 55/2024"]
    
    # Detailed weaknesses
    weaknesses = []
    for cat in weak_cats[:4]:
        pct = cat.get("percentage", 0)
        name = cat.get("category_name", "")
        name_lower = name.lower()
        if pct >= 60:
            if "điện" in name_lower:
                weaknesses.append(f"{name}: Tỷ lệ nguy cơ {pct}% — NGHIÊM TRỌNG. Vi phạm quy định an toàn điện tại QCVN 25:2025/BCT. Nguy cơ cháy do chập điện, quá tải rất cao. Cần kiểm tra ngay hệ thống điện theo QCVN 25:2025/BKHCN")
            else:
                weaknesses.append(f"{name}: Tỷ lệ nguy cơ {pct}% — NGHIÊM TRỌNG. Không đáp ứng yêu cầu theo QCVN 06:2022/BXD. Có thể bị xử phạt theo Nghị định 105/2025/NĐ-CP")
        elif pct >= 40:
            weaknesses.append(f"{name}: Tỷ lệ nguy cơ {pct}% — Cần cải thiện để đáp ứng tiêu chuẩn. Nguy cơ sự cố nếu không khắc phục kịp thời")
    if not weaknesses:
        weaknesses = ["Không phát hiện điểm yếu nghiêm trọng. Tuy nhiên cần kiểm tra định kỳ theo Nghị định 105/2025/NĐ-CP"]
    
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
                "Khắc phục ngay các nguy cơ cháy nổ nghiêm trọng nhất",
                "Kiểm tra và bảo trì hệ thống phòng cháy hiện có theo Nghị định 105/2025/NĐ-CP",
                "Kiểm tra hệ thống điện theo QCVN 25:2025/BCT",
                "Tập huấn cơ bản về PCCC cho toàn bộ nhân viên"
            ],
            "60_days": [
                "Nâng cấp trang thiết bị PCCC theo Nghị định 105/2025/NĐ-CP",
                "Thiết lập quy trình ứng phó khẩn cấp theo Luật PCCC 55/2024",
                "Diễn tập phương án chữa cháy và thoát nạn",
                "Thay thế thiết bị điện không đạt chuẩn QCVN 25:2025/BKHCN"
            ],
            "90_days": [
                "Đánh giá lại toàn diện sau khi khắc phục",
                "Xây dựng kế hoạch duy trì an toàn dài hạn",
                "Đào tạo chuyên sâu cho đội PCCC cơ sở",
                "Hoàn thiện hồ sơ PCCC theo quy định mới"
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
        return {"title": "Sửa chữa ổ cắm điện", "description": "Thay ổ cắm hỏng, méo, biến dạng. Không cắm chồng ổ nối dài. Sờ ổ cắm khi đang dùng — nếu nóng thì ngắt ngay. Ngửi xem có mùi khét không. Sử dụng ổ cắm đạt chuẩn QCVN 25:2025/BKHCN.", "priority": priority, "deadline": deadline, "category": "Hệ thống điện", "legal_basis": "QCVN 25:2025/BKHCN"}
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
