"""Recommendation engine for fire risk assessment."""

from sqlalchemy.orm import Session
from models import Recommendation, AssessmentAnswer, QuestionOption, Question, QuestionCategory


def get_recommendations_for_assessment(db: Session, assessment_id: str):
    """Get all recommendations based on selected answers.
    
    Returns recommendations sorted by priority (urgent first).
    """
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    
    answers = (
        db.query(AssessmentAnswer)
        .filter(AssessmentAnswer.assessment_id == assessment_id)
        .all()
    )
    
    recommendations = []
    for answer in answers:
        if not answer.selected_option_id:
            continue
        
        recs = (
            db.query(Recommendation)
            .filter(
                Recommendation.question_option_id == answer.selected_option_id,
                Recommendation.is_active == True
            )
            .all()
        )
        
        for rec in recs:
            option = db.query(QuestionOption).get(answer.selected_option_id)
            question = db.query(Question).get(answer.question_id)
            category = db.query(QuestionCategory).get(question.category_id) if question else None
            
            recommendations.append({
                "id": rec.id,
                "recommendation_text": rec.recommendation_text,
                "priority": rec.priority,
                "deadline_days": rec.deadline_days,
                "legal_reference": rec.legal_reference,
                "question_text": question.question_text if question else None,
                "category_name": category.name if category else None,
                "score": answer.score_obtained,
                "risk_level": option.risk_level if option else "medium",
            })
    
    # Sort by priority
    recommendations.sort(key=lambda r: priority_order.get(r["priority"], 99))
    
    return recommendations


def get_priority_label_vi(priority: str) -> str:
    """Get Vietnamese label for priority."""
    labels = {
        "urgent": "Khẩn cấp",
        "high": "Cao",
        "medium": "Trung bình",
        "low": "Thấp",
    }
    return labels.get(priority, priority)


def get_priority_color(priority: str) -> str:
    """Get color for priority level."""
    colors = {
        "urgent": "#ef4444",
        "high": "#f97316",
        "medium": "#eab308",
        "low": "#22c55e",
    }
    return colors.get(priority, "#94a3b8")
