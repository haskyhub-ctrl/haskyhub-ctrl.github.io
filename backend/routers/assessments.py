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


@router.get("/compare/list")
def compare_assessments(
    ids: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare multiple assessments. ids = comma-separated assessment IDs."""
    id_list = [x.strip() for x in ids.split(",") if x.strip()]
    if len(id_list) < 2:
        raise HTTPException(status_code=400, detail="Cần ít nhất 2 đánh giá để so sánh")
    
    is_admin = current_user.role in ("admin", "superadmin")
    results = []
    for aid in id_list:
        if is_admin:
            assessment = db.query(Assessment).filter(Assessment.id == aid).first()
        else:
            assessment = db.query(Assessment).filter(
                Assessment.id == aid,
                Assessment.user_id == current_user.id
            ).first()
        if not assessment:
            continue
        
        cat_scores = db.query(CategoryScore).filter(
            CategoryScore.assessment_id == aid
        ).all()
        
        cat_data = []
        for cs in cat_scores:
            cat = db.query(QuestionCategory).get(cs.category_id)
            cat_data.append({
                "category_id": cs.category_id,
                "category_name": cat.name if cat else "",
                "score_obtained": cs.score_obtained,
                "max_score": cs.max_score,
                "percentage": cs.percentage,
                "risk_level": cs.risk_level,
            })
        
        results.append({
            "assessment": AssessmentResponse.model_validate(assessment).model_dump(),
            "category_scores": cat_data,
        })
    
    return results


@router.get("/map-data")
def get_user_map_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return current user's completed assessments with coordinates for map display."""
    assessments = db.query(Assessment).filter(
        Assessment.user_id == current_user.id,
        Assessment.status == "completed",
        Assessment.latitude.isnot(None),
        Assessment.longitude.isnot(None),
    ).order_by(Assessment.created_at.desc()).all()

    return [
        {
            "id": a.id,
            "facility_name": a.facility_name,
            "facility_type": a.facility_type,
            "facility_address": a.facility_address,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "risk_level": a.risk_level,
            "risk_percentage": a.risk_percentage,
            "total_score": a.total_score,
            "max_possible_score": a.max_possible_score,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            "user_name": current_user.full_name,
            "organization": current_user.organization,
            "source": "assessment",
        }
        for a in assessments
    ]


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
