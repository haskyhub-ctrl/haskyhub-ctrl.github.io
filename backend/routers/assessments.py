import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from database import get_db
from models import (
    User, Assessment, AssessmentAnswer, CategoryScore,
    Question, QuestionOption, QuestionCategory, Recommendation
)
from schemas import AssessmentResponse, AssessmentDetail, CategoryScoreResponse, RecommendationResponse
from middleware.auth_middleware import get_current_user, get_optional_user
from utils.recommendations import get_recommendations_for_assessment

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


@router.get("", response_model=List[AssessmentResponse])
def list_assessments(
    status: Optional[str] = None,
    limit: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Assessment).filter(Assessment.user_id == current_user.id)
    if status:
        query = query.filter(Assessment.status == status)
    query = query.order_by(Assessment.created_at.desc())
    if limit > 0:
        query = query.limit(limit)
    assessments = query.all()
    return [AssessmentResponse.model_validate(a) for a in assessments]


@router.get("/map-data")
def get_user_map_data(
    risk_level: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """Get all completed assessments + imported facilities for map display, but hide info of others."""
    results = []
    assessed_user_ids = set()

    # 1. Completed assessments
    query = db.query(Assessment).filter(Assessment.status == "completed")
    if risk_level and risk_level != "unassessed":
        query = query.filter(Assessment.risk_level == risk_level)

    if risk_level != "unassessed":
        assessments = query.order_by(Assessment.created_at.desc()).all()
        for a in assessments:
            user = db.get(User, a.user_id)
            lat = a.latitude if a.latitude is not None else (user.latitude if user else None)
            lng = a.longitude if a.longitude is not None else (user.longitude if user else None)
            if lat is None or lng is None:
                continue
                
            assessed_user_ids.add(a.user_id)
            
            is_own = (current_user is not None and a.user_id == current_user.id)
            results.append({
                "id": a.id if is_own else "hidden",
                "facility_name": a.facility_name if is_own else "",
                "facility_type": a.facility_type,
                "facility_address": a.facility_address if is_own else "",
                "latitude": lat,
                "longitude": lng,
                "risk_level": a.risk_level,
                "risk_percentage": a.risk_percentage,
                "total_score": a.total_score if is_own else 0,
                "max_possible_score": a.max_possible_score if is_own else 0,
                "completed_at": a.completed_at.isoformat() if (a.completed_at and is_own) else None,
                "user_name": user.full_name if (user and is_own) else "",
                "organization": user.organization if (user and is_own) else "",
                "source": "assessment",
                "mitigation_data": a.mitigation_data if is_own else None,
            })

    # 2. Imported facilities (users with coordinates) that have no assessment
    if not risk_level or risk_level == "unassessed":
        facility_users = db.query(
            User.id,
            User.full_name,
            User.facility_types,
            User.ward,
            User.province,
            User.latitude,
            User.longitude,
            User.organization,
        ).filter(
            User.latitude.isnot(None),
            User.longitude.isnot(None),
            User.facility_code.isnot(None),
        ).limit(1000).all()
        for u_id, u_full_name, u_types, u_ward, u_prov, u_lat, u_lng, u_org in facility_users:
            if u_id in assessed_user_ids:
                continue
                
            is_own = (current_user is not None and u_id == current_user.id)
            results.append({
                "id": u_id if is_own else "hidden",
                "facility_name": u_full_name if is_own else "Cơ sở chưa đánh giá",
                "facility_type": u_types,
                "facility_address": f"{u_ward or ''}, {u_prov or ''}".strip(", ") if is_own else "***",
                "latitude": u_lat,
                "longitude": u_lng,
                "risk_level": "unassessed",
                "risk_percentage": 0,
                "total_score": 0,
                "max_possible_score": 0,
                "completed_at": None,
                "user_name": u_full_name if is_own else "***",
                "organization": (u_org or u_full_name) if is_own else "***",
                "source": "facility",
            })

    return results


@router.get("/compare/list")
def compare_assessments(
    ids: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Return 2-4 assessments with their category scores for the compare page."""
    id_list = [i.strip() for i in ids.split(",") if i.strip()][:4]
    query = db.query(Assessment).filter(Assessment.id.in_(id_list))
    if current_user.role not in ("admin", "superadmin"):
        query = query.filter(Assessment.user_id == current_user.id)
    by_id = {a.id: a for a in query.all()}

    results = []
    for aid in id_list:  # keep the order the user picked
        a = by_id.get(aid)
        if not a:
            continue
        scores = []
        for cs in db.query(CategoryScore).filter(CategoryScore.assessment_id == a.id).all():
            cat = db.query(QuestionCategory).get(cs.category_id)
            scores.append({
                "category_id": cs.category_id,
                "category_name": cat.name if cat else "",
                "score_obtained": cs.score_obtained,
                "max_score": cs.max_score,
                "percentage": cs.percentage,
                "risk_level": cs.risk_level,
            })
        results.append({
            "assessment": AssessmentResponse.model_validate(a).model_dump(mode="json"),
            "category_scores": scores,
        })
    return results


@router.get("/{assessment_id}", response_model=AssessmentDetail)
def get_assessment_detail(
    assessment_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    # Admin/superadmin can view any assessment
    if current_user and current_user.role in ("admin", "superadmin"):
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id
        ).first()
    elif current_user:
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id
        ).first()
        if not assessment:
            # Fallback to direct id lookup
            assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    else:
        # Public / guest survey result lookup by unique assessment GUID
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")
    
    # Get category scores with category info
    cat_scores_raw = (
        db.query(CategoryScore)
        .filter(CategoryScore.assessment_id == assessment_id)
        .all()
    )
    
    cat_scores = []
    for cs in cat_scores_raw:
        cat = db.query(QuestionCategory).get(cs.category_id)
        cat_scores.append(CategoryScoreResponse(
            id=cs.id,
            category_id=cs.category_id,
            category_name=cat.name if cat else "",
            category_icon=cat.icon if cat else "",
            category_color=cat.color if cat else "",
            score_obtained=cs.score_obtained,
            max_score=cs.max_score,
            percentage=cs.percentage,
            risk_level=cs.risk_level,
        ))
    
    # Get recommendations
    recs = get_recommendations_for_assessment(db, assessment_id)
    rec_responses = [RecommendationResponse(**r) for r in recs]
    
    result = AssessmentDetail.model_validate(assessment)
    result.category_scores = cat_scores
    result.recommendations = rec_responses
    
    return result


@router.delete("/{assessment_id}")
def delete_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.user_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")
    
    db.delete(assessment)
    db.commit()
    return {"status": "ok"}


@router.put("/{assessment_id}/archive")
def archive_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.user_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")
    
    assessment.status = "archived"
    db.commit()
    return {"status": "ok"}


# ======================== REALTIME DEFICIENCY MITIGATION & MAP SYNC ========================

class MitigationItemUpdate(BaseModel):
    id: int
    resolved: bool
    notes: Optional[str] = None
    resolved_at: Optional[str] = None


class MitigationUpdateRequest(BaseModel):
    items: List[MitigationItemUpdate]


def _build_default_mitigation_data(assessment: Assessment, db: Session) -> dict:
    """Build initial deficiency checklist from AI analysis and assessment answers."""
    items = []
    idx = 0

    # 1. Try to extract from AI recommendations / weaknesses
    if assessment.ai_analysis:
        try:
            ai = json.loads(assessment.ai_analysis)
            gemini = ai.get("gemini_38") or ai
            recs = gemini.get("detailed_recommendations", [])
            for r in recs:
                p = (r.get("priority") or "medium").lower()
                weight = 4 if p == "urgent" else 3 if p == "high" else 2 if p == "medium" else 1
                items.append({
                    "id": idx,
                    "title": r.get("title", f"Hạng mục kiến nghị {idx+1}"),
                    "description": r.get("description", ""),
                    "priority": p,
                    "deadline": r.get("deadline", "Khắc phục ngay trong 24h - 48h" if p == "urgent" else "30 ngày"),
                    "category": "Khuyến cáo kỹ thuật",
                    "weight_score": weight,
                    "resolved": False,
                    "notes": "",
                    "resolved_at": None,
                    "legal_basis": r.get("legal_basis", "Quy định an toàn PCCC"),
                })
                idx += 1
        except Exception:
            pass

    # 2. Fallback to database recommendations from risky answers if AI didn't provide enough items
    if len(items) < 3:
        db_recs = get_recommendations_for_assessment(db, assessment.id)
        for r in db_recs:
            # avoid duplicating titles
            if any(it["title"] == r["recommendation_text"][:80] for it in items):
                continue
            p = (r.get("priority") or "medium").lower()
            weight = 4 if p == "urgent" else 3 if p == "high" else 2 if p == "medium" else 1
            items.append({
                "id": idx,
                "title": r.get("recommendation_text", f"Hạng mục {idx+1}")[:100],
                "description": f"Câu hỏi: {r.get('question_text') or ''}. Yêu cầu xử lý dứt điểm.",
                "priority": p,
                "deadline": "Khắc phục ngay trong 24h - 48h" if p == "urgent" else f"{r.get('deadline_days', 30)} ngày",
                "category": r.get("category_name", "An toàn PCCC"),
                "weight_score": weight,
                "resolved": False,
                "notes": "",
                "resolved_at": None,
                "legal_basis": r.get("legal_reference", "Luật PCCC số 55/2024/QH15"),
            })
            idx += 1

    return {
        "initial_risk_percentage": assessment.risk_percentage,
        "initial_risk_level": assessment.risk_level,
        "initial_total_score": assessment.total_score,
        "current_risk_percentage": assessment.risk_percentage,
        "current_risk_level": assessment.risk_level,
        "current_total_score": assessment.total_score,
        "items": items,
        "ai_feedback": "Hệ thống đã lập danh mục các tồn tại, vi phạm an toàn PCCC cần khắc phục. Cơ sở sau khi xử lý xong ngoài thực tế hãy tích chọn để cập nhật mức nguy cơ theo thời gian thực và đồng bộ lên Bản đồ Rủi ro PCCC Bắc Ninh.",
        "last_updated": datetime.utcnow().isoformat(),
    }


@router.get("/{assessment_id}/mitigation")
def get_assessment_mitigation(
    assessment_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Lấy danh mục các tồn tại cần khắc phục và trạng thái nguy cơ realtime."""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")

    if assessment.mitigation_data:
        try:
            return json.loads(assessment.mitigation_data)
        except Exception:
            pass

    # Initialize default
    data = _build_default_mitigation_data(assessment, db)
    assessment.mitigation_data = json.dumps(data, ensure_ascii=False)
    db.commit()
    return data


@router.post("/{assessment_id}/mitigation")
def update_assessment_mitigation(
    assessment_id: str,
    payload: MitigationUpdateRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Cập nhật tiến độ khắc phục từng hạng mục, tự động tính lại điểm nguy cơ và cập nhật Bản đồ Admin Realtime."""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")

    # Load current data
    if assessment.mitigation_data:
        try:
            data = json.loads(assessment.mitigation_data)
        except Exception:
            data = _build_default_mitigation_data(assessment, db)
    else:
        data = _build_default_mitigation_data(assessment, db)

    items = data.get("items", [])
    updates_map = {u.id: u for u in payload.items}

    now_iso = datetime.utcnow().isoformat()
    for it in items:
        it_id = it.get("id")
        if it_id in updates_map:
            u = updates_map[it_id]
            was_resolved = it.get("resolved", False)
            it["resolved"] = u.resolved
            if u.notes is not None:
                it["notes"] = u.notes
            if u.resolved and not was_resolved:
                it["resolved_at"] = u.resolved_at or now_iso
            elif not u.resolved:
                it["resolved_at"] = None

    # Recalculate Risk Score & Risk Percentage
    total_count = len(items)
    resolved_count = sum(1 for it in items if it.get("resolved"))
    total_weight = sum(it.get("weight_score", 1) for it in items) or 1
    resolved_weight = sum(it.get("weight_score", 1) for it in items if it.get("resolved"))

    ratio = resolved_weight / total_weight if total_weight > 0 else 0
    init_pct = float(data.get("initial_risk_percentage", assessment.risk_percentage or 50.0))
    init_score = int(data.get("initial_total_score", assessment.total_score or 30))

    if total_count == 0:
        new_risk_pct = 0.0
        new_score = 0
        new_risk_level = "low"
    elif resolved_count == total_count:
        # 100% resolved: drop to minimal baseline risk (5%)
        new_risk_pct = min(init_pct, 5.0)
        new_score = max(0, round(init_score * 0.05))
        new_risk_level = "low"
    else:
        # Proportionally reduce risk up to 80% reduction
        reduction = 0.80 * ratio
        new_risk_pct = round(max(8.0, init_pct * (1.0 - reduction)), 1)
        new_score = max(0, round(init_score * (1.0 - reduction)))
        
        # Risk thresholds
        if new_risk_pct < 25.0:
            new_risk_level = "low"
        elif new_risk_pct < 50.0:
            new_risk_level = "medium"
        elif new_risk_pct < 75.0:
            new_risk_level = "high"
        else:
            new_risk_level = "critical"

    # AI Confirmation & Guidance Note
    if total_count > 0 and resolved_count == total_count:
        ai_feedback = (
            f"Xuất sắc: Cơ sở '{assessment.facility_name}' đã hoàn thành khắc phục toàn bộ 100% ({total_count}/{total_count}) tồn tại, vi phạm an toàn PCCC. "
            f"Tỷ lệ nguy cơ cháy nổ thực tế đã hạ từ {init_pct}% xuống {new_risk_pct}% (Nguy cơ Thấp - Vùng Xanh An toàn). "
            f"Hệ thống đã tự động cập nhật chấm an toàn trên Bản đồ Rủi ro PCCC Bắc Ninh. Đề nghị cơ sở tiếp tục duy trì chế độ tự kiểm tra định kỳ theo quy định."
        )
    elif resolved_count >= total_count / 2 and resolved_count > 0:
        pct_progress = round((resolved_count / total_count) * 100)
        ai_feedback = (
            f"Ghi nhận nỗ lực tích cực: Cơ sở đã khắc phục thành công {resolved_count}/{total_count} hạng mục trọng yếu ({pct_progress}% tiến độ). "
            f"Nguy cơ cháy nổ đã giảm từ {init_pct}% xuống {new_risk_pct}%. Trạng thái an toàn trên Bản đồ Rủi ro PCCC đã được cập nhật tương ứng. "
            f"Đề nghị cơ sở khẩn trương hoàn thiện các nội dung còn lại để đưa cơ sở về trạng thái an toàn tuyệt đối."
        )
    elif resolved_count > 0:
        ai_feedback = (
            f"Cơ sở đã bắt đầu tiến trình khắc phục ({resolved_count}/{total_count} hạng mục). "
            f"Tỷ lệ nguy cơ hiện tại là {new_risk_pct}%. Lưu ý ưu tiên xử lý dứt điểm các nguy cơ trực tiếp gây cháy (hệ thống thiết bị điện, nguồn nhiệt) trong vòng 24h - 48h."
        )
    else:
        ai_feedback = (
            f"Chưa ghi nhận hạng mục nào được khắc phục. Tỷ lệ nguy cơ vẫn giữ ở mức ban đầu {init_pct}% ({new_risk_level.upper()}). "
            f"Khuyến cáo cơ sở khẩn trương rà soát và xử lý các tồn tại nguy cơ cao để đảm bảo an toàn PCCC."
        )

    # Update metadata
    data["current_risk_percentage"] = new_risk_pct
    data["current_risk_level"] = new_risk_level
    data["current_total_score"] = new_score
    data["ai_feedback"] = ai_feedback
    data["last_updated"] = now_iso
    data["items"] = items

    # Synchronize to Assessment database record (Realtime Admin Map Sync)
    assessment.risk_percentage = new_risk_pct
    assessment.risk_level = new_risk_level
    assessment.total_score = new_score
    assessment.mitigation_data = json.dumps(data, ensure_ascii=False)
    db.commit()

    return data

