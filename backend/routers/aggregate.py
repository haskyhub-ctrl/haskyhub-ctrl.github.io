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


class AggregateRequest(BaseModel):
    assessment_ids: Optional[List[str]] = None
    facility_type: Optional[str] = None
    risk_level: Optional[str] = None


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

    assessments = query.all()
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
    for a in assessments:
        cat_scores = (
            db.query(CategoryScore)
            .filter(CategoryScore.assessment_id == a.id)
            .all()
        )
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

    # Calculate averages
    category_analysis = []
    for cat_id, stat in category_stats.items():
        avg_pct = round(stat["total_percentage"] / stat["count"], 1) if stat["count"] > 0 else 0
        category_analysis.append({
            "category_id": cat_id,
            "name": stat["name"],
            "icon": stat["icon"],
            "avg_percentage": avg_pct,
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

    # ===== 7. Generate Rule-Based Recommendations =====
    recommendations = _generate_aggregate_recommendations(
        total, risk_counts, avg_risk, worst_categories, facility_distribution, high_risk_facilities
    )

    # ===== 8. AI Analysis (Gemini) =====
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
        },
        "risk_distribution": risk_counts,
        "facility_distribution": facility_distribution,
        "category_analysis": category_analysis,
        "worst_categories": worst_categories,
        "high_risk_facilities": high_risk_facilities,
        "recommendations": recommendations,
        "ai_analysis": ai_analysis,
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
{chr(10).join(f"- {ft}: {fd['count']} cơ sở, nguy cơ TB {fd['avg_risk']}%, nguy cơ cao {fd['high_risk_count']} cơ sở" for ft, fd in facility_dist.items())}

## CƠ SỞ NGUY CƠ CAO ({len(high_risk)} cơ sở):
{chr(10).join(f"- {f['facility_name']} ({f['facility_type']}): {f['risk_percentage']}% - {f['facility_address']}" for f in high_risk[:10])}

## YÊU CẦU: 
Trả lời bằng JSON với format sau (tiếng Việt):
{{
  "nhan_dinh_chung": "Nhận định tổng quan về tình hình PCCC của địa phương (2-3 câu)",
  "diem_noi_bat": ["Các điểm nổi bật tích cực hoặc tiêu cực (3-5 items)"],
  "nguyen_nhan_chu_yeu": ["Các nguyên nhân chủ yếu dẫn đến tình trạng nguy cơ (3-4 items)"],
  "phuong_huong": [
    {{
      "tieu_de": "Tiêu đề phương hướng",
      "noi_dung": "Nội dung chi tiết",
      "thoi_gian": "Thời gian thực hiện (ngắn hạn/trung hạn/dài hạn)",
      "don_vi_thuc_hien": "Đơn vị chịu trách nhiệm"
    }}
  ],
  "giai_phap_cu_the": [
    {{
      "tieu_de": "Tên giải pháp",
      "noi_dung": "Mô tả chi tiết hành động",
      "muc_do_uu_tien": "khẩn cấp/cao/trung bình/thấp",
      "co_so_phap_ly": "Căn cứ pháp luật (nếu có)"
    }}
  ],
  "kien_nghi": ["Các kiến nghị gửi cấp trên hoặc các ngành liên quan (2-3 items)"]
}}"""

        # Synchronous call for simplicity in FastAPI sync endpoint
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}",
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


def _generate_aggregate_recommendations(total, risk_counts, avg_risk, worst_cats, facility_dist, high_risk):
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

    # Facility type specific recommendations
    for ft, fd in facility_dist.items():
        if fd["high_risk_count"] > 0 and fd["count"] > 0:
            hr_rate = fd["high_risk_count"] / fd["count"] * 100
            if hr_rate > 40:
                recs.append({
                    "priority": "high",
                    "category": "Loại hình cơ sở",
                    "title": f"🏢 Loại hình '{ft}' có tỷ lệ nguy cơ cao: {round(hr_rate, 1)}%",
                    "detail": f"{fd['high_risk_count']}/{fd['count']} cơ sở loại này có nguy cơ cao/rất cao.",
                    "actions": [
                        f"Kiểm tra tập trung toàn bộ cơ sở loại '{ft}'",
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
