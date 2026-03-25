from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, subqueryload
from typing import List
from database import get_db
from models import (
    User, QuestionCategory, Question, QuestionOption,
    Assessment, AssessmentAnswer, CategoryScore
)
from schemas import (
    AssessmentStart, AnswerSubmit, BulkAnswerSubmit,
    CategoryWithQuestions, AssessmentResponse
)
from middleware.auth_middleware import get_current_user
from utils.scoring import calculate_category_scores, calculate_total_score, calculate_risk_level

router = APIRouter(prefix="/api/survey", tags=["Survey"])


@router.get("/categories")
def get_survey_categories(facility_type: str = None, db: Session = Depends(get_db)):
    """Get all active categories with their questions and options.
    If facility_type is provided (comma-separated), only return common questions
    and questions matching ANY of the specified facility types.
    """
    # Parse comma-separated facility types
    selected_types = []
    if facility_type:
        selected_types = [t.strip() for t in facility_type.split(",") if t.strip()]
    
    # Query categories
    categories = (
        db.query(QuestionCategory)
        .filter(QuestionCategory.is_active == True)
        .order_by(QuestionCategory.order_index)
        .all()
    )
    
    # Query ALL active questions at once
    all_questions = (
        db.query(Question)
        .filter(Question.is_active == True)
        .order_by(Question.order_index)
        .all()
    )
    
    # Query ALL options at once
    all_options = (
        db.query(QuestionOption)
        .order_by(QuestionOption.order_index)
        .all()
    )
    
    # Build lookup maps
    options_by_question = {}
    for opt in all_options:
        options_by_question.setdefault(opt.question_id, []).append(opt)
    
    questions_by_category = {}
    for q in all_questions:
        questions_by_category.setdefault(q.category_id, []).append(q)
    
    total_q = sum(len(qs) for qs in questions_by_category.values())
    print(f"[DEBUG] categories={len(categories)}, questions={len(all_questions)}, options={len(all_options)}, grouped_q={total_q}")
    
    result = []
    for cat in categories:
        questions_list = []
        cat_questions = questions_by_category.get(cat.id, [])
        
        for q in cat_questions:
            # If facility_type specified, filter questions
            if selected_types:
                if q.facility_type and q.facility_type != "all" and q.facility_type not in selected_types:
                    continue
            
            q_options = options_by_question.get(q.id, [])
            options_list = [{
                "id": opt.id,
                "option_key": opt.option_key,
                "option_text": opt.option_text,
                "score": opt.score,
                "risk_level": opt.risk_level,
                "order_index": opt.order_index,
            } for opt in q_options]
            
            questions_list.append({
                "id": q.id,
                "category_id": q.category_id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "facility_type": q.facility_type,
                "is_conditional": q.is_conditional,
                "condition_question_id": q.condition_question_id,
                "condition_answer": q.condition_answer,
                "help_text": q.help_text,
                "reference": q.reference,
                "order_index": q.order_index,
                "is_active": q.is_active,
                "created_at": q.created_at.isoformat() if q.created_at else None,
                "options": options_list,
            })
        
        # Skip empty categories
        if not questions_list:
            continue
        
        result.append({
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "max_score": cat.max_score,
            "weight": cat.weight,
            "order_index": cat.order_index,
            "icon": cat.icon,
            "color": cat.color,
            "is_active": cat.is_active,
            "created_at": cat.created_at.isoformat() if cat.created_at else None,
            "questions": questions_list,
        })
    
    return result


@router.post("/start", response_model=AssessmentResponse)
def start_assessment(
    data: AssessmentStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new assessment session."""
    assessment = Assessment(
        user_id=current_user.id,
        facility_name=data.facility_name,
        facility_type=data.facility_type,
        facility_address=data.facility_address,
        facility_area=data.facility_area,
        worker_count=data.worker_count,
        latitude=data.latitude,
        longitude=data.longitude,
        status="in_progress",
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return AssessmentResponse.model_validate(assessment)


@router.post("/answer")
def submit_answer(
    data: AnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a single answer."""
    assessment = db.query(Assessment).filter(
        Assessment.id == data.assessment_id,
        Assessment.user_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên đánh giá")
    
    option = db.query(QuestionOption).filter(QuestionOption.id == data.selected_option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Đáp án không hợp lệ")
    
    # Upsert answer
    existing = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == data.assessment_id,
        AssessmentAnswer.question_id == data.question_id
    ).first()
    
    if existing:
        existing.selected_option_id = data.selected_option_id
        existing.score_obtained = option.score
    else:
        answer = AssessmentAnswer(
            assessment_id=data.assessment_id,
            question_id=data.question_id,
            selected_option_id=data.selected_option_id,
            score_obtained=option.score,
        )
        db.add(answer)
    
    db.commit()
    return {"status": "ok", "score": option.score}


@router.post("/submit-all")
def submit_all_answers(
    data: BulkAnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit all answers at once."""
    assessment = db.query(Assessment).filter(
        Assessment.id == data.assessment_id,
        Assessment.user_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên đánh giá")
    
    # Delete existing answers 
    db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == data.assessment_id
    ).delete()
    
    for ans in data.answers:
        option = db.query(QuestionOption).filter(QuestionOption.id == ans.selected_option_id).first()
        score = option.score if option else 0
        answer = AssessmentAnswer(
            assessment_id=data.assessment_id,
            question_id=ans.question_id,
            selected_option_id=ans.selected_option_id,
            score_obtained=score,
        )
        db.add(answer)
    
    db.commit()
    return {"status": "ok", "answers_count": len(data.answers)}


@router.post("/complete/{assessment_id}", response_model=AssessmentResponse)
def complete_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete an assessment and calculate final scores.
    Only counts questions that were actually answered AND match the facility's types.
    """
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.user_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên đánh giá")
    
    # Get answers
    answers = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == assessment_id
    ).all()
    
    if not answers:
        raise HTTPException(status_code=400, detail="Chưa có câu trả lời nào")
    
    # Parse facility types (comma-separated)
    selected_types = []
    if assessment.facility_type:
        selected_types = [t.strip() for t in assessment.facility_type.split(",") if t.strip()]
    
    # Get answered question IDs
    answered_question_ids = {a.question_id for a in answers}
    
    # Get categories and questions
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
    
    # CRITICAL FIX: Only include questions that match the facility's types
    # AND were actually answered
    questions_by_category = {}
    for q in questions:
        # Check if question matches facility type
        type_match = (
            not q.facility_type
            or q.facility_type == "all"
            or (selected_types and q.facility_type in selected_types)
        )
        # Only include if type matches AND was answered  
        if type_match and q.id in answered_question_ids:
            questions_by_category.setdefault(q.category_id, []).append(q)
    
    # Calculate category scores
    cat_scores = calculate_category_scores(answers, questions_by_category, categories)
    
    # Delete old category scores
    db.query(CategoryScore).filter(CategoryScore.assessment_id == assessment_id).delete()
    
    # Save category scores
    for cs in cat_scores:
        db_cs = CategoryScore(
            assessment_id=assessment_id,
            category_id=cs["category_id"],
            score_obtained=cs["score_obtained"],
            max_score=cs["max_score"],
            percentage=cs["percentage"],
            risk_level=cs["risk_level"],
        )
        db.add(db_cs)
    
    # Calculate total score
    totals = calculate_total_score(cat_scores)
    
    assessment.total_score = totals["total_score"]
    assessment.max_possible_score = totals["max_possible_score"]
    assessment.risk_percentage = totals["risk_percentage"]
    assessment.risk_level = totals["risk_level"]
    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(assessment)
    
    # Trigger notifications for high/critical risk
    if assessment.risk_level in ("high", "critical"):
        _trigger_risk_notifications(db, assessment, current_user)
    
    return AssessmentResponse.model_validate(assessment)


def _trigger_risk_notifications(db, assessment, current_user):
    """Create notifications when high/critical risk is detected."""
    try:
        from routers.notifications import create_notification
        risk_label = "Nguy cơ Cao" if assessment.risk_level == "high" else "Nguy cơ Rất cao"
        create_notification(
            db, current_user.id,
            notification_type="high_risk",
            title=f"⚠️ {risk_label}: {assessment.facility_name}",
            message=f"Đánh giá cơ sở '{assessment.facility_name}' cho thấy mức {risk_label} ({assessment.risk_percentage}%). Hãy xem khuyến cáo cải thiện ngay.",
            link=f"/result.html?id={assessment.id}",
        )
        admins = db.query(User).filter(
            User.role.in_(["admin", "superadmin"]),
            User.is_active == True,
        ).all()
        for admin_user in admins:
            if admin_user.id != current_user.id:
                create_notification(
                    db, admin_user.id,
                    notification_type="high_risk",
                    title=f"⚠️ {risk_label}: {assessment.facility_name}",
                    message=f"{current_user.full_name} vừa đánh giá '{assessment.facility_name}' - {risk_label} ({assessment.risk_percentage}%).",
                    link=f"/admin/assessments.html",
                )
    except Exception:
        pass
