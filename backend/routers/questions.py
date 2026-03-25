from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models import User, Question, QuestionOption, QuestionCategory, Recommendation
from schemas import (
    QuestionCreate, QuestionUpdate, QuestionResponse,
    CategoryCreate, CategoryUpdate, CategoryResponse
)
from middleware.auth_middleware import get_current_user
from middleware.rbac import require_role

router = APIRouter(prefix="/api/questions", tags=["Questions"])


# ======================== CATEGORIES ========================

@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(QuestionCategory).order_by(QuestionCategory.order_index).all()
    return [CategoryResponse.model_validate(c) for c in cats]


@router.post("/categories", response_model=CategoryResponse)
def create_category(
    data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    cat = QuestionCategory(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return CategoryResponse.model_validate(cat)


@router.put("/categories/{cat_id}", response_model=CategoryResponse)
def update_category(
    cat_id: int,
    data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    cat = db.query(QuestionCategory).filter(QuestionCategory.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhóm câu hỏi")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, key, value)
    db.commit()
    db.refresh(cat)
    return CategoryResponse.model_validate(cat)


@router.delete("/categories/{cat_id}")
def delete_category(
    cat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    cat = db.query(QuestionCategory).filter(QuestionCategory.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhóm câu hỏi")
    cat.is_active = False
    db.commit()
    return {"status": "ok"}


# ======================== QUESTIONS ========================

@router.get("/", response_model=List[QuestionResponse])
def list_questions(
    category_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question).options(joinedload(Question.options))
    if category_id:
        query = query.filter(Question.category_id == category_id)
    questions = query.order_by(Question.order_index).all()
    return [QuestionResponse.model_validate(q) for q in questions]


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).options(joinedload(Question.options)).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")
    return QuestionResponse.model_validate(q)


@router.post("/", response_model=QuestionResponse)
def create_question(
    data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    
    q = Question(
        category_id=data.category_id,
        question_text=data.question_text,
        question_type=data.question_type,
        facility_type=data.facility_type,
        is_conditional=data.is_conditional,
        condition_question_id=data.condition_question_id,
        condition_answer=data.condition_answer,
        help_text=data.help_text,
        reference=data.reference,
        order_index=data.order_index,
        is_active=data.is_active,
        created_by=current_user.id,
    )
    db.add(q)
    db.flush()
    
    for opt_data in data.options:
        opt = QuestionOption(
            question_id=q.id,
            **opt_data.model_dump()
        )
        db.add(opt)
    
    db.commit()
    db.refresh(q)
    return QuestionResponse.model_validate(q)


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    data: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    q = db.query(Question).options(joinedload(Question.options)).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")
    
    update_data = data.model_dump(exclude_unset=True, exclude={"options"})
    for key, value in update_data.items():
        setattr(q, key, value)
    
    # Update options in-place to avoid FK constraint violations
    if data.options is not None:
        existing_opts = {opt.option_key: opt for opt in q.options}
        incoming_keys = set()
        
        for i, opt_data in enumerate(data.options):
            od = opt_data.model_dump()
            key = od.get("option_key", "")
            incoming_keys.add(key)
            
            if key in existing_opts:
                # Update existing option in-place
                existing = existing_opts[key]
                existing.option_text = od.get("option_text", existing.option_text)
                existing.score = od.get("score", existing.score)
                existing.risk_level = od.get("risk_level", existing.risk_level)
                existing.order_index = od.get("order_index", i)
            else:
                # Add new option
                new_opt = QuestionOption(question_id=question_id, **od)
                db.add(new_opt)
        
        # Remove options no longer in the list (only if not referenced by answers)
        from models import AssessmentAnswer
        for key, opt in existing_opts.items():
            if key not in incoming_keys:
                has_refs = db.query(AssessmentAnswer).filter(
                    AssessmentAnswer.selected_option_id == opt.id
                ).first()
                if not has_refs:
                    db.delete(opt)
                # If referenced, keep it but it won't appear in new response
    
    db.commit()
    db.refresh(q)
    return QuestionResponse.model_validate(q)


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")
    q.is_active = False
    db.commit()
    return {"status": "ok"}
