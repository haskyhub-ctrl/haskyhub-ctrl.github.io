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
    "Luật Điện lực số 61/2024/QH15",
    "Nghị quyết số 66.18/2026/NQ-CP ngày 18/5/2026 của Chính phủ",
    "Nghị định số 105/2025/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ (sửa đổi, bổ sung bởi Nghị định số 347/2026/NĐ-CP)",
    "QCVN 06:2022/BXD và Sửa đổi 1:2023: Quy chuẩn kỹ thuật quốc gia về An toàn cháy cho nhà và công trình",
    "QCVN 10:2025/BCA: Quy chuẩn kỹ thuật quốc gia về trang bị, bố trí phương tiện phòng cháy, chữa cháy, cứu nạn, cứu hộ cho nhà và công trình",
    "QCVN 01:2021/BXD: Quy chuẩn kỹ thuật quốc gia về Quy hoạch xây dựng",
    "QCVN 13:2018/BXD: Quy chuẩn kỹ thuật quốc gia về Gara ô tô",
    "QCVN 01:2020/BCT: Quy chuẩn kỹ thuật quốc gia về yêu cầu thiết kế cửa hàng xăng dầu",
    "QCVN 25:2025/BCT: Quy chuẩn kỹ thuật quốc gia về An toàn điện",
    "QCVN 25:2025/BKHCN: Quy chuẩn kỹ thuật quốc gia về Thiết bị điện dùng cho lắp đặt điện trong gia đình và hệ thống điện tương tự",
    "TCVN 3890:2023: Phương tiện phòng cháy và chữa cháy cho nhà và công trình, trang bị, bố trí, kiểm tra, bảo dưỡng",
    "TCVN 5738:2021: Phòng cháy chữa cháy, hệ thống báo cháy tự động, yêu cầu kỹ thuật",
    "TCVN 7336:2021: Phòng cháy chữa cháy, hệ thống sprinkler tự động, yêu cầu thiết kế và lắp đặt",
    "TCVN 9385:2012: Chống sét cho công trình xây dựng, hướng dẫn thiết kế, kiểm tra và bảo trì hệ thống",
    "TCVN 6223:2017: Cửa hàng khí dầu mỏ hóa lỏng (LPG), yêu cầu chung về an toàn",
    "TCVN 5307:2009: Kho dầu mỏ và sản phẩm dầu mỏ, yêu cầu thiết kế",
    "Các văn bản quy phạm pháp luật, quy chuẩn, tiêu chuẩn kỹ thuật khác có liên quan",
]


FACILITY_TYPE_LABELS = {
    "industrial": "Cơ sở sản xuất công nghiệp",
    "warehouse": "Kho hàng, kho vật liệu",
    "mixed_residence": "Nhà ở kết hợp kinh doanh",
    "hospitality": "Nhà hàng, khách sạn, chợ, trung tâm thương mại",
    "medical_education": "Bệnh viện, trường học, cơ sở y tế",
    "fuel_gas": "Xăng dầu, khí gas, vật liệu nổ",
    "transport": "Phương tiện giao thông",
    "residential": "Khu dân cư, nhà ở, nhà trọ",
    "construction": "Công trình xây dựng đang thi công",
    "office": "Cơ quan, văn phòng, trụ sở",
    "laboratory": "Nghiên cứu, phòng thí nghiệm",
    "agriculture": "Nông nghiệp, chế biến nông lâm sản",
}


def facility_type_text(raw) -> str:
    """Đổi mã loại hình (có thể nhiều mã, cách nhau dấu phẩy) thành tên tiếng Việt."""
    if not raw:
        return "chưa rõ loại hình"
    parts = [p.strip() for p in str(raw).split(",") if p.strip()]
    return "; ".join(FACILITY_TYPE_LABELS.get(p, p) for p in parts)


def split_answers(assessment_data: dict):
    """Tách các câu trả lời theo mức: rất cao (3), cao (2), trung bình (1), an toàn (0)."""
    ans = assessment_data.get("detailed_answers", []) or []
    red = [a for a in ans if a.get("score", 0) >= 3]
    high = [a for a in ans if a.get("score", 0) == 2]
    mid = [a for a in ans if a.get("score", 0) == 1]
    safe = [a for a in ans if a.get("score", 0) == 0]
    return red, high, mid, safe


def numbered_risky_answers(assessment_data: dict):
    """Danh sách đánh số các câu trả lời có nguy cơ (3 điểm trước, rồi 2 điểm). Dùng chung cho lời nhắc,
    kiểm tra độ phủ và kho tri thức để cùng một số thứ tự."""
    red, high, _mid, _safe = split_answers(assessment_data)
    return red + high


def build_analysis_prompt(assessment_data: dict) -> str:
    """Lời nhắc gửi AI phân tích kết quả khảo sát. Quy tắc nằm ở utils/ai_rules.py."""
    from utils.ai_rules import rules_as_prompt, LEVEL_LABELS, LEVEL_TONE

    level = assessment_data.get("risk_level", "medium")
    level_text = LEVEL_LABELS.get(level, "trung bình")
    tone = LEVEL_TONE.get(level, LEVEL_TONE["medium"])

    facility_info = f"""THÔNG TIN CƠ SỞ (do cơ sở tự khai):
- Tên: {assessment_data.get('facility_name', 'N/A')}
- Loại hình hoạt động: {facility_type_text(assessment_data.get('facility_type'))}
- Địa chỉ: {assessment_data.get('facility_address', 'N/A')}
- Diện tích: {assessment_data.get('facility_area') or 'chưa khai'} m2
- Số người làm việc, sinh hoạt: {assessment_data.get('worker_count') or 'chưa khai'}"""

    scores_info = "KẾT QUẢ THEO NHÓM (do hệ thống tính):\n"
    for cs in assessment_data.get("category_scores", []):
        lv = LEVEL_LABELS.get(cs.get("risk_level"), cs.get("risk_level"))
        scores_info += f"- {cs['category_name']}: {cs['percentage']}% (mức {lv})\n"

    total_info = (
        f"MỨC NGUY CƠ TỔNG THỂ (do hệ thống tính, KHÔNG được tự thay đổi): {assessment_data.get('risk_percentage', 0)}%, "
        f"mức {level_text.upper()}.\nGiọng văn phù hợp mức này: {tone}."
    )

    red, high, mid, safe = split_answers(assessment_data)
    risky = red + high
    answers_info = f"CÁC CÂU TRẢ LỜI CÓ NGUY CƠ ({len(red)} câu mức rất cao, {len(high)} câu mức cao). Số trong [ ] dùng để gắn khuyến nghị:\n"
    for i, a in enumerate(risky, 1):
        tag = "RẤT CAO" if a.get("score", 0) >= 3 else "CAO"
        cat = f" ({a.get('category')})" if a.get("category") else ""
        answers_info += f"[{i}] MỨC {tag}{cat}\n    Câu hỏi: {a.get('question_text', '')}\n    Cơ sở trả lời: {a.get('answer_text', '')}\n"

    answers_info += f"\nCÁC CÂU TRẢ LỜI AN TOÀN ({len(safe)} câu, dùng cho phần ƯU ĐIỂM):\n"
    for a in safe[:12]:
        answers_info += f"- {a.get('question_text', '')} => {a.get('answer_text', '')}\n"
    answers_info += f"\n(Ngoài ra có {len(mid)} câu ở mức nguy cơ thấp, chỉ cần nhắc duy trì, không cần phân tích riêng.)"

    legal_refs = "\n".join(f"  - {r}" for r in CURRENT_LEGAL_REFERENCES)

    return f"""Bạn là chuyên gia tư vấn an toàn phòng cháy chữa cháy và cứu nạn cứu hộ, hỗ trợ Phòng Cảnh sát PCCC và CNCH, Công an thành phố Bắc Ninh.
Hệ thống FRAS là công cụ để người dân và cơ sở TỰ KIỂM TRA, nhận hướng dẫn an toàn miễn phí; kết quả không dùng để xử phạt. Hãy viết bản phân tích như một cán bộ PCCC tận tình đang hướng dẫn trực tiếp chủ cơ sở.

{facility_info}

{scores_info}
{total_info}

{answers_info}

DANH MỤC VĂN BẢN ĐƯỢC PHÉP VIỆN DẪN (chỉ dùng trong trường legal_basis, như căn cứ tham khảo):
{legal_refs}

QUY TẮC BẮT BUỘC:
{rules_as_prompt()}

NỘI DUNG CẦN VIẾT:
1. overall_assessment: 3-5 câu. Nêu loại hình, mức nguy cơ tổng thể (đúng nhãn hệ thống), 2-3 nhóm cần chú ý nhất, và nói rõ kết quả dựa trên thông tin cơ sở cung cấp, chưa qua kiểm tra thực địa.
2. strengths: 3-5 ưu điểm lấy từ các câu trả lời an toàn.
3. critical_weaknesses: mỗi tồn tại một câu mô tả tình trạng theo đúng câu trả lời và hậu quả có thể xảy ra, không viện dẫn pháp luật, không dùng từ vi phạm. Nêu đủ MỌI câu mức rất cao (gộp được nếu cùng chủ đề), sau đó các câu mức cao quan trọng nhất. Tối đa 10 mục.
4. detailed_recommendations: 8-12 khuyến nghị. Mỗi khuyến nghị gồm "answers": danh sách số [ ] của các câu trả lời mà khuyến nghị này xử lý (bắt buộc, để hệ thống kiểm tra độ phủ), "issue": một câu mô tả tình trạng ghi nhận, "title", "description" (các bước cụ thể), "priority" (urgent|high|medium|low), "deadline" (chỉ dùng nhãn thời hạn chuẩn), "responsible_party", "legal_basis".
5. daily_checklist: 5-8 việc tự kiểm tra hằng ngày gắn với các tồn tại của cơ sở này.
6. improvement_plan: lộ trình 30_days, 60_days, 90_days (mỗi giai đoạn 2-4 việc, gồm task, detail, responsible, criteria, legal_basis). Là lộ trình tổng hợp, không chép lại nguyên khuyến nghị.
7. legal_references: chọn các văn bản trong danh mục thực sự liên quan.
8. risk_summary: một câu tóm tắt.

Trả về đúng một khối JSON:
{{
  "overall_assessment": "...",
  "strengths": ["..."],
  "critical_weaknesses": ["..."],
  "detailed_recommendations": [
    {{"answers": [1], "issue": "...", "title": "...", "description": "...", "priority": "urgent|high|medium|low",
      "deadline": "...", "responsible_party": "...", "legal_basis": "..."}}
  ],
  "daily_checklist": ["..."],
  "improvement_plan": {{
    "30_days": [{{"task": "...", "detail": "...", "responsible": "...", "criteria": "...", "legal_basis": "..."}}],
    "60_days": [],
    "90_days": []
  }},
  "legal_references": ["..."],
  "risk_summary": "..."
}}
"""


def build_fallback_analysis(assessment_data: dict) -> dict:
    """Phân tích dự phòng khi AI không hoạt động: soạn từ kho tri thức (analysis_library)."""
    from utils.analysis_library import compose_analysis
    return compose_analysis(assessment_data)


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
