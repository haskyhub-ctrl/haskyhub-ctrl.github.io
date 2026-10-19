"""Scoring engine for fire risk assessment.

Quy tắc tính điểm: Weighted Scoring + Cờ đỏ (red flag):

1. Tỷ lệ nguy cơ = trung bình có trọng số của tỷ lệ nguy cơ từng nhóm.
   Trọng số 8 nhóm chung (tổng 100, dựa trên thống kê nguyên nhân cháy tại Việt Nam):
     1. Hệ thống điện 50 • 2. Nguồn lửa/nhiệt 15 • 3. Lối thoát nạn & trang bị PCCC 12
     4. Máy móc 7 • 5. Thiên nhiên 4 • 6. Tự cháy 5 • 7. Phương tiện giao thông 4 • 8. Bổ sung 3
   Các nhóm ĐẶC THÙ theo loại hình (xăng dầu, kho hàng, karaoke...) được chia đều tổng trọng số 30,
   tức chiếm khoảng 23% tỷ lệ chung, để nguy cơ đặc thù không bị "pha loãng".

2. Mức nguy cơ (dùng chung cho tổng thể, từng nhóm và theo dõi khắc phục):
     0-20% LOW • 21-45% MEDIUM • 46-70% HIGH • 71-100% CRITICAL

3. Nâng mức (chỉ áp dụng cho các nhóm trọng yếu: điện, lửa/nhiệt, thoát nạn & PCCC, máy móc,
   tự cháy, phương tiện giao thông và các nhóm đặc thù; không áp dụng cho thiên nhiên, bổ sung):
   - Có ít nhất 1 câu trả lời ở mức nghiêm trọng nhất (cờ đỏ, 3 điểm) -> tổng thể tối thiểu HIGH
   - Có nhóm trọng yếu ở mức CRITICAL -> tối thiểu HIGH
   - Có nhóm trọng yếu ở mức HIGH     -> tối thiểu MEDIUM
"""

# Trọng số 8 nhóm chung theo order_index (tổng = 100)
CATEGORY_WEIGHTS_BY_ORDER = {
    1: 50,   # Dấu hiệu nguy cơ từ hệ thống điện
    2: 15,   # Nguy cơ từ nguồn lửa/nhiệt
    3: 12,   # Lối thoát nạn và trang bị PCCC
    4: 7,    # Dấu hiệu bất thường từ máy móc
    5: 4,    # Tác động từ thiên nhiên
    6: 5,    # Nguy cơ tự cháy
    7: 4,    # Phương tiện giao thông
    8: 3,    # Nguy cơ bổ sung
}

# Fallback cho nhóm chung không có order_index chuẩn: map theo từ khóa trong tên
CATEGORY_WEIGHT_KEYWORDS = {
    "điện": 50,
    "lửa": 15, "nhiệt": 15, "bất cẩn": 15,
    "pccc": 12, "thoát nạn": 12,
    "máy móc": 7, "kỹ thuật": 7,
    "thiên nhiên": 4,
    "tự cháy": 5,
    "giao thông": 4,
}

DEFAULT_WEIGHT = 5            # Nhóm chung không nhận diện được
SPECIFIC_TOTAL_WEIGHT = 30    # Tổng trọng số chia đều cho các nhóm đặc thù của cơ sở
RED_FLAG_SCORE = 3            # Điểm của đáp án nghiêm trọng nhất
NON_KEY_ORDERS = {5, 8}       # Thiên nhiên, nguy cơ bổ sung: không dùng để nâng mức

RISK_RANK = {"low": 0, "safe": 0, "medium": 1, "high": 2, "critical": 3}
RANK_TO_LEVEL = {0: "low", 1: "medium", 2: "high", 3: "critical"}


def is_specific_category(category) -> bool:
    """Nhóm câu hỏi đặc thù theo loại hình cơ sở (không thuộc 8 nhóm chung)."""
    name = (getattr(category, "name", "") or "").strip().lower()
    if name.startswith("đặc thù"):
        return True
    order = getattr(category, "order_index", None)
    return order is not None and order not in CATEGORY_WEIGHTS_BY_ORDER


def is_key_category(category) -> bool:
    """Nhóm trọng yếu được dùng để nâng mức nguy cơ."""
    if is_specific_category(category):
        return True
    order = getattr(category, "order_index", None)
    if order in CATEGORY_WEIGHTS_BY_ORDER:
        return order not in NON_KEY_ORDERS
    name = (getattr(category, "name", "") or "").lower()
    return not ("thiên nhiên" in name or "bổ sung" in name)


def get_category_weight(category):
    """Trọng số nhóm chung. Nhóm đặc thù trả về None (chia trong calculate_total_score)."""
    if is_specific_category(category):
        return None
    if getattr(category, "order_index", None) in CATEGORY_WEIGHTS_BY_ORDER:
        return CATEGORY_WEIGHTS_BY_ORDER[category.order_index]
    name_lower = (getattr(category, "name", "") or "").lower()
    for keyword, weight in CATEGORY_WEIGHT_KEYWORDS.items():
        if keyword in name_lower:
            return weight
    return DEFAULT_WEIGHT


def calculate_risk_level(percentage: float) -> str:
    """Mức nguy cơ từ tỷ lệ %. Dùng chung cho tổng thể, từng nhóm và theo dõi khắc phục."""
    if percentage <= 20:
        return "low"        # 🟢 Nguy cơ thấp - An toàn
    elif percentage <= 45:
        return "medium"     # 🟡 Nguy cơ trung bình - Cần cải thiện
    elif percentage <= 70:
        return "high"       # 🟠 Nguy cơ cao
    else:
        return "critical"   # 🔴 Nguy cơ rất cao - Nghiêm trọng


def calculate_category_risk_level(percentage: float) -> str:
    """Giữ tên cũ cho tương thích; dùng cùng thang với mức tổng thể."""
    return calculate_risk_level(percentage)


def calculate_category_scores(answers, questions_by_category, categories, zero_question_ids=None):
    """Tính điểm nguy cơ cho từng nhóm câu hỏi.

    zero_question_ids: các câu hỏi coi như đã khắc phục (tính 0 điểm), dùng khi theo dõi khắc phục.
    """
    zero_question_ids = set(zero_question_ids or ())
    answer_by_q = {a.question_id: a for a in answers}
    category_scores = []

    for category in categories:
        cat_questions = questions_by_category.get(category.id, [])
        if not cat_questions:
            continue

        max_score = 0
        obtained = 0
        red_flags = 0
        key = is_key_category(category)

        for q in cat_questions:
            q_max = max((opt.score for opt in q.options), default=0)
            max_score += q_max
            answer = answer_by_q.get(q.id)
            if not answer or q.id in zero_question_ids:
                continue
            obtained += answer.score_obtained
            if key and q_max >= RED_FLAG_SCORE and answer.score_obtained >= RED_FLAG_SCORE:
                red_flags += 1

        percentage = (obtained / max_score * 100) if max_score > 0 else 0

        category_scores.append({
            "category_id": category.id,
            "category_name": category.name,
            "category_icon": category.icon,
            "category_color": category.color,
            "score_obtained": obtained,
            "max_score": max_score,
            "percentage": round(percentage, 1),
            "risk_level": calculate_risk_level(percentage),
            "weight": get_category_weight(category),
            "is_specific": is_specific_category(category),
            "is_key": key,
            "red_flags": red_flags,
        })

    return category_scores


def calculate_total_score(category_scores):
    """Tỷ lệ nguy cơ có trọng số + quy tắc nâng mức (cờ đỏ, nhóm trọng yếu)."""
    if not category_scores:
        return {
            "total_score": 0,
            "max_possible_score": 0,
            "risk_percentage": 0.0,
            "risk_level": "low",
            "escalated": False,
            "escalation_reason": "",
        }

    total_obtained = sum(cs["score_obtained"] for cs in category_scores)
    total_max = sum(cs["max_score"] for cs in category_scores)

    # Nhóm đặc thù chia đều tổng trọng số SPECIFIC_TOTAL_WEIGHT
    specific = [cs for cs in category_scores if cs.get("is_specific")]
    specific_weight = SPECIFIC_TOTAL_WEIGHT / len(specific) if specific else 0

    def weight_of(cs):
        if cs.get("is_specific"):
            return specific_weight
        w = cs.get("weight")
        return DEFAULT_WEIGHT if w is None else w

    total_weight = sum(weight_of(cs) for cs in category_scores)
    weighted_sum = sum(cs["percentage"] * weight_of(cs) for cs in category_scores)
    weighted_percentage = (weighted_sum / total_weight) if total_weight > 0 else 0

    risk_level = calculate_risk_level(weighted_percentage)
    base_rank = RISK_RANK.get(risk_level, 0)

    # Quy tắc nâng mức, chỉ xét các nhóm trọng yếu
    min_rank, reasons = 0, []
    red_flag_cats = [cs["category_name"] for cs in category_scores if cs.get("red_flags")]
    if red_flag_cats:
        min_rank = 2
        reasons.append("có câu trả lời ở mức nghiêm trọng nhất tại nhóm: " + ", ".join(red_flag_cats[:3]))
    key_ranks = [(RISK_RANK.get(cs["risk_level"], 0), cs["category_name"]) for cs in category_scores if cs.get("is_key")]
    worst_rank, worst_name = max(key_ranks, default=(0, ""))
    if worst_rank >= 3 and min_rank < 2:
        min_rank = 2
        reasons.append(f"nhóm \"{worst_name}\" ở mức rất cao")
    elif worst_rank >= 2 and min_rank < 1:
        min_rank = 1
        reasons.append(f"nhóm \"{worst_name}\" ở mức cao")

    escalated = base_rank < min_rank
    if escalated:
        risk_level = RANK_TO_LEVEL[min_rank]

    return {
        "total_score": total_obtained,
        "max_possible_score": total_max,
        "risk_percentage": round(weighted_percentage, 1),
        "risk_level": risk_level,
        "escalated": escalated,
        "escalation_reason": ("Mức nguy cơ được nâng do " + "; ".join(reasons) + ".") if escalated else "",
    }


def score_assessment(db, assessment, zero_question_ids=None):
    """Chấm điểm một hồ sơ từ các câu trả lời đã lưu.

    Chỉ tính các câu hỏi đã trả lời và phù hợp loại hình cơ sở. Dùng chung cho lúc hoàn thành khảo sát
    và lúc tính lại nguy cơ khi cơ sở khắc phục (zero_question_ids = câu hỏi đã khắc phục).
    Trả về (category_scores, totals).
    """
    from sqlalchemy.orm import joinedload
    from models import AssessmentAnswer, Question, QuestionCategory
    from routers.survey import normalize_facility_types

    answers = db.query(AssessmentAnswer).filter(AssessmentAnswer.assessment_id == assessment.id).all()

    selected_types = set()
    if assessment.facility_type:
        raw_types = [t.strip() for t in assessment.facility_type.split(",") if t.strip()]
        selected_types = normalize_facility_types(raw_types)

    answered_ids = {a.question_id for a in answers}
    categories = (
        db.query(QuestionCategory)
        .filter(QuestionCategory.is_active == True)
        .order_by(QuestionCategory.order_index)
        .all()
    )
    questions = (
        db.query(Question)
        .filter(Question.is_active == True)
        .options(joinedload(Question.options))
        .all()
    )
    questions_by_category = {}
    for q in questions:
        type_match = (
            not q.facility_type
            or q.facility_type == "all"
            or (selected_types and q.facility_type in selected_types)
        )
        if type_match and q.id in answered_ids:
            questions_by_category.setdefault(q.category_id, []).append(q)

    cat_scores = calculate_category_scores(answers, questions_by_category, categories, zero_question_ids)
    return cat_scores, calculate_total_score(cat_scores)


def get_risk_label_vi(risk_level: str) -> str:
    """Get Vietnamese label for risk level."""
    labels = {
        "low": "🟢 Nguy cơ Thấp",
        "medium": "🟡 Nguy cơ Trung bình",
        "high": "🟠 Nguy cơ Cao",
        "critical": "🔴 Nguy cơ Rất cao",
        "safe": "🟢 An toàn",
    }
    return labels.get(risk_level, risk_level)


def get_risk_color(risk_level: str) -> str:
    """Get color hex for risk level."""
    colors = {
        "low": "#22c55e",
        "medium": "#eab308",
        "high": "#f97316",
        "critical": "#ef4444",
        "safe": "#22c55e",
    }
    return colors.get(risk_level, "#94a3b8")
