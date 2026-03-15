import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Assessment, AssessmentAnswer, CategoryScore, Question, QuestionOption, QuestionCategory
from middleware.auth_middleware import get_current_user
from utils.ai_prompt import build_analysis_prompt, build_fallback_analysis

router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


@router.post("/analyze/{assessment_id}")
async def analyze_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run AI analysis on a completed assessment."""
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.user_id == current_user.id,
        Assessment.status == "completed"
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá hoàn thành")
    
    # Build assessment data
    cat_scores = db.query(CategoryScore).filter(
        CategoryScore.assessment_id == assessment_id
    ).all()
    
    cat_scores_data = []
    for cs in cat_scores:
        cat = db.query(QuestionCategory).get(cs.category_id)
        cat_scores_data.append({
            "category_name": cat.name if cat else "",
            "score_obtained": cs.score_obtained,
            "max_score": cs.max_score,
            "percentage": cs.percentage,
            "risk_level": cs.risk_level,
        })
    
    answers = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == assessment_id
    ).all()
    
    detailed_answers = []
    for ans in answers:
        q = db.query(Question).get(ans.question_id)
        opt = db.query(QuestionOption).get(ans.selected_option_id) if ans.selected_option_id else None
        detailed_answers.append({
            "question_text": q.question_text if q else "",
            "answer_text": opt.option_text if opt else "",
            "score": ans.score_obtained,
        })
    
    assessment_data = {
        "facility_name": assessment.facility_name,
        "facility_type": assessment.facility_type,
        "facility_address": assessment.facility_address,
        "facility_area": assessment.facility_area,
        "worker_count": assessment.worker_count,
        "total_score": assessment.total_score,
        "max_possible_score": assessment.max_possible_score,
        "risk_percentage": assessment.risk_percentage,
        "risk_level": assessment.risk_level,
        "category_scores": cat_scores_data,
        "detailed_answers": detailed_answers,
    }
    
    analysis = None
    
    # Try OpenAI
    if OPENAI_API_KEY:
        try:
            import httpx
            prompt = build_analysis_prompt(assessment_data)
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3,
                    },
                    timeout=60.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    # Try to parse JSON from response
                    try:
                        # Remove markdown code fences if present
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0]
                        elif "```" in content:
                            content = content.split("```")[1].split("```")[0]
                        analysis = json.loads(content)
                    except json.JSONDecodeError:
                        analysis = {"overall_assessment": content, "source": "openai_raw"}
        except Exception as e:
            pass
    
    # Try Gemini
    if not analysis and GEMINI_API_KEY:
        try:
            import httpx
            prompt = build_analysis_prompt(assessment_data)
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.3}
                    },
                    timeout=60.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    try:
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0]
                        elif "```" in content:
                            content = content.split("```")[1].split("```")[0]
                        analysis = json.loads(content)
                    except json.JSONDecodeError:
                        analysis = {"overall_assessment": content, "source": "gemini_raw"}
        except Exception:
            pass
    
    # Fallback to rule-based
    if not analysis:
        analysis = build_fallback_analysis(assessment_data)
        analysis["source"] = "rule_based"
    
    # Save to assessment
    assessment.ai_analysis = json.dumps(analysis, ensure_ascii=False)
    db.commit()
    
    return analysis
