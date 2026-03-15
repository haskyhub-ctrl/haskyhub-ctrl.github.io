"""Scoring engine for fire risk assessment.

Quy tắc tính điểm — Weighted Scoring + Max-Domination Rule:

Trọng số theo 8 nhóm nguyên nhân cháy:
  1. Sự cố hệ thống, thiết bị điện:        55 điểm (55%)
  2. Sơ suất, bất cẩn dùng lửa/nhiệt:      15 điểm (15%)
  3. Vi phạm quy định PCCC:                 10 điểm (10%)
  4. Sự cố kỹ thuật (thiết bị, máy móc):    7 điểm (7%)
  5. Tác động thiên nhiên:                   4 điểm (4%)
  6. Tự cháy:                                4 điểm (4%)
  7. Tai nạn giao thông:                     3 điểm (3%)  (max_score=3 in seed)
  8. Nguyên nhân khác / Rủi ro bổ sung:      2 điểm (2%)

Max-Domination Rule:
  - Nếu BẤT KỲ nhóm nào = CRITICAL -> tổng thể tối thiểu = HIGH
  - Nếu BẤT KỲ nhóm nào = HIGH     -> tổng thể tối thiểu = MEDIUM
  - Điều này đảm bảo: 1 nhóm nguy cơ cao => tổng thể không thể xanh

Risk Level (từ % nguy cơ):
  0-20%   -> LOW      (🟢 An toàn)
  21-45%  -> MEDIUM   (🟡 Cần cải thiện)
  46-70%  -> HIGH     (🟠 Nguy cơ cao)
  71-100% -> CRITICAL (🔴 Nguy hiểm nghiêm trọng)
"""

# Trọng số mặc định theo tên nhóm (khớp với seed_data.py)
# Key = tên category hoặc order_index, giá trị = weight (tổng = 100)
CATEGORY_WEIGHTS_BY_ORDER = {
    1: 55,   # Sự cố hệ thống, thiết bị điện
    2: 15,   # Sơ suất, bất cẩn dùng lửa/nhiệt
    3: 10,   # Vi phạm quy định PCCC
    4: 7,    # Sự cố kỹ thuật
    5: 4,    # Tác động thiên nhiên
    6: 4,    # Tự cháy
    7: 3,    # Tai nạn giao thông
    8: 2,    # Nguyên nhân khác
}

# Fallback: map bằng tên chứa keyword
CATEGORY_WEIGHT_KEYWORDS = {
    "điện": 55,
    "lửa": 15, "nhiệt": 15, "bất cẩn": 15,
    "pccc": 10, "quy định": 10,
    "kỹ thuật": 7,
    "thiên nhiên": 4,
    "tự cháy": 4,
    "giao thông": 3,
}

DEFAULT_WEIGHT = 5  # For specific categories (A-L) not in common groups


def get_category_weight(category):
    """Get weight for a category based on order_index or name matching."""
    # Try order_index first (common categories 1-8)
    if hasattr(category, 'order_index') and category.order_index in CATEGORY_WEIGHTS_BY_ORDER:
        return CATEGORY_WEIGHTS_BY_ORDER[category.order_index]
    
    # Try keyword matching on name
    if hasattr(category, 'name') and category.name:
        name_lower = category.name.lower()
        for keyword, weight in CATEGORY_WEIGHT_KEYWORDS.items():
            if keyword in name_lower:
                return weight
    
    return DEFAULT_WEIGHT


def calculate_risk_level(percentage: float) -> str:
    """Xác định mức nguy cơ từ phần trăm điểm nguy cơ.
    Percentage CAO = nguy hiểm hơn (nhiều điểm nguy cơ hơn).
    """
    if percentage <= 20:
        return "low"        # 🟢 Nguy cơ thấp - An toàn
    elif percentage <= 45:
        return "medium"     # 🟡 Nguy cơ trung bình - Cần cải thiện
    elif percentage <= 70:
        return "high"       # 🟠 Nguy cơ cao
    else:
        return "critical"   # 🔴 Nguy cơ rất cao - Nghiêm trọng


def calculate_category_risk_level(percentage: float) -> str:
    """Xác định mức nguy cơ theo nhóm câu hỏi.
    < 25% điểm tối đa nhóm -> Xanh (low)
    25-50% -> Vàng (medium)
    50-75% -> Cam (high)
    > 75% -> Đỏ (critical)
    """
    if percentage < 25:
        return "low"
    elif percentage < 50:
        return "medium"
    elif percentage < 75:
        return "high"
    else:
        return "critical"


RISK_RANK = {"low": 0, "safe": 0, "medium": 1, "high": 2, "critical": 3}


def calculate_category_scores(answers, questions_by_category, categories):
    """Tính điểm nguy cơ cho từng nhóm câu hỏi.
    
    Returns list of dicts with category scoring info.
    """
    category_scores = []
    
    for category in categories:
        cat_questions = questions_by_category.get(category.id, [])
        if not cat_questions:
            continue
        
        max_score = 0
        obtained = 0
        
        for q in cat_questions:
            # Max score for this question = max option score (worst case)
            q_max = max((opt.score for opt in q.options), default=0)
            max_score += q_max
            
            # Find answer for this question
            answer = next((a for a in answers if a.question_id == q.id), None)
            if answer:
                obtained += answer.score_obtained
        
        percentage = (obtained / max_score * 100) if max_score > 0 else 0
        weight = get_category_weight(category)
        
        category_scores.append({
            "category_id": category.id,
            "category_name": category.name,
            "category_icon": category.icon,
            "category_color": category.color,
            "score_obtained": obtained,
            "max_score": max_score,
            "percentage": round(percentage, 1),
            "risk_level": calculate_category_risk_level(percentage),
            "weight": weight,
        })
    
    return category_scores


def calculate_total_score(category_scores):
    """Tính tổng điểm nguy cơ với trọng số và quy tắc max-domination.
    
    Weighted Average:
      - Mỗi nhóm đóng góp: (percentage * weight) / total_weight
      
    Max-Domination Rule:
      - Nếu BẤT KỲ nhóm nào = critical -> tổng thể >= high
      - Nếu BẤT KỲ nhóm nào = high     -> tổng thể >= medium
    """
    if not category_scores:
        return {
            "total_score": 0,
            "max_possible_score": 0,
            "risk_percentage": 0.0,
            "risk_level": "low",
        }
    
    # Raw totals (for display)
    total_obtained = sum(cs["score_obtained"] for cs in category_scores)
    total_max = sum(cs["max_score"] for cs in category_scores)
    
    # Weighted percentage calculation
    total_weight = sum(cs.get("weight", DEFAULT_WEIGHT) for cs in category_scores)
    weighted_sum = 0.0
    
    max_cat_risk_rank = 0  # Track worst category risk
    
    for cs in category_scores:
        w = cs.get("weight", DEFAULT_WEIGHT)
        pct = cs["percentage"]
        weighted_sum += pct * w
        
        cat_rank = RISK_RANK.get(cs["risk_level"], 0)
        if cat_rank > max_cat_risk_rank:
            max_cat_risk_rank = cat_rank
    
    weighted_percentage = (weighted_sum / total_weight) if total_weight > 0 else 0
    
    # Determine risk level from weighted percentage
    risk_level = calculate_risk_level(weighted_percentage)
    
    # Apply Max-Domination Rule
    # If any category is critical -> overall must be at least high
    # If any category is high -> overall must be at least medium
    risk_rank = RISK_RANK.get(risk_level, 0)
    
    if max_cat_risk_rank >= 3:  # critical
        min_rank = 2  # at least high
    elif max_cat_risk_rank >= 2:  # high
        min_rank = 1  # at least medium
    else:
        min_rank = 0
    
    if risk_rank < min_rank:
        # Elevate risk level
        rank_to_level = {0: "low", 1: "medium", 2: "high", 3: "critical"}
        risk_level = rank_to_level[min_rank]
    
    return {
        "total_score": total_obtained,
        "max_possible_score": total_max,
        "risk_percentage": round(weighted_percentage, 1),
        "risk_level": risk_level,
    }


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
