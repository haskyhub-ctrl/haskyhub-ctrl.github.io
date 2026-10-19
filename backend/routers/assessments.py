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
from utils.scoring import score_assessment, calculate_risk_level, is_key_category

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
    # Bản đồ rủi ro chỉ dành cho cán bộ quản trị
    if not current_user or current_user.role not in ("admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Bản đồ rủi ro chỉ dành cho cán bộ quản lý")
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


PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
PRIORITY_DEADLINE = {
    "urgent": "Khắc phục ngay (trong 24h - 48h)",
    "high": "Trong 15 ngày",
    "medium": "Trong 30 ngày",
    "low": "Trong 60 ngày",
}
MITIGATION_MIN_SCORE = 2  # Câu trả lời từ 2 điểm trở lên được đưa vào danh mục khắc phục


def _build_default_mitigation_data(assessment: Assessment, db: Session, initial: Optional[dict] = None) -> dict:
    """Lập danh mục khắc phục từ các câu trả lời có nguy cơ.

    Mỗi hạng mục gắn với một câu hỏi gốc (question_id). Khi cơ sở tích "đã khắc phục", câu hỏi đó được tính
    0 điểm và nguy cơ được tính lại bằng chính công thức chấm điểm của bài khảo sát.
    """
    initial = initial or {
        "initial_risk_percentage": assessment.risk_percentage,
        "initial_risk_level": assessment.risk_level,
        "initial_total_score": assessment.total_score,
    }
    answers = db.query(AssessmentAnswer).filter(AssessmentAnswer.assessment_id == assessment.id).all()
    items = []
    for ans in answers:
        if (ans.score_obtained or 0) < MITIGATION_MIN_SCORE or not ans.selected_option_id:
            continue
        q = db.query(Question).get(ans.question_id)
        if not q:
            continue
        opt = db.query(QuestionOption).get(ans.selected_option_id)
        cat = db.query(QuestionCategory).get(q.category_id)
        rec = (
            db.query(Recommendation)
            .filter(Recommendation.question_option_id == ans.selected_option_id, Recommendation.is_active == True)
            .first()
        )
        severe = ans.score_obtained >= 3
        priority = "urgent" if severe and cat and is_key_category(cat) else "high" if severe else "medium"
        if rec and rec.priority in PRIORITY_ORDER and PRIORITY_ORDER[rec.priority] < PRIORITY_ORDER[priority]:
            priority = rec.priority
        if priority == "urgent":
            deadline = PRIORITY_DEADLINE["urgent"]
        elif rec and rec.deadline_days:
            deadline = f"Trong {rec.deadline_days} ngày"
        else:
            deadline = PRIORITY_DEADLINE[priority]
        items.append({
            "question_id": q.id,
            "title": (rec.recommendation_text if rec else f"Khắc phục: {q.question_text}")[:200],
            "description": f"Câu hỏi: {q.question_text} Hiện trạng khi khảo sát: {opt.option_text if opt else ''}",
            "priority": priority,
            "deadline": deadline,
            "category": cat.name if cat else "",
            "score": ans.score_obtained,
            "resolved": False,
            "notes": "",
            "resolved_at": None,
            "legal_basis": (rec.legal_reference if rec and rec.legal_reference else ""),
        })
    items.sort(key=lambda it: (PRIORITY_ORDER.get(it["priority"], 9), -it["score"]))
    for i, it in enumerate(items):
        it["id"] = i

    return {
        **initial,
        "current_risk_percentage": initial["initial_risk_percentage"],
        "current_risk_level": initial["initial_risk_level"],
        "current_total_score": initial["initial_total_score"],
        "items": items,
        "linked_to_questions": True,
        "history": [],
        "ai_feedback_source": "template",
        "ai_feedback": "Hệ thống đã lập danh mục các tồn tại, nguy cơ về an toàn PCCC cần khắc phục theo câu trả lời khảo sát. Cơ sở xử lý xong ngoài thực tế thì tích chọn và ghi chú cách đã khắc phục, hệ thống sẽ tính lại mức nguy cơ.",
        "last_updated": datetime.utcnow().isoformat(),
    }


@router.get("/{assessment_id}/mitigation")
def get_assessment_mitigation(
    assessment_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Lấy danh mục các tồn tại cần khắc phục và trạng thái nguy cơ hiện tại."""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")

    if assessment.mitigation_data:
        try:
            data = json.loads(assessment.mitigation_data)
            # Danh mục kiểu cũ (lập từ khuyến cáo AI, không gắn câu hỏi) mà chưa tích mục nào thì lập lại
            no_progress = not any(it.get("resolved") for it in data.get("items", []))
            if not data.get("linked_to_questions") and no_progress:
                initial = {k: data[k] for k in ("initial_risk_percentage", "initial_risk_level", "initial_total_score") if k in data}
                data = _build_default_mitigation_data(assessment, db, initial if len(initial) == 3 else None)
                assessment.mitigation_data = json.dumps(data, ensure_ascii=False)
                db.commit()
            return data
        except Exception:
            pass

    data = _build_default_mitigation_data(assessment, db)
    assessment.mitigation_data = json.dumps(data, ensure_ascii=False)
    db.commit()
    return data


async def _ai_mitigation_feedback(assessment: Assessment, items: list, init_pct: float, new_pct: float) -> Optional[str]:
    """Nhờ AI nhận xét tiến độ khắc phục. Trả về None nếu AI không phản hồi."""
    import asyncio
    from routers.ai_analysis import call_gemini

    done = [f"- {it.get('title')}" + (f" (ghi chú: {it.get('notes')})" if it.get("notes") else "")
            for it in items if it.get("resolved")]
    todo = [f"- [{it.get('priority', 'medium')}] {it.get('title')}" for it in items if not it.get("resolved")]
    prompt = f"""Cơ sở: {assessment.facility_name} ({assessment.facility_type or 'chưa rõ loại hình'}).
Tỷ lệ nguy cơ khi khảo sát: {init_pct}%. Tỷ lệ nguy cơ tính lại sau khắc phục: {new_pct}%.

Các hạng mục cơ sở báo đã khắc phục ({len(done)}):
{chr(10).join(done) or '- Chưa có'}

Các hạng mục chưa khắc phục ({len(todo)}):
{chr(10).join(todo) or '- Không còn'}

Hãy viết nhận xét ngắn (3-5 câu) gửi chủ cơ sở về tiến độ khắc phục: ghi nhận phần đã làm, chỉ rõ 1-3 việc cần ưu tiên tiếp theo (nguy cơ điện, nguồn lửa/nhiệt phải làm trước), nhắc giữ lại bằng chứng khắc phục.
Văn phong hành chính, khách quan, không dùng dấu gạch ngang dài, không nêu chi phí, không bịa số hiệu văn bản pháp luật.
Trả về JSON: {{"advice": "nội dung nhận xét"}}"""
    try:
        res = await asyncio.wait_for(call_gemini(prompt, temperature=0.3), timeout=40)
        advice = (res.get("advice") or res.get("overall_assessment") or "").strip()
        return advice or None
    except Exception as e:
        print(f"[Mitigation AI] {e}")
        return None


@router.post("/{assessment_id}/mitigation")
async def update_assessment_mitigation(
    assessment_id: str,
    payload: MitigationUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cập nhật tiến độ khắc phục từng hạng mục, tự động tính lại điểm nguy cơ và cập nhật Bản đồ Admin Realtime."""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")
    # Chỉ chủ hồ sơ hoặc cán bộ quản trị mới được cập nhật tiến độ
    if assessment.user_id != current_user.id and current_user.role not in ("admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật tiến độ khắc phục của hồ sơ này")

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

    # Tính lại nguy cơ
    total_count = len(items)
    resolved_count = sum(1 for it in items if it.get("resolved"))
    init_pct = float(data.get("initial_risk_percentage", assessment.risk_percentage or 0))
    init_score = int(data.get("initial_total_score", assessment.total_score or 0))

    if data.get("linked_to_questions"):
        # Câu hỏi đã khắc phục tính 0 điểm, chấm lại bằng đúng công thức của bài khảo sát
        resolved_qids = {it["question_id"] for it in items if it.get("resolved") and it.get("question_id") is not None}
        _, totals = score_assessment(db, assessment, resolved_qids)
        new_risk_pct = totals["risk_percentage"]
        new_risk_level = totals["risk_level"]
        new_score = totals["total_score"]
    else:
        # Danh mục kiểu cũ đã có tiến độ: giữ cách tính tỷ lệ cũ, dùng thang mức chung
        total_weight = sum(it.get("weight_score", 1) for it in items) or 1
        resolved_weight = sum(it.get("weight_score", 1) for it in items if it.get("resolved"))
        reduction = 0.80 * (resolved_weight / total_weight)
        new_risk_pct = round(max(0.0, init_pct * (1.0 - reduction)), 1)
        new_score = max(0, round(init_score * (1.0 - reduction)))
        new_risk_level = calculate_risk_level(new_risk_pct)

    level_vi = {"low": "Nguy cơ Thấp", "medium": "Nguy cơ Trung bình", "high": "Nguy cơ Cao", "critical": "Nguy cơ Rất cao"}.get(new_risk_level, new_risk_level)

    # AI Confirmation & Guidance Note
    if total_count > 0 and resolved_count == total_count:
        ai_feedback = (
            f"Xuất sắc: Cơ sở '{assessment.facility_name}' đã hoàn thành khắc phục toàn bộ 100% ({total_count}/{total_count}) tồn tại, nguy cơ về an toàn PCCC. "
            f"Tỷ lệ nguy cơ đã giảm từ {init_pct}% xuống {new_risk_pct}% ({level_vi}). "
            f"Kết quả đã được cập nhật tới cơ quan quản lý. Đề nghị cơ sở tiếp tục duy trì chế độ tự kiểm tra định kỳ theo quy định."
        )
    elif resolved_count >= total_count / 2 and resolved_count > 0:
        pct_progress = round((resolved_count / total_count) * 100)
        ai_feedback = (
            f"Ghi nhận nỗ lực tích cực: Cơ sở đã khắc phục thành công {resolved_count}/{total_count} hạng mục trọng yếu ({pct_progress}% tiến độ). "
            f"Nguy cơ cháy nổ đã giảm từ {init_pct}% xuống {new_risk_pct}% ({level_vi}). "
            f"Đề nghị cơ sở khẩn trương hoàn thiện các nội dung còn lại để đưa cơ sở về trạng thái an toàn tuyệt đối."
        )
    elif resolved_count > 0:
        ai_feedback = (
            f"Cơ sở đã bắt đầu tiến trình khắc phục ({resolved_count}/{total_count} hạng mục). "
            f"Tỷ lệ nguy cơ hiện tại là {new_risk_pct}%. Lưu ý ưu tiên xử lý dứt điểm các nguy cơ trực tiếp gây cháy (hệ thống thiết bị điện, nguồn nhiệt) trong vòng 24h - 48h."
        )
    else:
        ai_feedback = (
            f"Chưa ghi nhận hạng mục nào được khắc phục. Tỷ lệ nguy cơ vẫn giữ ở mức ban đầu {init_pct}% ({level_vi}). "
            f"Khuyến cáo cơ sở khẩn trương rà soát và xử lý các tồn tại nguy cơ cao để đảm bảo an toàn PCCC."
        )

    # AI nhận xét tiến độ; nếu AI không phản hồi thì dùng nhận xét soạn sẵn ở trên
    ai_advice = await _ai_mitigation_feedback(assessment, items, init_pct, new_risk_pct)
    data["ai_feedback_source"] = "ai" if ai_advice else "template"
    if ai_advice:
        ai_feedback = ai_advice

    # Lưu lịch sử mỗi lần cập nhật để theo dõi diễn biến nguy cơ
    history = data.get("history") or []
    history.append({
        "at": now_iso,
        "risk_percentage": new_risk_pct,
        "risk_level": new_risk_level,
        "resolved": resolved_count,
        "total": total_count,
        "by": current_user.full_name,
    })
    data["history"] = history[-50:]

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

