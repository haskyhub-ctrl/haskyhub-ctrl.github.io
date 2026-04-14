"""
Aggregate Analysis Router
Provides locality-wide fire risk assessment reports for administrators.
Includes AI-powered analysis from the perspective of Phòng Cảnh sát PCCC và CNCH Công an tỉnh.
"""
import os
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
from models import (
    User, Assessment, AssessmentAnswer, Question, QuestionOption,
    QuestionCategory, CategoryScore
)
from middleware.auth_middleware import get_current_user
from middleware.rbac import require_role

router = APIRouter(prefix="/api/admin/aggregate", tags=["Aggregate Analysis"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Vietnamese labels for facility types
FACILITY_TYPE_LABELS = {
    "industrial": "Sản xuất công nghiệp",
    "warehouse": "Kho hàng",
    "mixed_residence": "Nhà ở hỗn hợp",
    "hospitality": "Nhà hàng, khách sạn",
    "medical_education": "Bệnh viện, trường học",
    "fuel_gas": "Xăng dầu, khí gas",
    "transport": "Giao thông",
    "residential": "Khu dân cư",
    "construction": "Xây dựng",
    "office": "Văn phòng",
    "laboratory": "Phòng thí nghiệm",
    "agriculture": "Nông nghiệp",
}

FACILITY_TYPE_ICONS = {
    "industrial": "🏭",
    "warehouse": "🏪",
    "mixed_residence": "🏠",
    "hospitality": "🍽️",
    "medical_education": "🏥",
    "fuel_gas": "⛽",
    "transport": "🚌",
    "residential": "🏘️",
    "construction": "🏗️",
    "office": "🏛️",
    "laboratory": "🔬",
    "agriculture": "🌾",
}


class AggregateRequest(BaseModel):
    assessment_ids: Optional[List[str]] = None
    facility_type: Optional[str] = None
    risk_level: Optional[str] = None
    province: Optional[str] = None      # Lọc theo tỉnh (qua User.province)
    limit: Optional[int] = None         # Giới hạn số lượng bài phân tích (None = tất cả)
    include_demo: bool = True           # Có bao gồm dữ liệu demo không


@router.post("/analyze")
def generate_aggregate_analysis(
    request: AggregateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate aggregate fire risk analysis for selected assessments or filters."""
    require_role("admin", "superadmin")(current_user)

    # Build query
    query = db.query(Assessment).filter(Assessment.status == "completed")
    if request.assessment_ids:
        query = query.filter(Assessment.id.in_(request.assessment_ids))
    if request.facility_type:
        query = query.filter(Assessment.facility_type == request.facility_type)
    if request.risk_level:
        query = query.filter(Assessment.risk_level == request.risk_level)
    if not request.include_demo:
        query = query.filter(Assessment.is_demo == False)

    # Lọc theo tỉnh qua User.province
    if request.province:
        user_ids_in_province = [
            u.id for u in db.query(User).filter(User.province == request.province).all()
        ]
        # Cũng lọc các assessment demo có địa chỉ chứa tên tỉnh
        query = query.filter(
            (Assessment.user_id.in_(user_ids_in_province)) |
            (Assessment.facility_address.ilike(f"%{request.province}%"))
        )

    assessments = query.order_by(Assessment.created_at.desc()).all()

    # Áp dụng limit
    if request.limit and request.limit > 0:
        assessments = assessments[:request.limit]

    if not assessments:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá phù hợp")

    total = len(assessments)

    # ===== 1. Risk Distribution =====
    risk_counts = {"safe": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    for a in assessments:
        if a.risk_level in risk_counts:
            risk_counts[a.risk_level] += 1

    # ===== 2. Average Risk Score =====
    avg_risk = sum(a.risk_percentage for a in assessments) / total if total > 0 else 0
    avg_total_score = sum(a.total_score for a in assessments) / total if total > 0 else 0

    # ===== 3. Facility Type Distribution =====
    facility_distribution = {}
    for a in assessments:
        ft = a.facility_type or "unknown"
        if ft not in facility_distribution:
            facility_distribution[ft] = {"count": 0, "avg_risk": 0, "total_risk": 0, "high_risk_count": 0}
        facility_distribution[ft]["count"] += 1
        facility_distribution[ft]["total_risk"] += a.risk_percentage
        if a.risk_level in ("high", "critical"):
            facility_distribution[ft]["high_risk_count"] += 1
    for ft in facility_distribution:
        fd = facility_distribution[ft]
        fd["avg_risk"] = round(fd["total_risk"] / fd["count"], 1) if fd["count"] > 0 else 0
        del fd["total_risk"]

    # ===== 4. Category-level Analysis =====
    category_stats = {}
    # Also track category scores per facility type for detailed recommendations
    facility_category_stats = {}  # {facility_type: {category_id: {total_pct, count, high_risk_count}}}
    for a in assessments:
        cat_scores = (
            db.query(CategoryScore)
            .filter(CategoryScore.assessment_id == a.id)
            .all()
        )
        ft = a.facility_type or "unknown"
        if ft not in facility_category_stats:
            facility_category_stats[ft] = {}
        for cs in cat_scores:
            if cs.category_id not in category_stats:
                cat = db.query(QuestionCategory).filter(QuestionCategory.id == cs.category_id).first()
                category_stats[cs.category_id] = {
                    "name": cat.name if cat else f"Category {cs.category_id}",
                    "icon": cat.icon if cat else "📋",
                    "total_percentage": 0,
                    "count": 0,
                    "high_risk_count": 0,
                    "risk_levels": {"safe": 0, "low": 0, "medium": 0, "high": 0, "critical": 0},
                }
            stat = category_stats[cs.category_id]
            stat["total_percentage"] += cs.percentage
            stat["count"] += 1
            if cs.risk_level in stat["risk_levels"]:
                stat["risk_levels"][cs.risk_level] += 1
            if cs.risk_level in ("high", "critical"):
                stat["high_risk_count"] += 1
            # Track per-facility-type category stats
            if cs.category_id not in facility_category_stats[ft]:
                cat_name = category_stats[cs.category_id]["name"]
                facility_category_stats[ft][cs.category_id] = {
                    "name": cat_name,
                    "total_pct": 0, "count": 0, "high_risk_count": 0
                }
            fcs = facility_category_stats[ft][cs.category_id]
            fcs["total_pct"] += cs.percentage
            fcs["count"] += 1
            if cs.risk_level in ("high", "critical"):
                fcs["high_risk_count"] += 1

    # Calculate averages
    category_analysis = []
    for cat_id, stat in category_stats.items():
        avg_pct = round(stat["total_percentage"] / stat["count"], 1) if stat["count"] > 0 else 0
        category_analysis.append({
            "category_id": cat_id,
            "name": stat["name"],
            "icon": stat["icon"],
            "avg_percentage": avg_pct,
            "high_risk_count": stat["high_risk_count"],
            "high_risk_rate": round(stat["high_risk_count"] / stat["count"] * 100, 1) if stat["count"] > 0 else 0,
            "risk_levels": stat["risk_levels"],
        })
    category_analysis.sort(key=lambda x: x["avg_percentage"])  # Worst first

    # ===== 5. Worst Performing Categories =====
    worst_categories = category_analysis[:3] if len(category_analysis) >= 3 else category_analysis

    # ===== 6. High Risk Facilities =====
    high_risk_facilities = []
    for a in assessments:
        if a.risk_level in ("high", "critical"):
            user = db.query(User).filter(User.id == a.user_id).first()
            high_risk_facilities.append({
                "id": a.id,
                "facility_name": a.facility_name,
                "facility_type": a.facility_type,
                "facility_address": a.facility_address or "N/A",
                "risk_level": a.risk_level,
                "risk_percentage": a.risk_percentage,
                "total_score": a.total_score,
                "max_possible_score": a.max_possible_score,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
                "user_name": user.full_name if user else "N/A",
                "organization": user.organization if user else "N/A",
            })
    high_risk_facilities.sort(key=lambda x: x["risk_percentage"])

    # ===== 7. Map Points (Heatmap + Dots) =====
    map_points = []
    for a in assessments:
        if a.latitude and a.longitude:
            map_points.append({
                "lat": a.latitude,
                "lng": a.longitude,
                "risk_level": a.risk_level,
                "risk_percentage": a.risk_percentage,
                "facility_name": a.facility_name,
                "facility_type": a.facility_type or "unknown",
                "is_demo": getattr(a, "is_demo", False),
            })

    # ===== 8. Generate Rule-Based Recommendations =====
    recommendations = _generate_aggregate_recommendations(
        total, risk_counts, avg_risk, worst_categories, facility_distribution, high_risk_facilities,
        facility_category_stats, category_stats
    )

    # ===== 9. AI Analysis (Gemini) =====
    ai_analysis = None
    if GEMINI_API_KEY and total > 0:
        ai_analysis = _generate_ai_aggregate_analysis(
            total, risk_counts, avg_risk, category_analysis, facility_distribution, high_risk_facilities
        )

    return {
        "summary": {
            "total_assessments": total,
            "avg_risk_percentage": round(avg_risk, 1),
            "avg_total_score": round(avg_total_score, 1),
            "generated_at": datetime.utcnow().isoformat(),
            "province_filter": request.province,
            "limit_applied": request.limit,
        },
        "risk_distribution": risk_counts,
        "facility_distribution": facility_distribution,
        "category_analysis": category_analysis,
        "worst_categories": worst_categories,
        "high_risk_facilities": high_risk_facilities,
        "recommendations": recommendations,
        "ai_analysis": ai_analysis,
        "map_points": map_points,
    }



def _generate_ai_aggregate_analysis(total, risk_counts, avg_risk, category_analysis, facility_dist, high_risk):
    """Call Gemini API to generate aggregate analysis from PCCC management perspective."""
    try:
        import httpx

        # Build comprehensive prompt
        high_critical = risk_counts.get("high", 0) + risk_counts.get("critical", 0)
        high_critical_rate = (high_critical / total * 100) if total > 0 else 0

        prompt = f"""Bạn là chuyên gia Phòng cháy chữa cháy và Cứu nạn cứu hộ (PCCC&CNCH), đang làm việc tại Phòng Cảnh sát PCCC và CNCH, Công an tỉnh. 
Hãy phân tích dữ liệu tổng hợp đánh giá nguy cơ cháy nổ dưới đây và đưa ra nhận định, phương hướng, giải pháp với góc nhìn quản lý nhà nước.

## DỮ LIỆU TỔNG HỢP:
- Tổng số cơ sở đã khảo sát: {total}
- Tỷ lệ nguy cơ trung bình: {round(avg_risk, 1)}%
- Phân bố nguy cơ: An toàn={risk_counts.get('safe',0)}, Thấp={risk_counts.get('low',0)}, Trung bình={risk_counts.get('medium',0)}, Cao={risk_counts.get('high',0)}, Rất cao={risk_counts.get('critical',0)}
- Tỷ lệ cơ sở nguy cơ cao/rất cao: {round(high_critical_rate, 1)}%

## PHÂN TÍCH THEO NHÓM NGUYÊN NHÂN:
{chr(10).join(f"- {c['icon']} {c['name']}: Trung bình {c['avg_percentage']}%, tỷ lệ nguy cơ cao {c['high_risk_rate']}%" for c in category_analysis)}

## PHÂN BỐ THEO LOẠI HÌNH CƠ SỞ:
{chr(10).join(f"- {FACILITY_TYPE_LABELS.get(ft, ft)}: {fd['count']} cơ sở, nguy cơ TB {fd['avg_risk']}%, nguy cơ cao {fd['high_risk_count']} cơ sở" for ft, fd in facility_dist.items())}

## CƠ SỞ NGUY CƠ CAO ({len(high_risk)} cơ sở):
{chr(10).join(f"- {f['facility_name']} ({FACILITY_TYPE_LABELS.get(f['facility_type'], f['facility_type'])}): {f['risk_percentage']}% - {f['facility_address']}" for f in high_risk[:10])}

## YÊU CẦU:
Trả lời bằng JSON với format sau (tiếng Việt). LưU Ý:
- Đối với mỗi loại hình cơ sở có nguy cơ cao, phải chỉ rõ nhóm nguyên nhân nào là lớn nhất
- Đưa ra giải pháp CỤ THỂ với đơn vị phối hợp cụ thể (ví dụ: "Đề nghị Phòng PC07 phối hợp Công ty Điện lực...", "UBND cấp xã phối hợp...") chứ KHÔNG đưa giải pháp chung chung
- Đề xuất các hình thức tuyên truyền cụ thể (video clip, infographic, đăng mạng xã hội, tờ rơi) về từng nhóm nguyên nhân cụ thể
- Tích hợp căn cứ pháp lý mới nhất (Luật PCCC 55/2024, QCVN, Nghị định...) nếu phù hợp
{{
  "nhan_dinh_chung": "Nhận định tổng quan về tình hình PCCC của địa phương (2-3 câu)",
  "diem_noi_bat": ["Các điểm nổi bật tích cực hoặc tiêu cực (3-5 items)"],
  "nguyen_nhan_chu_yeu": ["Các nguyên nhân chủ yếu dẫn đến tình trạng nguy cơ (3-4 items)"],
  "phuong_huong": [
    {{
      "tieu_de": "Tiêu đề phương hướng",
      "noi_dung": "Nội dung chi tiết với đơn vị phối hợp cụ thể",
      "thoi_gian": "Thời gian thực hiện (ngắn hạn/trung hạn/dài hạn)",
      "don_vi_thuc_hien": "Đơn vị chịu trách nhiệm cụ thể (ví dụ: Phòng PC07 và CNCH, UBND cấp xã, Công ty điện lực...)"
    }}
  ],
  "giai_phap_cu_the": [
    {{
      "tieu_de": "Tên giải pháp cụ thể",
      "noi_dung": "Mô tả chi tiết hành động VỚI ĐƠN VỊ PHỐI HỢP (ví dụ: Đề nghị Phòng PC07 phối hợp Công ty Điện lực tổ chức kiểm tra... hoặc UBND cấp xã đề xuất...)",
      "muc_do_uu_tien": "khẩn cấp/cao/trung bình/thấp",
      "hinh_thuc_tuyen_truyen": "Loại hình tuyên truyền cụ thể (ví dụ: video clip về an toàn điện, infographic về thoát nạn cháy...)",
      "co_so_phap_ly": "Căn cứ pháp luật cụ thể (Luật PCCC 55/2024, QCVN 06, Nghị định...)"
    }}
  ],
  "kien_nghi": ["Các kiến nghị gửi cấp trên hoặc các ngành liên quan VỚI ĐƠN VỊ CỤ THỂ (2-3 items)"]
}}"""

        # Synchronous call for simplicity in FastAPI sync endpoint
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.3}
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                try:
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0]
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0]
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {"nhan_dinh_chung": content, "source": "gemini_raw"}
    except Exception as e:
        print(f"AI aggregate analysis error: {e}")
        return None


def _generate_aggregate_recommendations(total, risk_counts, avg_risk, worst_cats, facility_dist, high_risk,
                                        facility_category_stats=None, category_stats=None):
    """Generate rule-based aggregate recommendations for state fire management."""
    recs = []

    # Overall risk assessment
    high_critical_rate = ((risk_counts.get("high", 0) + risk_counts.get("critical", 0)) / total * 100) if total > 0 else 0

    if high_critical_rate > 50:
        recs.append({
            "priority": "critical",
            "category": "Tổng thể",
            "title": "⚠️ Tình hình PCCC của địa phương ở mức BÁO ĐỘNG",
            "detail": f"{round(high_critical_rate, 1)}% cơ sở có nguy cơ cháy nổ cao hoặc rất cao. Cần triển khai đợt kiểm tra toàn diện ngay lập tức.",
            "actions": [
                "Báo cáo UBND cấp trên về tình hình PCCC",
                "Thành lập đoàn kiểm tra liên ngành",
                "Đình chỉ hoạt động các cơ sở vi phạm nghiêm trọng",
                "Tổ chức tập huấn PCCC diện rộng",
            ]
        })
    elif high_critical_rate > 30:
        recs.append({
            "priority": "high",
            "category": "Tổng thể",
            "title": "🔴 Nguy cơ cháy nổ của địa phương ở mức CAO",
            "detail": f"{round(high_critical_rate, 1)}% cơ sở có nguy cơ cháy nổ cao hoặc rất cao.",
            "actions": [
                "Lập kế hoạch kiểm tra PCCC tập trung",
                "Ưu tiên kiểm tra các cơ sở nguy cơ cao",
                "Tăng cường tuyên truyền PCCC",
            ]
        })
    elif high_critical_rate > 15:
        recs.append({
            "priority": "medium",
            "category": "Tổng thể",
            "title": "🟡 Tình trạng PCCC cần được cải thiện",
            "detail": f"{round(high_critical_rate, 1)}% cơ sở có nguy cơ cháy nổ cao.",
            "actions": [
                "Duy trì kiểm tra PCCC định kỳ",
                "Hỗ trợ cơ sở khắc phục tồn tại",
            ]
        })
    else:
        recs.append({
            "priority": "low",
            "category": "Tổng thể",
            "title": "🟢 Tình hình PCCC của địa phương tương đối tốt",
            "detail": f"Chỉ {round(high_critical_rate, 1)}% cơ sở có nguy cơ cao.",
            "actions": [
                "Tiếp tục duy trì kiểm tra định kỳ",
                "Tuyên dương các cơ sở thực hiện tốt PCCC",
            ]
        })

    # Category-specific recommendations
    for cat in worst_cats:
        if cat["avg_percentage"] < 50:
            recs.append({
                "priority": "high",
                "category": cat["name"],
                "title": f"📋 Nhóm yếu nhất: {cat['name']}",
                "detail": f"Điểm trung bình chỉ đạt {cat['avg_percentage']}%. Đây là điểm yếu chung của các cơ sở.",
                "actions": [
                    f"Tổ chức tập huấn chuyên đề về {cat['name'].lower()}",
                    "Hỗ trợ kỹ thuật cho cơ sở trong lĩnh vực này",
                    "Đưa vào trọng tâm kiểm tra đợt tới",
                ]
            })

    # Facility type specific recommendations — WITH DETAILED CAUSE ANALYSIS
    for ft, fd in facility_dist.items():
        if fd["high_risk_count"] > 0 and fd["count"] > 0:
            hr_rate = fd["high_risk_count"] / fd["count"] * 100
            if hr_rate > 40:
                ft_label = FACILITY_TYPE_LABELS.get(ft, ft)
                ft_icon = FACILITY_TYPE_ICONS.get(ft, "🏢")
                
                # Analyze which cause groups are worst for this facility type
                cause_detail = ""
                cause_actions = []
                if facility_category_stats and ft in facility_category_stats:
                    ft_cats = facility_category_stats[ft]
                    # Sort categories by avg risk percentage (worst first = lowest score)
                    sorted_cats = sorted(
                        ft_cats.items(),
                        key=lambda x: (x[1]["total_pct"] / x[1]["count"]) if x[1]["count"] > 0 else 999
                    )
                    if sorted_cats:
                        worst_cat_id, worst_cat_data = sorted_cats[0]
                        worst_avg = round(worst_cat_data["total_pct"] / worst_cat_data["count"], 1) if worst_cat_data["count"] > 0 else 0
                        worst_name = worst_cat_data["name"]
                        worst_hr = worst_cat_data["high_risk_count"]
                        
                        cause_detail = (f"\n\n📊 Phân tích nguyên nhân: Nhóm nguyên nhân có nguy cơ lớn nhất đối với loại hình '{ft_label}' là "
                                       f"'{worst_name}' (điểm an toàn trung bình chỉ đạt {worst_avg}%, "
                                       f"{worst_hr}/{worst_cat_data['count']} cơ sở ở mức nguy cơ cao/rất cao).")
                        
                        # Generate specific actions based on the cause group name
                        cause_actions = _get_cause_specific_actions(worst_name, ft, ft_label)
                        
                        # Also mention 2nd worst if exists
                        if len(sorted_cats) > 1:
                            second_id, second_data = sorted_cats[1]
                            second_avg = round(second_data["total_pct"] / second_data["count"], 1) if second_data["count"] > 0 else 0
                            if second_avg < 60:
                                cause_detail += (f"\nNhóm nguyên nhân đáng lo ngại thứ hai là '{second_data['name']}' "
                                               f"(điểm an toàn trung bình {second_avg}%).")
                
                recs.append({
                    "priority": "high",
                    "category": "Loại hình cơ sở",
                    "title": f"{ft_icon} Loại hình '{ft_label}' có tỷ lệ nguy cơ cao: {round(hr_rate, 1)}%",
                    "detail": (f"{fd['high_risk_count']}/{fd['count']} cơ sở loại này có nguy cơ cao/rất cao."
                              f"{cause_detail}"),
                    "actions": [
                        f"Kiểm tra tập trung toàn bộ cơ sở loại '{ft_label}'",
                        *cause_actions,
                        "Xem xét siết chặt điều kiện kinh doanh",
                    ]
                })

    # Inspection priority
    if high_risk:
        recs.append({
            "priority": "urgent",
            "category": "Kế hoạch kiểm tra",
            "title": f"🔍 Đề xuất kiểm tra {len(high_risk)} cơ sở nguy cơ cao",
            "detail": "Danh sách cơ sở cần ưu tiên kiểm tra trong đợt tới.",
            "actions": [
                f"Kiểm tra ngay {min(5, len(high_risk))} cơ sở có nguy cơ cao nhất",
                "Lập biên bản và yêu cầu khắc phục có thời hạn",
                "Đình chỉ hoạt động nếu vi phạm nghiêm trọng theo Luật PCCC",
            ]
        })

    return recs


def _get_cause_specific_actions(cause_name: str, facility_type: str, ft_label: str) -> list:
    """Generate specific actionable recommendations based on the dominant cause group for a facility type."""
    cause_lower = cause_name.lower()
    actions = []
    
    if "điện" in cause_lower:
        actions = [
            f"🔌 Đề nghị Phòng PC07 hoặc UBND cấp xã phối hợp Công ty Điện lực tổ chức kiểm tra hệ thống điện tại các cơ sở '{ft_label}' có nguy cơ cao",
            f"📹 Tăng cường sản xuất các video clip, infographic tuyên truyền về an toàn điện tại cơ sở '{ft_label}' (kiểm tra dây dẫn, aptomat, RCCB, ổ cắm)",
            "⚡ Yêu cầu các cơ sở kiểm tra định kỳ hệ thống điện theo QCVN 25:2025/BCT; lắp đặt RCCB 30mA cho mạch ẩm ướt",
            "Cảnh báo: Không sử dụng ổ cắm nối dài chồng, không để dây điện quá tải, rút phích sạc thiết bị khi ra ngoài",
        ]
    elif "cháy" in cause_lower or "lửa" in cause_lower or "nhiệt" in cause_lower:
        actions = [
            f"🔥 Tổ chức chiến dịch tuyên truyền phòng chống cháy nổ do nguồn lửa, nguồn nhiệt tại các cơ sở '{ft_label}'",
            "📹 Sản xuất video clip, infographic về quy tắc an toàn khi sử dụng lửa trần, bếp gas, hàn cắt và phổ biến trên mạng xã hội",
            f"🧯 Đề nghị UBND cấp xã phối hợp kiểm tra việc trang bị bình chữa cháy, phương tiện dập lửa ban đầu tại các cơ sở '{ft_label}'",
            "Yêu cầu các cơ sở quy định khu vực hút thuốc, khu vực hàn cắt riêng biệt, cách xa vật liệu dễ cháy",
        ]
    elif "thoát" in cause_lower or "nạn" in cause_lower:
        actions = [
            f"🚪 Tổ chức kiểm tra lối thoát nạn, cầu thang thoát hiểm tại tất cả cơ sở '{ft_label}' có nguy cơ cao",
            "📹 Sản xuất video hướng dẫn thoát nạn, kỹ năng tự cứu khi cháy và phổ biến rộng rãi đến từng cơ sở",
            "Yêu cầu dán sơ đồ thoát nạn tại mỗi tầng, lắp đèn EXIT và đèn chiếu sáng sự cố",
            f"Đề nghị UBND cấp xã phối hợp kiểm tra việc để đồ vật cản trở lối thoát, khóa cửa thoát nạn tại cơ sở '{ft_label}'",
        ]
    elif "thiết bị" in cause_lower or "phương tiện" in cause_lower or "pccc" in cause_lower:
        actions = [
            f"🧯 Rà soát số lượng, chất lượng bình chữa cháy và phương tiện PCCC tại các cơ sở '{ft_label}'",
            "📹 Tăng cường video clip hướng dẫn sử dụng bình chữa cháy (quy tắc PASS), hệ thống báo cháy",
            "Đề nghị Phòng PC07 tổ chức hỗ trợ miễn phí thực hành sử dụng bình chữa cháy cho các cơ sở",
            f"Yêu cầu các cơ sở '{ft_label}' trang bị đầu báo khói độc lập theo QCVN 10:2025/BCA",
        ]
    elif "quản lý" in cause_lower or "huấn luyện" in cause_lower or "nhận thức" in cause_lower:
        actions = [
            f"📚 Tổ chức tập huấn, huấn luyện PCCC bắt buộc cho 100% nhân viên tại cơ sở '{ft_label}'",
            "📹 Sản xuất video clip, infographic về nghĩa vụ PCCC của chủ cơ sở theo Luật PCCC 55/2024 và phổ biến rộng rãi",
            "Yêu cầu chủ cơ sở lập hồ sơ PCCC, bổ nhiệm người phụ trách PCCC, xây dựng phương án chữa cháy",
            "Tổ chức diễn tập PCCC định kỳ ít nhất 1 lần/năm tại các cơ sở",
        ]
    elif "gas" in cause_lower or "khí" in cause_lower or "hóa chất" in cause_lower:
        actions = [
            f"⛽ Đề nghị Phòng PC07 phối hợp Sở Công Thương kiểm tra an toàn gas, hóa chất tại các cơ sở '{ft_label}'",
            "📹 Sản xuất video clip, infographic về an toàn sử dụng gas, phòng chống rò rỉ khí gas và tuyên truyền rộng rãi",
            f"Yêu cầu các cơ sở '{ft_label}' lắp đặt van ngắt gas tự động, đầu dò rò rỉ gas",
            "Kiểm tra hạn sử dụng bình gas, ống dẫn gas; thay thế thiết bị quá hạn",
        ]
    elif "vật liệu" in cause_lower or "cháy" in cause_lower or "kết cấu" in cause_lower:
        actions = [
            f"🏗️ Kiểm tra kết cấu chịu lửa, vật liệu xây dựng tại các cơ sở '{ft_label}' theo QCVN 06:2022/BXD",
            "📹 Tuyên truyền về yêu cầu ngăn cháy lan, khoảng cách an toàn giữa các công trình",
            "Đề nghị cơ sở di chuyển vật liệu dễ cháy ra xa nguồn nhiệt, sắp xếp kho hàng đúng quy cách",
            "Yêu cầu bổ sung vách ngăn cháy, cửa ngăn cháy tại các vị trí theo quy chuẩn",
        ]
    else:
        # Generic
        actions = [
            f"📋 Tổ chức kiểm tra chuyên đề về '{cause_name}' tại tất cả cơ sở '{ft_label}'",
            f"📹 Tăng cường tuyên truyền về nhóm nguyên nhân '{cause_name}' qua video clip, infographic, mạng xã hội",
            f"Phối hợp UBND cấp xã tổ chức rà soát, nhắc nhở các cơ sở '{ft_label}' khắc phục tồn tại",
        ]
    
    return actions


@router.get("/assessments-list")
def list_assessments_for_aggregate(
    facility_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List assessments available for aggregate analysis."""
    require_role("admin", "superadmin")(current_user)

    query = db.query(Assessment).filter(Assessment.status == "completed")
    if facility_type:
        query = query.filter(Assessment.facility_type == facility_type)
    if risk_level:
        query = query.filter(Assessment.risk_level == risk_level)

    assessments = query.order_by(Assessment.completed_at.desc()).all()
    results = []
    for a in assessments:
        user = db.query(User).filter(User.id == a.user_id).first()
        results.append({
            "id": a.id,
            "facility_name": a.facility_name,
            "facility_type": a.facility_type,
            "risk_level": a.risk_level,
            "risk_percentage": a.risk_percentage,
            "total_score": a.total_score,
            "max_possible_score": a.max_possible_score,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            "user_name": user.full_name if user else "N/A",
            "organization": user.organization if user else "N/A",
        })
    return results

@router.get("/dashboard")
def get_dashboard_kpis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get Key Performance Indicators (KPIs) for the Executive Dashboard."""
    require_role("admin", "superadmin")(current_user)

    # 1. Total Facilities Assessed
    completed_assessments = db.query(Assessment).filter(Assessment.status == "completed").all()
    total_assessments = len(completed_assessments)
    
    unique_facilities = len(set(a.user_id for a in completed_assessments))
    total_users = db.query(User).filter(User.role == "user").count()
    coverage_rate = (unique_facilities / total_users * 100) if total_users > 0 else 0

    # 2. Risk Distribution
    risk_counts = {"safe": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    for a in completed_assessments:
        if a.risk_level in risk_counts:
            risk_counts[a.risk_level] += 1

    # 3. Monthly Trends (last 6 months)
    import collections
    monthly_trends = collections.defaultdict(lambda: {"count": 0, "avg_score": 0, "high_risk": 0})
    for a in completed_assessments:
        if a.completed_at:
            month_key = a.completed_at.strftime("%Y-%m")
            monthly_trends[month_key]["count"] += 1
            monthly_trends[month_key]["avg_score"] += a.risk_percentage
            if a.risk_level in ("high", "critical"):
                monthly_trends[month_key]["high_risk"] += 1
    
    # Format monthly trends
    trend_data = []
    for month_key in sorted(monthly_trends.keys())[-6:]:  # Last 6 months
        data = monthly_trends[month_key]
        trend_data.append({
            "month": month_key,
            "count": data["count"],
            "avg_risk": round(data["avg_score"] / data["count"], 1) if data["count"] > 0 else 0,
            "high_risk_count": data["high_risk"]
        })

    # 4. Worst Categories (global)
    category_stats = {}
    from models import CategoryScore, QuestionCategory
    all_cat_scores = db.query(CategoryScore).all()
    for cs in all_cat_scores:
        if cs.category_id not in category_stats:
            cat = db.query(QuestionCategory).filter(QuestionCategory.id == cs.category_id).first()
            category_stats[cs.category_id] = {
                "name": cat.name if cat else f"Category {cs.category_id}",
                "total_percentage": 0,
                "count": 0
            }
        category_stats[cs.category_id]["total_percentage"] += cs.percentage
        category_stats[cs.category_id]["count"] += 1
    
    worst_cats = []
    for cat_id, stat in category_stats.items():
        avg_pct = stat["total_percentage"] / stat["count"] if stat["count"] > 0 else 0
        worst_cats.append({
            "name": stat["name"],
            "avg_score": round(avg_pct, 1)
        })
    worst_cats.sort(key=lambda x: x["avg_score"])

    # 5. Recent Assessments
    recent = []
    for a in sorted(completed_assessments, key=lambda x: x.completed_at if x.completed_at else datetime.min, reverse=True)[:5]:
        recent.append({
            "id": a.id,
            "facility_name": a.facility_name,
            "risk_level": a.risk_level,
            "risk_percentage": a.risk_percentage,
            "date": a.completed_at.strftime("%Y-%m-%d") if a.completed_at else None
        })

    return {
        "kpis": {
            "total_assessments": total_assessments,
            "unique_facilities": unique_facilities,
            "coverage_rate": round(coverage_rate, 1)
        },
        "risk_distribution": risk_counts,
        "trend_data": trend_data,
        "worst_categories": worst_cats[:5],
        "recent_assessments": recent
    }
