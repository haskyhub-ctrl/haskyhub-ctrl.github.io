"""
AI Analysis Router
Provides AI-powered features using Gemini API:
1. Post-assessment analysis
2. AI question generation
3. AI comparison & trend analysis
4. AI chatbot (context-aware Q&A)
5. AI regional summary
6. AI risk prediction
"""
import os
import json
import asyncio
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from models import User, Assessment, AssessmentAnswer, CategoryScore, Question, QuestionOption, QuestionCategory
from middleware.auth_middleware import get_current_user, get_optional_user
from middleware.rbac import require_role
from utils.ai_prompt import build_analysis_prompt, build_fallback_analysis
from utils.ai_rules import sanitize_analysis
from utils.analysis_library import learn_from_analysis, ensure_red_flag_coverage, normalize_deadline

router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


# ======================== HELPER ========================

GEMINI_FALLBACK_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
]

# Khóa và địa chỉ 9router đọc từ biến môi trường (file backend/.env trên máy chủ), không ghi cứng trong mã nguồn.
# Dùng chung biến ROUTER_* với chatbot nếu không đặt riêng NINEROUTER_*.
NINEROUTER_BASE_URL = (os.getenv("NINEROUTER_BASE_URL") or os.getenv("ROUTER_BASE_URL") or "http://127.0.0.1:20128/v1").rstrip("/")
NINEROUTER_API_KEY = os.getenv("NINEROUTER_API_KEY") or os.getenv("ROUTER_API_KEY") or ""
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "ag/gemini-3.8-flash")


async def call_gemini(prompt: str, temperature: float = 0.3, system_prompt: str = None, timeout: float = 50.0) -> dict:
    """Call 9Router (Gemini 3.8 Flash) with fast non-streaming JSON response and robust fallback."""
    import httpx

    # 1. Prioritize 9Router VPS (ag/gemini-3.8-flash)
    if NINEROUTER_BASE_URL and NINEROUTER_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {NINEROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            sys_content = system_prompt or (
                "Bạn là chuyên gia Phòng cháy chữa cháy và Cứu nạn cứu hộ (PCCC&CNCH) hàng đầu tại Việt Nam. "
                "Hãy luôn trả về kết quả thuần định dạng JSON hợp lệ (không kèm văn bản ngoài khối JSON)."
            )
            payload = {
                "model": GEMINI_MODEL,
                "messages": [
                    {"role": "system", "content": sys_content},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "stream": False,
            }
            # connect ngắn để báo lỗi nhanh khi máy chủ AI ngừng; read dài vì bản phân tích đầy đủ mất ~60 giây
            async with httpx.AsyncClient(timeout=httpx.Timeout(timeout, connect=10.0)) as client:
                resp = await client.post(f"{NINEROUTER_BASE_URL}/chat/completions", headers=headers, json=payload)
                if resp.status_code == 200:
                    raw_text = resp.text
                    full_text = ""
                    if raw_text.startswith("data:") or "text/event-stream" in resp.headers.get("content-type", ""):
                        parts = []
                        for line in raw_text.split("\n"):
                            line = line.strip()
                            if line.startswith("data:"):
                                sub = line[5:].strip()
                                if sub == "[DONE]":
                                    break
                                try:
                                    c = json.loads(sub)
                                    delta = c.get("choices", [{}])[0].get("delta", {})
                                    if "content" in delta and delta["content"]:
                                        parts.append(delta["content"])
                                except Exception:
                                    pass
                        full_text = "".join(parts).strip()
                    else:
                        data = resp.json()
                        full_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if full_text:
                        clean = full_text.strip()
                        if "```json" in clean:
                            clean = clean.split("```json")[1].split("```")[0]
                        elif "```" in clean:
                            clean = clean.split("```")[1].split("```")[0]
                        try:
                            return json.loads(clean.strip())
                        except json.JSONDecodeError:
                            return {"raw_text": full_text, "overall_assessment": full_text}
        except Exception as e:
            print(f"[9Router Warning] Failed to call 9Router: {e}, falling back...")

    # 2. Fallback to direct Gemini API
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if api_key and not api_key.startswith("sk-"):
        primary_model = "gemini-2.5-flash"
        models_to_try = [primary_model] + [m for m in GEMINI_FALLBACK_MODELS if m != primary_model]
        for model_name in models_to_try:
            try:
                async with httpx.AsyncClient(timeout=25.0) as client:
                    resp = await client.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}",
                        json={
                            "contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {"temperature": temperature}
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
                            return {"raw_text": content}
            except Exception:
                continue

    raise ValueError("Không thể kết nối dịch vụ AI phân tích")


def get_assessment_data(assessment: Assessment, db: Session) -> dict:
    """Build assessment data dict for AI prompts."""
    cat_scores = db.query(CategoryScore).filter(
        CategoryScore.assessment_id == assessment.id
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
        AssessmentAnswer.assessment_id == assessment.id
    ).all()

    detailed_answers = []
    for ans in answers:
        q = db.query(Question).get(ans.question_id)
        opt = db.query(QuestionOption).get(ans.selected_option_id) if ans.selected_option_id else None
        detailed_answers.append({
            "question_text": q.question_text if q else "",
            "answer_text": opt.option_text if opt else "",
            "score": ans.score_obtained,
            "category": (q.category.name if q and q.category else ""),
        })

    return {
        "facility_name": assessment.facility_name,
        "facility_type": assessment.facility_type,
        "facility_address": assessment.facility_address,
        "facility_area": assessment.facility_area,
        "worker_count": assessment.worker_count,
        "total_score": assessment.total_score,
        "max_possible_score": assessment.max_possible_score,
        "risk_percentage": assessment.risk_percentage,
        "risk_level": assessment.risk_level,
        "completed_at": str(assessment.completed_at) if assessment.completed_at else None,
        "category_scores": cat_scores_data,
        "detailed_answers": detailed_answers,
    }


# ======================== 1. POST-ASSESSMENT ANALYSIS ========================

@router.post("/analyze/{assessment_id}")
async def analyze_assessment(
    assessment_id: str,
    force: bool = False,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Phân tích kết quả khảo sát bằng AI (một luồng duy nhất).

    AI không phản hồi hoặc trả về sai cấu trúc thì dùng kho tri thức phân tích (utils/analysis_library.py),
    cùng cấu trúc và giọng văn nên người dùng không thấy khác biệt.
    """
    if current_user and current_user.role in ("admin", "superadmin"):
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    else:
        q = db.query(Assessment).filter(Assessment.id == assessment_id)
        if current_user:
            q = q.filter(Assessment.user_id == current_user.id)
        assessment = q.first()
        if not assessment:
            # Fallback to direct ID match
            assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")

    # Trả ngay bản đã phân tích (đổi cấu trúc cũ hai luồng sang một luồng nếu gặp)
    if not force and assessment.ai_analysis:
        try:
            cached = flatten_analysis(json.loads(assessment.ai_analysis))
            if cached and cached.get("overall_assessment"):
                return cached
        except Exception:
            pass

    assessment_data = get_assessment_data(assessment, db)
    prompt = build_analysis_prompt(assessment_data)

    analysis = None
    try:
        res = await call_gemini(prompt, temperature=0.3, timeout=85.0)
        if isinstance(res, dict) and res.get("overall_assessment") and res.get("detailed_recommendations"):
            analysis = sanitize_analysis(res)
            for rec in analysis.get("detailed_recommendations", []):
                rec["deadline"] = normalize_deadline(rec.get("deadline"), rec.get("priority"))
            try:
                learn_from_analysis(assessment_data, analysis)   # lưu vào kho tri thức dự phòng
            except Exception as e:
                print(f"[analysis_library] Không lưu được: {e}")
            analysis = ensure_red_flag_coverage(assessment_data, analysis)
            analysis["source"] = "ai"
    except Exception as e:
        print(f"[AI analysis] Lỗi gọi AI: {e}")

    if analysis is None:
        analysis = build_fallback_analysis(assessment_data)

    assessment.ai_analysis = json.dumps(analysis, ensure_ascii=False)
    if assessment.status != "completed":
        assessment.status = "completed"
    db.commit()

    return analysis


def flatten_analysis(obj):
    """Bản cũ lưu hai luồng (gemini_38 và rag_chroma); chỉ giữ một luồng."""
    if isinstance(obj, dict) and obj.get("dual_mode"):
        base = obj.get("gemini_38") or {}
        flat = {k: obj.get(k) or base.get(k) for k in (
            "overall_assessment", "strengths", "critical_weaknesses", "detailed_recommendations",
            "daily_checklist", "improvement_plan", "legal_references")}
        flat["risk_summary"] = base.get("risk_summary", "")
        return sanitize_analysis(flat)
    return obj


# ======================== 2. AI QUESTION GENERATION ========================

class QuestionGenRequest(BaseModel):
    category_id: int
    topic: str
    count: int = 3


@router.post("/generate-questions")
async def generate_questions(
    data: QuestionGenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate fire safety assessment questions using AI."""
    require_role("admin", "superadmin")(current_user)

    category = db.query(QuestionCategory).filter(QuestionCategory.id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhóm câu hỏi")

    # Get existing questions in this category as examples
    existing = db.query(Question).filter(
        Question.category_id == data.category_id,
        Question.is_active == True
    ).limit(3).all()

    examples = ""
    if existing:
        examples = "Ví dụ các câu hỏi đã có trong nhóm này:\n"
        for q in existing:
            examples += f"  - {q.question_text}\n"

    prompt = f"""Bạn là chuyên gia PCCC tại Việt Nam. Hãy tạo {data.count} câu hỏi đánh giá nguy cơ cháy nổ cho nhóm "{category.name}" ({category.description or ''}).

Chủ đề yêu cầu: {data.topic}

{examples}

Yêu cầu:
1. Mỗi câu hỏi phải có 3-4 đáp án (A, B, C, D) với các mức nguy cơ khác nhau
2. Đáp án A luôn là phương án an toàn nhất (score=0, risk=safe)
3. Đáp án cuối (C hoặc D) là phương án nguy cơ cao nhất (score cao nhất, risk=critical)
4. Điểm số tăng dần từ A đến D (VD: 0, 1, 2, 3)
5. Câu hỏi phải cụ thể, thực tế, dễ hiểu cho chủ cơ sở
6. Viện dẫn pháp lý nếu liên quan (Luật PCCC 55/2024, QCVN 06:2022/BXD, Nghị định 105/2025/NĐ-CP)

Trả về JSON:
{{
    "questions": [
        {{
            "category_id": {data.category_id},
            "question_text": "string - nội dung câu hỏi",
            "question_type": "single",
            "facility_type": "all",
            "help_text": "string - gợi ý ngắn cho người trả lời (hoặc null)",
            "reference": "string - tham chiếu pháp lý (hoặc null)",
            "order_index": 0,
            "is_active": true,
            "options": [
                {{
                    "option_key": "A",
                    "option_text": "string - nội dung đáp án an toàn",
                    "score": 0,
                    "risk_level": "safe",
                    "order_index": 0
                }},
                {{
                    "option_key": "B",
                    "option_text": "string",
                    "score": 1,
                    "risk_level": "low",
                    "order_index": 1
                }},
                {{
                    "option_key": "C",
                    "option_text": "string",
                    "score": 2,
                    "risk_level": "high",
                    "order_index": 2
                }},
                {{
                    "option_key": "D",
                    "option_text": "string - nội dung đáp án nguy cơ cao nhất",
                    "score": 3,
                    "risk_level": "critical",
                    "order_index": 3
                }}
            ]
        }}
    ]
}}
"""

    result = await call_gemini(prompt, temperature=0.5)
    return result


# ======================== 3. AI COMPARISON & TREND ========================

class CompareRequest(BaseModel):
    assessment_ids: List[str]


@router.post("/compare-trend")
async def compare_trend(
    data: CompareRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI-powered comparison and trend analysis of multiple assessments."""
    if len(data.assessment_ids) < 2:
        raise HTTPException(status_code=400, detail="Cần ít nhất 2 đánh giá để so sánh")

    assessments_data = []
    for aid in data.assessment_ids[:5]:  # Max 5
        if current_user.role in ("admin", "superadmin"):
            assessment = db.query(Assessment).filter(Assessment.id == aid, Assessment.status == "completed").first()
        else:
            assessment = db.query(Assessment).filter(Assessment.id == aid, Assessment.user_id == current_user.id, Assessment.status == "completed").first()
        if assessment:
            assessments_data.append(get_assessment_data(assessment, db))

    if len(assessments_data) < 2:
        raise HTTPException(status_code=400, detail="Không đủ đánh giá để so sánh")

    comparisons = json.dumps(assessments_data, ensure_ascii=False, indent=2)

    prompt = f"""Bạn là chuyên gia PCCC tại Việt Nam. Hãy so sánh và phân tích xu hướng của {len(assessments_data)} đánh giá nguy cơ cháy nổ sau.

DỮ LIỆU CÁC ĐÁNH GIÁ:
{comparisons}

YÊU CẦU PHÂN TÍCH:
1. So sánh điểm tổng thể và tỷ lệ nguy cơ giữa các đánh giá
2. Chỉ ra những lĩnh vực CẢI THIỆN (điểm giảm = nguy cơ giảm)
3. Chỉ ra những lĩnh vực XẤU ĐI (điểm tăng = nguy cơ tăng)
4. Xu hướng chung: cơ sở đang an toàn hơn hay nguy hiểm hơn?
5. Đề xuất ưu tiên tiếp theo

Trả về JSON:
{{
    "summary": "string - tóm tắt xu hướng 2-3 câu",
    "trend": "improving|declining|stable",
    "improved_areas": ["string - lĩnh vực cải thiện + chi tiết"],
    "declined_areas": ["string - lĩnh vực xấu đi + chi tiết"],
    "unchanged_areas": ["string - lĩnh vực không thay đổi"],
    "score_progression": [
        {{"date": "string", "score": 0, "percentage": 0, "risk_level": "string"}}
    ],
    "priority_recommendations": ["string - đề xuất ưu tiên tiếp theo"],
    "overall_trend_detail": "string - phân tích xu hướng chi tiết 3-5 câu"
}}
"""

    result = await call_gemini(prompt, temperature=0.3)
    return result


# ======================== 4. AI CHATBOT ========================

class ChatRequest(BaseModel):
    assessment_id: Optional[str] = None
    message: str
    history: Optional[List[dict]] = None  # [{"role": "user"|"assistant", "content": "..."}]


@router.post("/chat")
async def ai_chat(
    data: ChatRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """AI chatbot for fire safety Q&A using RAG Architecture (hỗ trợ cả khách vãng lai và người đã đăng nhập)."""
    from utils.rag_search import ask_ai_chi
    from utils.chat_scope import is_in_scope, out_of_scope_response, with_disclaimer

    # Đáp án chuẩn do cán bộ duyệt được ưu tiên cao nhất
    user_email_str = getattr(current_user, "email", "Khách vãng lai") if current_user else "Khách vãng lai"
    import time as _time
    t_start = _time.time()

    try:
        from utils.kb_qa import find_approved
        hit = find_approved(db, data.message)
        if hit:
            res = with_disclaimer({
                "reply": hit.answer, "suggestions": [], "references": [], "source_type": "curated",
            }, data.message)
            _log_chat_history(data.message, hit.answer, source_type="curated", user_email=user_email_str, elapsed_seconds=_time.time() - t_start)
            return res
    except Exception as e:
        print(f"[AI Chat] Lỗi tra đáp án chuẩn: {e}")

    # Chỉ trả lời lĩnh vực PCCC và CNCH; ngoài lĩnh vực thì từ chối khéo (không gọi AI)
    if not is_in_scope(data.message, data.history):
        # Từ khóa không khớp: hỏi AI nhanh một lần, chỉ từ chối khi AI khẳng định câu hỏi ngoài phạm vi
        import asyncio as _aio
        from utils.chat_scope import classify_with_ai
        verdict = await _aio.to_thread(classify_with_ai, data.message)
        if verdict is False:
            resp = out_of_scope_response()
            _log_chat_history(data.message, resp.get("reply", ""), source_type="out_of_scope", user_email=user_email_str, elapsed_seconds=_time.time() - t_start)
            return resp

    # Câu hỏi chung đã có câu trả lời gần đây: trả ngay, không gọi AI lại
    cacheable = not data.assessment_id and not data.history
    if cacheable:
        try:
            from utils import answer_cache
            cached = answer_cache.get(data.message)
            if cached:
                _log_chat_history(data.message, cached.get("reply", ""), source_type=cached.get("source_type", "cache"), user_email=user_email_str, elapsed_seconds=_time.time() - t_start)
                return cached
        except Exception as e:
            print(f"[AI Chat] Lỗi bộ nhớ đệm: {e}")

    context = ""
    if data.assessment_id and current_user:
        if current_user.role in ("admin", "superadmin"):
            assessment = db.query(Assessment).filter(Assessment.id == data.assessment_id).first()
        else:
            assessment = db.query(Assessment).filter(Assessment.id == data.assessment_id, Assessment.user_id == current_user.id).first()

        if assessment:
            adata = get_assessment_data(assessment, db)
            context = f"""
Người dùng đang hỏi về đánh giá cháy nổ của cơ sở "{adata['facility_name']}" (Loại: {adata['facility_type']}).
Tỷ lệ nguy cơ: {adata['risk_percentage']}% ({adata['risk_level']}). Điểm: {adata['total_score']}/{adata['max_possible_score']}
"""

    # Build conversation history
    history_text = ""
    if data.history:
        for msg in data.history[-6:]:
            role = "Người dùng" if msg.get("role") == "user" else "AI"
            history_text += f"{role}: {msg.get('content', '')}\n"

    # Try RAG Gemini
    try:
        import asyncio
        result = await asyncio.to_thread(ask_ai_chi, question=data.message, history_text=history_text, context=context)
        # Bước cuối: thẩm định hiệu lực, đối chiếu văn bản hướng dẫn, thay nội dung đã hết hiệu lực
        unresolved = False
        elapsed = _time.time() - t_start
        if isinstance(result, dict) and result.get("source_type") in ("notebooklm", "docs", "web", "general") and elapsed < 55:
            from utils.answer_check import verify_answer
            # Còn trong hạn mức 90 giây của cổng truy cập: thẩm định tối đa phần thời gian còn lại
            checked = await asyncio.to_thread(verify_answer, data.message, result, max(12.0, min(30.0, 80 - elapsed)))
            result, unresolved = checked["result"], checked["unresolved"]
            if checked["fixed"]:
                print(f"[AI Chat] Đã sửa câu trả lời sau thẩm định hiệu lực: {data.message[:60]}")
        if isinstance(result, dict):
            result.pop("_doc_context", None)
        # Bot chưa có căn cứ trong kho hoặc sau thẩm định vẫn chưa đủ căn cứ: ghi lại để cán bộ bổ sung đáp án chuẩn
        if isinstance(result, dict) and (unresolved or result.get("source_type") in ("general", "web")):
            _log_hard_question(db, data.message)
        final = with_disclaimer(_finish_reply(result), data.message)
        _log_chat_history(data.message, final.get("reply", "") if isinstance(final, dict) else str(final), source_type=final.get("source_type", "docs") if isinstance(final, dict) else "docs", user_email=user_email_str, elapsed_seconds=_time.time() - t_start)
        if cacheable and not unresolved and isinstance(final, dict) and final.get("source_type") in ("notebooklm", "docs", "web", "general"):
            try:
                from utils import answer_cache
                answer_cache.put(data.message, final)
            except Exception as e:
                print(f"[AI Chat] Không lưu được bộ nhớ đệm: {e}")
        return final
    except Exception as e:
        print(f"[AI Chat RAG] Error: {e}")
        _log_hard_question(db, data.message)
        fb_res = with_disclaimer(_finish_reply(_chat_fallback(data.message)), data.message)
        _log_chat_history(data.message, fb_res.get("reply", "") if isinstance(fb_res, dict) else str(fb_res), source_type="fallback", user_email=user_email_str, elapsed_seconds=_time.time() - t_start)
        return fb_res


class ChatFeedback(BaseModel):
    message: str
    reply: Optional[str] = None
    helpful: bool


@router.post("/chat/feedback")
def chat_feedback(data: ChatFeedback, db: Session = Depends(get_db)):
    """Người dùng đánh giá câu trả lời. Đánh giá "chưa giúp được" đưa câu hỏi vào hàng chờ để cán bộ bổ sung đáp án chuẩn."""
    if not data.helpful and data.message and len(data.message) <= 1500:
        try:
            from utils import answer_cache
            answer_cache.drop(data.message)      # câu trả lời bị đánh giá chưa tốt thì không giữ trong bộ nhớ đệm
            from utils.kb_qa import log_unanswered
            log_unanswered(db, data.message, source="feedback")
        except Exception as e:
            print(f"[AI Chat] Không ghi được phản hồi: {e}")
    return {"ok": True}


@router.get("/chat/history-logs")
def get_chat_history_logs(
    limit: int = 100,
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Lấy danh sách các câu hỏi và câu trả lời AI để cán bộ theo dõi, rút kinh nghiệm."""
    from pathlib import Path
    import json
    log_file = Path(__file__).resolve().parent.parent / "data" / "chat_history.jsonl"
    if not log_file.exists():
        return []
    lines = []
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        lines.append(json.loads(line))
                    except Exception:
                        pass
        return list(reversed(lines[-limit:]))
    except Exception as e:
        print(f"[Chat History] Lỗi đọc log: {e}")
        return []


@router.get("/faq/audit")
def get_faq_audit(current_user: Optional[User] = Depends(get_optional_user)):
    """Lấy báo cáo rà soát hiệu lực định kỳ của Ngân hàng 200 câu hỏi chuẩn."""
    from utils.faq_auditor import get_latest_audit_report
    return get_latest_audit_report()


@router.post("/faq/run-audit")
def run_faq_audit(db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    """Chạy rà soát hiệu lực văn bản ngay lập tức cho toàn bộ câu hỏi chuẩn."""
    from utils.faq_auditor import audit_faq_bank
    return audit_faq_bank(db)


@router.post("/faq/seed-200")
def sync_faq_200(db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    """Nạp hoặc đồng bộ hóa lại 200 câu hỏi chuẩn PCCC 2026."""
    from utils.faq_auditor import seed_200_faqs
    return seed_200_faqs(db, force_update=True)


def _finish_reply(result):
    """Chuẩn hóa lần cuối: xưng Tôi/Trợ lý ảo, gọi bạn, giữ ký hiệu trình bày."""
    if isinstance(result, dict) and isinstance(result.get("reply"), str):
        from utils.chat_format import clean_reply
        result["reply"] = clean_reply(result["reply"])
    return result


def _log_hard_question(db, message: str) -> None:
    try:
        from utils.kb_qa import log_unanswered
        log_unanswered(db, message)
    except Exception as e:
        print(f"[AI Chat] Không ghi được câu hỏi khó: {e}")


def _log_chat_history(question: str, reply: str, source_type: str = "docs", user_email: str = "Khách vãng lai", elapsed_seconds: float = 0.0) -> None:
    """Ghi lại toàn bộ lịch sử hỏi - đáp của AI vào file JSONL để cán bộ theo dõi và rút kinh nghiệm."""
    try:
        from pathlib import Path
        import json
        from datetime import datetime
        log_dir = Path(__file__).resolve().parent.parent / "data"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "chat_history.jsonl"
        now_vn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "time": now_vn,
            "user": user_email or "Khách vãng lai",
            "question": (question or "").strip()[:2000],
            "reply": (reply or "").strip(),
            "source_type": source_type or "docs",
            "elapsed_seconds": round(elapsed_seconds, 2),
            "model": os.getenv("ROUTER_MODEL", "ag/gemini-3.8-flash-high")
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[AI Chat] Lỗi ghi nhật ký hỏi đáp: {e}")


def _chat_fallback(message: str) -> dict:
    """Built-in fallback responses when AI API is unavailable."""
    msg = message.lower()

    # Keyword-based responses: thứ tự ưu tiên từ tình huống khẩn cấp đến quy định cụ thể
    responses = [
        # --- Xử lý tình huống khẩn cấp (ưu tiên cao nhất) ---
        {
            "keywords": ["khi cháy", "phải làm gì khi", "xử lý khi cháy", "khi xảy ra cháy",
                         "khi phát hiện cháy", "bị cháy", "đang cháy", "thoát ra", "kẹt trong"],
            "reply": "🚨 XỬ LÝ KHẨN CẤP KHI XẢY RA CHÁY\n\n"
                     "BƯỚC 1: BÁO ĐỘNG NGAY\n"
                     "• Hô to \"CÓ CHÁY! CÓ CHÁY!\" để cảnh báo mọi người xung quanh\n"
                     "• Bấm chuông hoặc nút ấn báo cháy khẩn cấp gần nhất\n"
                     "• Gọi ngay 114 (Cảnh sát PCCC), nêu rõ địa chỉ cụ thể và vị trí tầng cháy\n\n"
                     "BƯỚC 2: SƠ TÁN AN TOÀN\n"
                     "• Di chuyển theo lối thoát nạn đã định\n"
                     "• Sử dụng cầu thang bộ, tuyệt đối KHÔNG dùng thang máy\n"
                     "• Dùng khăn hoặc vải ướt che kín mũi miệng, cúi thấp người khi có khói\n"
                     "• Sờ mu bàn tay lên nắm cửa trước khi mở: nếu nóng, tuyệt đối không mở và tìm lối thoát khác\n\n"
                     "BƯỚC 3: DẬP LỬA BAN ĐẦU (chỉ khi đám cháy còn nhỏ trong tầm kiểm soát)\n"
                     "• Sử dụng bình chữa cháy tại chỗ: Rút chốt, hướng vòi vào gốc lửa, bóp van và quét đều tay\n"
                     "• Nếu lửa bắt đầu lan rộng: Thoát ra ngoài ngay lập tức, không cố dập lửa\n\n"
                     "BƯỚC 4: KHI BỊ MẮC KẸT\n"
                     "• Đóng kín cửa ngăn khói tràn vào, dùng khăn ướt bịt kín các khe hở\n"
                     "• Ra ban công hoặc cửa sổ ra hiệu cho lực lượng cứu nạn cứu hộ\n"
                     "• Gọi 114 thông báo vị trí chính xác đang mắc kẹt\n\n"
                     "📜 Căn cứ: Luật PCCC và CNCH 55/2024/QH15, Điều 24 (Phương án chữa cháy và thoát nạn)",
            "suggestions": ["Cách sử dụng bình chữa cháy đúng cách?", "Số 114 gọi như thế nào?", "Cách thoát qua khói?"]
        },
        {
            "keywords": ["sử dụng bình", "dùng bình", "cách chữa cháy", "dập lửa", "phun bình"],
            "reply": "🧯 CÁCH SỬ DỤNG BÌNH CHỮA CHÁY XÁCH TAY\n\n"
                     "Quy tắc thao tác 4 bước (PASS):\n"
                     "• P (Pull - Rút): Rút chốt kẹp chì an toàn\n"
                     "• A (Aim - Nhắm): Hướng loa phun về phía GỐC LỬA, giữ cự ly 1,5 - 2m\n"
                     "• S (Squeeze - Bóp): Bóp mạnh mỏ vịt để xả chất chữa cháy\n"
                     "• S (Sweep - Quét): Quét đều tay sang hai bên mép gốc lửa\n\n"
                     "LƯU Ý KỸ THUẬT:\n"
                     "• Luôn đứng ở đầu hướng gió (ngoài trời) hoặc lưng hướng về phía cửa thoát (trong phòng)\n"
                     "• Bình bột ABC: dùng dập cháy chất rắn, lỏng, khí và thiết bị điện hạ thế\n"
                     "• Bình khí CO2: dùng cho phòng máy, thiết bị điện tử chính xác\n"
                     "• Thời gian phun liên tục của bình xách tay chỉ từ 10 đến 30 giây\n\n"
                     "📜 Căn cứ: QCVN 10:2025/BCA",
            "suggestions": ["Có mấy loại bình chữa cháy?", "Bình nào dùng cho cháy điện?", "Cách bảo quản bình chữa cháy?"]
        },
        # --- Trang bị và thiết bị ---
        {
            "keywords": ["bình chữa cháy", "bình cứu hỏa", "bcc", "bình abc", "bình co2"],
            "reply": "📋 QUY ĐỊNH VỀ BÌNH CHỮA CHÁY\n\n"
                     "ĐỊNH MỨC TRANG BỊ:\n"
                     "• Văn phòng: 1 bình ABC 4kg / 50m² sàn\n"
                     "• Nhà xưởng: 1 bình ABC 6kg / 50m² + 1 bình CO2 5kg / 100m²\n"
                     "• Kho hàng: 1 bình ABC 6kg / 30m²\n"
                     "• Nhà ở: tối thiểu 1 bình ABC 2kg/căn hộ\n\n"
                     "VỊ TRÍ LẮP ĐẶT:\n"
                     "• Treo cao 0,8 - 1,5m so với sàn\n"
                     "• Khoảng cách tối đa giữa 2 bình: 20m\n"
                     "• Không đặt sau cửa hoặc góc khuất\n\n"
                     "KIỂM TRA ĐỊNH KỲ:\n"
                     "• Hàng tháng: kiểm tra áp suất đồng hồ (kim phải ở vùng xanh)\n"
                     "• Hàng năm: kiểm định lại hoặc thay bột/khí\n"
                     "• Hết hạn sử dụng (5-10 năm): thay mới\n\n"
                     "📜 Căn cứ: QCVN 10:2025/BCA, Nghị định 105/2025/NĐ-CP",
            "suggestions": ["Cách sử dụng bình chữa cháy?", "Mua bình chữa cháy ở đâu?", "Kiểm tra bình hàng tháng thế nào?"]
        },
        {
            "keywords": ["lối thoát", "thoát nạn", "thoát hiểm", "exit", "cửa thoát"],
            "reply": "🚪 QUY ĐỊNH LỐI THOÁT NẠN\n\n"
                     "YÊU CẦU KỸ THUẬT:\n"
                     "• Chiều rộng tối thiểu: 1,2m (nhà dân dụng), 1,5m (nhà công cộng)\n"
                     "• Khoảng cách xa nhất từ bất kỳ vị trí đến lối thoát: 25-40m\n"
                     "• Cửa thoát nạn phải mở ra phía lối thoát\n\n"
                     "THIẾT BỊ BẮT BUỘC:\n"
                     "• Đèn EXIT tại mỗi lối ra (sáng 24/7)\n"
                     "• Đèn chiếu sáng sự cố (tự bật khi mất điện)\n"
                     "• Bảng chỉ dẫn thoát nạn ở mỗi tầng\n\n"
                     "NGHIÊM CẤM:\n"
                     "• Khóa cửa thoát nạn trong giờ hoạt động\n"
                     "• Để hàng hóa, xe máy cản trở lối thoát\n"
                     "• Che khuất biển chỉ dẫn EXIT\n\n"
                     "📜 Căn cứ: QCVN 06:2022/BXD (Sửa đổi 1:2023)",
            "suggestions": ["Quy định đèn EXIT?", "Sơ đồ thoát nạn cần gì?", "Xử phạt vi phạm lối thoát nạn?"]
        },
        {
            "keywords": ["điện", "dây điện", "aptomat", "ổ cắm", "rccb", "chập điện", "quá tải điện"],
            "reply": "⚡ AN TOÀN ĐIỆN: PHÒNG NGỪA CHÁY NỔ\n\n"
                     "DẤU HIỆU NGUY HIỂM CẦN XỬ LÝ NGAY:\n"
                     "• Ổ cắm nóng hoặc đổi màu khi sử dụng: ngắt nguồn ngay, gọi thợ kiểm tra\n"
                     "• Mùi khét từ bảng điện hoặc ổ cắm: nguy cơ quá nhiệt hoặc tiếp xúc kém\n"
                     "• Aptomat nhảy định kỳ: mạch điện đang bị quá tải dòng điện\n"
                     "• Dây dẫn nứt vỏ, rạn nứt lão hóa: cần thay thế ngay trong ống luồn chống cháy\n\n"
                     "QUY ĐỊNH BẮT BUỘC:\n"
                     "• Lắp thiết bị chống dòng rò RCCB 30mA cho khu vực ẩm ướt\n"
                     "• Chọn aptomat phù hợp với tiết diện dây dẫn và công suất phụ tải\n"
                     "• Nối đất bảo vệ cho vỏ thiết bị công suất lớn\n\n"
                     "NGHIÊM CẤM:\n"
                     "• Cắm nối tiếp nhiều ổ cắm trung gian\n"
                     "• Sử dụng dây dẫn không có chứng nhận tiêu chuẩn\n"
                     "• Kéo dây trần trực tiếp trên vật liệu dễ cháy\n\n"
                     "📜 Căn cứ: QCVN 25:2025/BCT và QCVN 25:2025/BKHCN",
            "suggestions": ["Dấu hiệu quá tải điện?", "Cách chọn aptomat phù hợp?", "Kiểm tra hệ thống điện định kỳ?"]
        },
        {
            "keywords": ["gas", "bếp gas", "bình gas", "rò gas", "mùi gas"],
            "reply": "🔥 AN TOÀN BẾP GAS\n\n"
                     "PHÒNG NGỪA:\n"
                     "• Lắp đầu dò rò rỉ gas và van ngắt tự động\n"
                     "• Đặt bình gas cách nguồn nhiệt tối thiểu 1,5m\n"
                     "• Kiểm tra ống dẫn gas: nếu giòn, nứt → thay ngay\n"
                     "• Tắt van bình gas sau mỗi lần dùng xong\n\n"
                     "KHI PHÁT HIỆN MÙI GAS:\n"
                     "• KHÔNG bật/tắt điện, không dùng lửa\n"
                     "• Tắt van bình gas ngay\n"
                     "• Mở toàn bộ cửa thông gió\n"
                     "• Thoát ra ngoài, gọi 114 nếu cần\n\n"
                     "NGHIÊM CẤM:\n"
                     "• Để bình gas trong phòng ngủ hoặc kho kín\n"
                     "• Dùng bếp gas trong không gian thiếu thông gió\n\n"
                     "📜 Căn cứ: Nghị định 105/2025/NĐ-CP",
            "suggestions": ["Cách kiểm tra rò rỉ gas?", "Bếp điện an toàn hơn bếp gas?", "Van ngắt gas tự động loại nào tốt?"]
        },
        {
            "keywords": ["luật", "pháp luật", "nghị định", "thông tư", "55/2024", "văn bản pháp lý"],
            "reply": "📜 PHÁP LUẬT PCCC HIỆN HÀNH (2024-2025)\n\n"
                     "VĂN BẢN ĐANG CÓ HIỆU LỰC:\n"
                     "1. Luật PCCC và CNCH số 55/2024/QH15 (hiệu lực 01/07/2025)\n"
                     "2. Nghị định 105/2025/NĐ-CP: Hướng dẫn chi tiết Luật PCCC và CNCH\n"
                     "3. Nghị định 144/2021/NĐ-CP: Xử phạt vi phạm hành chính trong lĩnh vực PCCC và CNCH\n"
                     "4. QCVN 06:2022/BXD kèm Sửa đổi 1:2023: An toàn cháy cho nhà và công trình\n"
                     "5. QCVN 10:2025/BCA: Trang bị, bố trí phương tiện PCCC và CNCH\n"
                     "6. QCVN 25:2025/BCT: An toàn điện\n\n"
                     "VĂN BẢN ĐÃ HẾT HIỆU LỰC:\n"
                     "• Luật PCCC 2001 sửa đổi 2013 (thay bằng Luật số 55/2024/QH15)\n"
                     "• Nghị định 136/2020/NĐ-CP (thay bằng Nghị định 105/2025/NĐ-CP)\n\n"
                     "📜 Cổng tra cứu chính thức: vbpl.vn hoặc thuvienphapluat.vn",
            "suggestions": ["Luật 55/2024 có gì mới?", "Mức phạt vi phạm PCCC?", "Cơ sở nào phải có giấy phép PCCC?"]
        },
        {
            "keywords": ["huấn luyện", "tập huấn", "đào tạo pccc", "diễn tập"],
            "reply": "🎓 HUẤN LUYỆN VÀ DIỄN TẬP PCCC\n\n"
                     "QUY ĐỊNH BẮT BUỘC:\n"
                     "• Huấn luyện PCCC cho 100% nhân viên: ít nhất 1 lần/năm\n"
                     "• Diễn tập phương án chữa cháy: ít nhất 1 lần/năm\n"
                     "• Lưu biên bản huấn luyện và diễn tập\n\n"
                     "NỘI DUNG HUẤN LUYỆN:\n"
                     "• Nhận biết nguy cơ cháy nổ\n"
                     "• Quy trình báo cháy (gọi 114, bấm còi)\n"
                     "• Sử dụng bình chữa cháy, vòi chữa cháy\n"
                     "• Hướng dẫn thoát nạn, cứu người bị nạn\n\n"
                     "LIÊN HỆ PCCC BẮC NINH:\n"
                     "• Phòng Cảnh sát PCCC & CNCH tỉnh Bắc Ninh\n"
                     "• Đường dây nóng: 114\n\n"
                     "📜 Căn cứ: Luật PCCC 55/2024, Điều 24",
            "suggestions": ["Chi phí huấn luyện PCCC?", "Ai phải tham gia huấn luyện?", "Diễn tập cần chuẩn bị gì?"]
        },
        {
            "keywords": ["dấu hiệu cháy", "nhận biết cháy", "nguy cơ cháy", "nguyên nhân cháy"],
            "reply": "🔍 DẤU HIỆU NHẬN BIẾT SỚM NGUY CƠ CHÁY\n\n"
                     "HỆ THỐNG ĐIỆN:\n"
                     "• Ổ cắm nóng bất thường khi sử dụng\n"
                     "• Mùi khét từ tủ điện, công tắc\n"
                     "• Đèn nhấp nháy, tối sáng không đều\n"
                     "• Aptomat tự ngắt thường xuyên\n\n"
                     "NGUỒN NHIỆT:\n"
                     "• Mùi gas bất thường\n"
                     "• Tàn thuốc chưa tắt hẳn\n"
                     "• Thiết bị đun nấu để trên vật dễ cháy\n\n"
                     "MÔI TRƯỜNG:\n"
                     "• Vật liệu dễ cháy chất đống gần nguồn lửa/nhiệt\n"
                     "• Lối thoát bị cản trở\n"
                     "• Bình chữa cháy hết hạn hoặc thiếu\n\n"
                     "📜 Căn cứ: Nghị định 105/2025/NĐ-CP",
            "suggestions": ["Khi cháy phải làm gì?", "Cách phòng ngừa cháy điện?", "Kiểm tra định kỳ những gì?"]
        },
        {
            "keywords": ["phạt", "xử phạt", "vi phạm", "mức phạt", "tiền phạt"],
            "reply": "⚖️ MỨC PHẠT VI PHẠM QUY ĐỊNH PCCC\n\n"
                     "PHẠT HÀNH CHÍNH (Nghị định 144/2021/NĐ-CP):\n"
                     "• Không có nội quy, tiêu lệnh PCCC: 2.000.000đ - 5.000.000đ (Điều 30)\n"
                     "• Không trang bị phương tiện PCCC đầy đủ: 15.000.000đ - 25.000.000đ (Điều 44)\n"
                     "• Vi phạm quy định về thoát nạn, khóa cửa thoát hiểm: 10.000.000đ - 20.000.000đ (Điều 40)\n"
                     "• Báo cháy giả, thông tin sai sự thật: 4.000.000đ - 6.000.000đ (Điều 42)\n"
                     "• Vi phạm quy định an toàn PCCC về điện: 5.000.000đ - 10.000.000đ (Điều 35)\n\n"
                     "BIỆN PHÁP TẠM ĐÌNH CHỈ / ĐÌNH CHỈ HOẠT ĐỘNG:\n"
                     "• Cơ sở không khắc phục nguy cơ trực tiếp phát sinh cháy theo thời hạn yêu cầu sẽ bị tạm đình chỉ hoạt động theo Điều 17 Nghị định 105/2025/NĐ-CP\n"
                     "• Nếu để xảy ra cháy gây thiệt hại nghiêm trọng về người và tài sản: xem xét truy cứu trách nhiệm hình sự theo Điều 313 Bộ luật Hình sự\n\n"
                     "📜 Căn cứ: Nghị định 144/2021/NĐ-CP và Nghị định 105/2025/NĐ-CP",
            "suggestions": ["Cơ sở nào phải có giấy phép PCCC?", "Thủ tục xin giấy phép PCCC?", "Cách khắc phục vi phạm PCCC?"]
        },
    ]

    for r in responses:
        if any(kw in msg for kw in r["keywords"]):
            return {"reply": r["reply"], "suggestions": r["suggestions"], "references": []}

    # Default response
    return {
        "reply": "Cảm ơn câu hỏi của bạn! Tôi là trợ lý ảo hỗ trợ giải đáp pháp luật và TTHC về PCCC.\n\nHiện tại tôi có thể tư vấn các vấn đề về PCCC như:\n• ⚡ An toàn hệ thống điện\n• 🔥 Phòng cháy bếp gas, nguồn nhiệt\n• 🧯 Bình chữa cháy và thiết bị PCCC\n• 🚪 Lối thoát nạn\n• 📜 Pháp luật PCCC 2024-2025\n• 🎓 Huấn luyện và diễn tập PCCC\n• 🔍 Dấu hiệu nhận biết nguy cơ cháy\n\nHãy đặt câu hỏi cụ thể hơn để tôi tư vấn chi tiết cho bạn nhé!",
        "suggestions": ["Dấu hiệu nào cho thấy hệ thống điện sắp gây cháy?", "Quy định bình chữa cháy?", "Luật PCCC 55/2024 có gì mới?"],
        "references": []
    }


# ======================== 5. AI REGIONAL SUMMARY ========================

class RegionalRequest(BaseModel):
    province: Optional[str] = None
    facility_type: Optional[str] = None
    limit: Optional[int] = None


@router.post("/regional-summary")
async def regional_summary(
    data: RegionalRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI-powered regional/aggregate analysis of assessments."""
    require_role("admin", "superadmin")(current_user)

    query = db.query(Assessment).filter(Assessment.status == "completed")

    if data.province:
        # Join with User to filter by province
        query = query.join(User).filter(User.province.ilike(f"%{data.province}%"))
    if data.facility_type:
        query = query.filter(Assessment.facility_type == data.facility_type)

    if data.limit and data.limit > 0:
        assessments = query.order_by(Assessment.completed_at.desc()).limit(data.limit).all()
    else:
        assessments = query.order_by(Assessment.completed_at.desc()).all()

    if not assessments:
        raise HTTPException(status_code=404, detail="Không có đánh giá nào phù hợp")

    FACILITY_TYPE_LABELS = {
        "industrial": "Sản xuất công nghiệp",
        "warehouse": "Kho hàng",
        "mixed_residence": "Nhà ở kết hợp kinh doanh",
        "hospitality": "Nhà hàng, khách sạn",
        "medical_education": "Bệnh viện, trường học",
        "fuel_gas": "Xăng dầu, khí gas",
        "transport": "Giao thông",
        "residential": "Khu dân cư",
        "construction": "Xây dựng",
        "office": "Văn phòng làm việc",
        "laboratory": "Phòng thí nghiệm",
        "agriculture": "Nông nghiệp"
    }

    # Build summary data
    summary_data = []
    for a in assessments:
        ft_vn = FACILITY_TYPE_LABELS.get(a.facility_type, a.facility_type)
        summary_data.append({
            "facility_name": a.facility_name,
            "facility_type": ft_vn,
            "risk_percentage": a.risk_percentage,
            "risk_level": a.risk_level,
            "total_score": a.total_score,
            "max_possible_score": a.max_possible_score,
            "completed_at": str(a.completed_at) if a.completed_at else None,
        })

    prompt = f"""Bạn là chuyên gia phân tích rủi ro. Dựa vào dữ liệu khảo sát và đánh giá an toàn PCCC, hãy phân tích tổng hợp {len(summary_data)} đánh giá nguy cơ cháy nổ sau. YÊU CẦU BẮT BUỘC: Bạn CHỈ ĐƯỢC phân tích sâu vào nhóm các cơ sở có nguy cơ ở mức "Rất cao" và "Cao". Tuyệt đối không phân tích miên man về các nhóm điểm thấp hơn.

{f"Khu vực: {data.province}" if data.province else "Toàn bộ khu vực"}
{f"Loại cơ sở: {FACILITY_TYPE_LABELS.get(data.facility_type, data.facility_type)}" if data.facility_type else "Tất cả loại cơ sở"}

DỮ LIỆU CÁC CƠ SỞ:
{json.dumps(summary_data, ensure_ascii=False, indent=2)}

Vui lòng trả về báo cáo phân tích chính xác theo từng gạch đầu dòng dưới đây, điền số liệu thực tế dựa trên dữ liệu hiện có:

Trả về JSON chính xác theo cấu trúc sau (Tiếng Việt):
{{
    "overview": "string - tóm tắt ngắn gọn báo cáo (1-2 câu).",
    "total_assessed": {len(summary_data)},
    "risk_distribution": {{
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }},
    "avg_risk_percentage": 0.0,
    "high_risk_analysis": [
        "Loại hình có nhiều cơ sở có nguy cơ 'rất cao' nhất: [Tên loại hình], gồm [Số lượng] cơ sở. (Hãy phân tích ngắn gọn lý do cốt lõi/vi phạm phổ biến nhất khiến loại hình này rơi vào mức cực kỳ nguy hiểm).",
        "Loại hình có nhiều cơ sở có nguy cơ 'cao' nhất: [Tên loại hình], gồm [Số lượng] cơ sở. (Chỉ ra nguyên nhân chính và nguy cơ tiềm ẩn).",
        "Phân tích chi tiết tổn thất tiềm năng: Nếu xảy ra sự cố cháy nổ đối với các cơ sở thuộc 2 nhóm trên, hậu quả về người và tài sản sẽ ở mức độ nào dựa trên đặc thù hoạt động của chúng? (Chỉ ra 1-2 điểm chí mạng)."
    ],
    "specific_recommendations": [
        "Tổ chức ngay các chuyên đề kiểm tra đột xuất, rà soát chéo (quy mô nhỏ, tập trung) giao nhiệm vụ cụ thể cho từng đội để 'đánh trúng, đánh đúng' vào đúng 2 loại hình có nguy cơ rất cao và cao nêu trên.",
        "Tăng cường tần suất phối hợp diễn tập phương án chữa cháy, cứu nạn cứu hộ có nhiều lực lượng tham gia tại các cơ sở trọng điểm này.",
        "Áp dụng biện pháp mạnh (như tạm đình chỉ, đình chỉ hoạt động) đối với các cơ sở có lỗi vi phạm nghiêm trọng kéo dài, đồng thời công khai danh sách trên thông tin đại chúng.",
        "Mời chủ cơ sở của nhóm nguy cơ Rất Cao và Cao lên làm việc trực tiếp, ký cam kết và đặt ra thời hạn chót để khắc phục triệt để các tồn tại."
    ],
    "trend_observation": "string - nhận xét xu hướng"
}}
"""

    # Prevent AI hallucination by calculating exact numbers beforehand
    actual_risk_dist = {"safe": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    actual_avg = 0
    if len(assessments) > 0:
        for a in assessments:
            if a.risk_level in actual_risk_dist:
                actual_risk_dist[a.risk_level] += 1
        actual_avg = sum(a.risk_percentage for a in assessments) / len(assessments)

    result = await call_gemini(prompt, temperature=0.3)
    
    if isinstance(result, dict):
        result["total_assessed"] = len(assessments)
        result["risk_distribution"] = actual_risk_dist
        result["avg_risk_percentage"] = round(actual_avg, 1)

    return result


# ======================== 6. AI RISK PREDICTION ========================

class PredictionRequest(BaseModel):
    user_id: Optional[str] = None  # Predict for specific user, or current user
    facility_name: Optional[str] = None


@router.post("/predict-risk")
async def predict_risk(
    data: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict future risk trends based on historical assessments."""
    target_user_id = current_user.id
    if data.user_id and current_user.role in ("admin", "superadmin"):
        target_user_id = data.user_id

    # Get historical assessments
    assessments = db.query(Assessment).filter(
        Assessment.user_id == target_user_id,
        Assessment.status == "completed"
    ).order_by(Assessment.completed_at.asc()).all()

    if not assessments:
        raise HTTPException(status_code=404, detail="Chưa có đánh giá nào để dự đoán")

    history = []
    for a in assessments:
        cat_scores = db.query(CategoryScore).filter(CategoryScore.assessment_id == a.id).all()
        scores_detail = []
        for cs in cat_scores:
            cat = db.query(QuestionCategory).get(cs.category_id)
            scores_detail.append({
                "category": cat.name if cat else "",
                "percentage": cs.percentage,
                "risk_level": cs.risk_level,
            })

        history.append({
            "facility_name": a.facility_name,
            "date": str(a.completed_at) if a.completed_at else str(a.created_at),
            "risk_percentage": a.risk_percentage,
            "risk_level": a.risk_level,
            "category_scores": scores_detail,
        })

    prompt = f"""Bạn là chuyên gia phân tích dữ liệu PCCC. Hãy dự đoán xu hướng nguy cơ cháy nổ dựa trên {len(history)} đánh giá lịch sử.

DỮ LIỆU LỊCH SỬ (từ cũ đến mới):
{json.dumps(history, ensure_ascii=False, indent=2)}

YÊU CẦU:
1. Phân tích xu hướng theo thời gian
2. Dự đoán mức nguy cơ trong 3-6 tháng tới
3. Chỉ ra lĩnh vực cần ưu tiên cải thiện
4. Đánh giá hiệu quả các biện pháp đã thực hiện (nếu có cải thiện)

Trả về JSON:
{{
    "current_risk": "string - mức nguy cơ hiện tại",
    "predicted_risk_3m": "string - dự đoán sau 3 tháng nếu không cải thiện",
    "predicted_risk_6m": "string - dự đoán sau 6 tháng nếu không cải thiện",
    "trend": "improving|declining|stable",
    "trend_detail": "string - phân tích xu hướng chi tiết 3-5 câu",
    "risk_factors": [
        {{
            "factor": "string - yếu tố nguy cơ",
            "trend": "improving|declining|stable",
            "urgency": "urgent|high|medium|low"
        }}
    ],
    "improvement_effectiveness": "string - đánh giá hiệu quả biện pháp đã thực hiện",
    "priority_actions": ["string - hành động ưu tiên trong tháng tới"],
    "prediction_confidence": "high|medium|low",
    "prediction_note": "string - lưu ý về tính chính xác của dự đoán"
}}
"""

    # Try Gemini API with fallback
    try:
        result = await call_gemini(prompt, temperature=0.3)
        return result
    except Exception as e:
        print(f"[AI Predict] Gemini API error: {e}")

    # Fallback: rule-based prediction
    latest = history[-1] if history else {}
    risk_pct = latest.get("risk_percentage", 50)
    risk_lvl = latest.get("risk_level", "medium")

    # Determine trend from history
    trend = "stable"
    if len(history) >= 2:
        first_pct = history[0].get("risk_percentage", 50)
        if risk_pct < first_pct - 5:
            trend = "improving"
        elif risk_pct > first_pct + 5:
            trend = "declining"

    # Find worst categories
    worst_cats = sorted(latest.get("category_scores", []), key=lambda c: c.get("percentage", 0), reverse=True)
    risk_factors = []
    for cat in worst_cats[:5]:
        urgency = "urgent" if cat.get("percentage", 0) >= 60 else "high" if cat.get("percentage", 0) >= 40 else "medium"
        risk_factors.append({
            "factor": cat.get("category", ""),
            "trend": "stable",
            "urgency": urgency
        })

    predicted_3m = "Cao" if risk_pct > 50 else "Trung bình" if risk_pct > 30 else "Thấp"
    predicted_6m = "Rất cao" if risk_pct > 60 else "Cao" if risk_pct > 40 else "Trung bình"

    return {
        "current_risk": f"{risk_lvl.upper()} ({risk_pct}%)",
        "predicted_risk_3m": f"{predicted_3m}: Nếu không cải thiện, nguy cơ có thể tăng thêm 5-10%",
        "predicted_risk_6m": f"{predicted_6m}: Cần hành động khẩn cấp nếu chưa khắc phục",
        "trend": trend,
        "trend_detail": f"Dựa trên {len(history)} lần đánh giá, tỷ lệ nguy cơ hiện tại là {risk_pct}% (mức {risk_lvl}). {'Xu hướng đang cải thiện so với lần đầu.' if trend == 'improving' else 'Xu hướng đang xấu đi, cần hành động ngay.' if trend == 'declining' else 'Tình trạng chưa thay đổi đáng kể, cần tiếp tục cải thiện.'}",
        "risk_factors": risk_factors,
        "improvement_effectiveness": "Chưa đủ dữ liệu để đánh giá hiệu quả. Cần ít nhất 2 đánh giá cách nhau 30 ngày.",
        "priority_actions": [
            "Kiểm tra hệ thống điện toàn bộ cơ sở",
            "Bổ sung bình chữa cháy theo quy định",
            "Thông thoáng lối thoát nạn",
            "Tổ chức tập huấn PCCC cho nhân viên",
            "Lập kế hoạch khắc phục các điểm yếu nghiêm trọng nhất"
        ],
        "prediction_confidence": "medium",
        "prediction_note": "Dự đoán dựa trên phân tích thống kê từ dữ liệu đánh giá. Kết quả chính xác hơn khi có nhiều đánh giá định kỳ."
    }


# ======================== ADMIN: RELOAD DOCS ========================

@router.post("/reload-docs")
async def reload_legal_docs(
    current_user: User = Depends(get_current_user)
):
    """Admin endpoint: xóa cache tài liệu pháp lý để nạp lại từ docs/ folder.
    Gọi sau khi thêm/sửa tài liệu mà không muốn restart server."""
    require_role("admin", "superadmin")(current_user)
    import legal_knowledge
    legal_knowledge._legal_context_cache = None
    context = legal_knowledge.get_legal_context_for_chat()
    char_count = len(context)
    return {"status": "ok", "message": f"Đã nạp lại tài liệu pháp lý ({char_count:,} ký tự)"}
