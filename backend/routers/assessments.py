from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db
from models import (
    User, Assessment, AssessmentAnswer, CategoryScore,
    Question, QuestionOption, QuestionCategory, Recommendation
)
from schemas import AssessmentResponse, AssessmentDetail, CategoryScoreResponse, RecommendationResponse
from middleware.auth_middleware import get_current_user
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
    current_user: User = Depends(get_current_user),
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
            user = db.query(User).filter(User.id == a.user_id).first()
            lat = a.latitude if a.latitude is not None else (user.latitude if user else None)
            lng = a.longitude if a.longitude is not None else (user.longitude if user else None)
            if lat is None or lng is None:
                continue
                
            assessed_user_ids.add(a.user_id)
            
            is_own = a.user_id == current_user.id
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
            })

    # 2. Imported facilities (users with coordinates) that have no assessment
    if not risk_level or risk_level == "unassessed":
        facility_users = db.query(User).filter(
            User.latitude.isnot(None),
            User.longitude.isnot(None),
            User.facility_code.isnot(None),
        ).all()
        for u in facility_users:
            if u.id in assessed_user_ids:
                continue
                
            is_own = u.id == current_user.id
            results.append({
                "id": u.id if is_own else "hidden",
                "facility_name": u.full_name if is_own else "Cơ sở chưa đánh giá",
                "facility_type": u.facility_types,
                "facility_address": f"{u.ward or ''}, {u.province or ''}".strip(", ") if is_own else "***",
                "latitude": u.latitude,
                "longitude": u.longitude,
                "risk_level": "unassessed",
                "risk_percentage": 0,
                "total_score": 0,
                "max_possible_score": 0,
                "completed_at": None,
                "user_name": u.full_name if is_own else "***",
                "organization": (u.organization or u.full_name) if is_own else "***",
                "source": "facility",
            })

    return results


@router.get("/{assessment_id}", response_model=AssessmentDetail)
def get_assessment_detail(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Admin/superadmin can view any assessment
    if current_user.role in ("admin", "superadmin"):
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id
        ).first()
    else:
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id
        ).first()
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
