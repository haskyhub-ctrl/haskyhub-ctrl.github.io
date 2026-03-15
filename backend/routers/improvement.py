"""
Improvement Plan Router — Manage improvement action plans from assessments.
Close the loop: assess → plan → improve → re-assess.
"""
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import (
    User, Assessment, ImprovementPlan, ImprovementTask,
    Recommendation, AssessmentAnswer, QuestionOption
)
from middleware.auth_middleware import get_current_user
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/api/improvement", tags=["Improvement Plans"])


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    evidence_file: Optional[str] = None


@router.post("/generate/{assessment_id}")
def generate_improvement_plan(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Auto-generate an improvement plan from assessment recommendations."""
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.user_id == current_user.id,
        Assessment.status == "completed",
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")

    # Check if plan already exists
    existing = db.query(ImprovementPlan).filter(
        ImprovementPlan.assessment_id == assessment_id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Kế hoạch cải thiện đã tồn tại cho đánh giá này",
        )

    # Get recommendations from risky answers
    answers = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == assessment_id,
    ).all()

    tasks_data = []
    for ans in answers:
        if ans.selected_option_id:
            option = db.query(QuestionOption).get(ans.selected_option_id)
            if option and option.score >= 2:
                # Get recommendations for this option
                recs = db.query(Recommendation).filter(
                    Recommendation.question_option_id == option.id,
                    Recommendation.is_active == True,
                ).all()
                for rec in recs:
                    tasks_data.append({
                        "title": rec.recommendation_text[:300],
                        "description": f"Căn cứ pháp lý: {rec.legal_reference}" if rec.legal_reference else None,
                        "priority": rec.priority,
                        "deadline_days": rec.deadline_days,
                    })

    if not tasks_data:
        raise HTTPException(
            status_code=400,
            detail="Không có khuyến cáo nào cần cải thiện",
        )

    # Create plan
    plan = ImprovementPlan(
        assessment_id=assessment_id,
        user_id=current_user.id,
        title=f"Kế hoạch cải thiện - {assessment.facility_name}",
        total_tasks=len(tasks_data),
    )
    db.add(plan)
    db.flush()

    # Create tasks
    for td in tasks_data:
        task = ImprovementTask(
            plan_id=plan.id,
            title=td["title"],
            description=td.get("description"),
            priority=td["priority"],
            deadline_days=td["deadline_days"],
        )
        db.add(task)

    db.commit()
    db.refresh(plan)

    return _plan_to_dict(plan, db)


@router.get("/")
def list_improvement_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List user's improvement plans."""
    plans = (
        db.query(ImprovementPlan)
        .filter(ImprovementPlan.user_id == current_user.id)
        .order_by(ImprovementPlan.created_at.desc())
        .all()
    )

    return [_plan_to_dict(p, db) for p in plans]


@router.get("/{plan_id}")
def get_improvement_plan(
    plan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed improvement plan with tasks."""
    plan = db.query(ImprovementPlan).filter(
        ImprovementPlan.id == plan_id,
        ImprovementPlan.user_id == current_user.id,
    ).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Không tìm thấy kế hoạch")

    result = _plan_to_dict(plan, db)

    # Include full task details
    tasks = (
        db.query(ImprovementTask)
        .filter(ImprovementTask.plan_id == plan_id)
        .order_by(
            ImprovementTask.priority.desc(),
            ImprovementTask.created_at,
        )
        .all()
    )

    result["tasks"] = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "status": t.status,
            "deadline_days": t.deadline_days,
            "evidence_file": t.evidence_file,
            "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in tasks
    ]

    return result


@router.put("/task/{task_id}")
def update_task(
    task_id: int,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task's status or evidence."""
    task = db.query(ImprovementTask).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhiệm vụ")

    plan = db.query(ImprovementPlan).filter(
        ImprovementPlan.id == task.plan_id,
        ImprovementPlan.user_id == current_user.id,
    ).first()
    if not plan:
        raise HTTPException(status_code=403, detail="Không có quyền")

    if data.status:
        task.status = data.status
        if data.status == "completed":
            task.completed_at = datetime.utcnow()

    if data.evidence_file is not None:
        task.evidence_file = data.evidence_file

    db.flush()

    # Recalculate plan progress
    all_tasks = db.query(ImprovementTask).filter(
        ImprovementTask.plan_id == plan.id,
    ).all()
    completed = sum(1 for t in all_tasks if t.status == "completed")
    plan.completed_tasks = completed
    plan.total_tasks = len(all_tasks)
    plan.progress = (completed / len(all_tasks) * 100) if all_tasks else 0

    if completed == len(all_tasks) and all_tasks:
        plan.status = "completed"

    db.commit()

    return {"status": "ok", "progress": plan.progress}


def _plan_to_dict(plan: ImprovementPlan, db: Session) -> dict:
    """Convert plan to a response dictionary."""
    assessment = db.query(Assessment).get(plan.assessment_id)
    return {
        "id": plan.id,
        "assessment_id": plan.assessment_id,
        "facility_name": assessment.facility_name if assessment else "",
        "title": plan.title,
        "status": plan.status,
        "total_tasks": plan.total_tasks,
        "completed_tasks": plan.completed_tasks,
        "progress": plan.progress,
        "created_at": plan.created_at.isoformat() if plan.created_at else None,
        "updated_at": plan.updated_at.isoformat() if plan.updated_at else None,
    }
