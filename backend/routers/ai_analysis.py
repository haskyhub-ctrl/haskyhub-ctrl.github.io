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
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from models import User, Assessment, AssessmentAnswer, CategoryScore, Question, QuestionOption, QuestionCategory
from middleware.auth_middleware import get_current_user
from middleware.rbac import require_role
from utils.ai_prompt import build_analysis_prompt, build_fallback_analysis

router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


# ======================== HELPER ========================

async def call_gemini(prompt: str, temperature: float = 0.3) -> dict:
    """Call Gemini API and return parsed JSON response."""
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY chưa được cấu hình")

    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature}
            },
            timeout=90.0
        )
        if resp.status_code != 200:
            error_detail = resp.text[:500] if resp.text else "No response body"
            print(f"[Gemini API Error] Status: {resp.status_code}, Response: {error_detail}")
            raise HTTPException(status_code=502, detail=f"Gemini API lỗi: {resp.status_code}")

        data = resp.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"]

        # Parse JSON from response
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_text": content}


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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run AI analysis on a completed assessment."""
    # Allow admin to analyze any assessment
    if current_user.role in ("admin", "superadmin"):
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.status == "completed"
        ).first()
    else:
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id,
            Assessment.status == "completed"
        ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá hoàn thành")

    assessment_data = get_assessment_data(assessment, db)
    analysis = None

    # Try Gemini first
    if GEMINI_API_KEY:
        try:
            prompt = build_analysis_prompt(assessment_data)
            analysis = await call_gemini(prompt, temperature=0.3)
        except Exception:
            pass

    # Try OpenAI fallback
    if not analysis and OPENAI_API_KEY:
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
                    try:
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0]
                        elif "```" in content:
                            content = content.split("```")[1].split("```")[0]
                        analysis = json.loads(content)
                    except json.JSONDecodeError:
                        analysis = {"overall_assessment": content, "source": "openai_raw"}
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI chatbot for fire safety Q&A, optionally contextual to an assessment."""
    from legal_knowledge import get_legal_context_for_chat
    legal_context = get_legal_context_for_chat()

    context = ""
    if data.assessment_id:
        if current_user.role in ("admin", "superadmin"):
            assessment = db.query(Assessment).filter(Assessment.id == data.assessment_id).first()
        else:
            assessment = db.query(Assessment).filter(Assessment.id == data.assessment_id, Assessment.user_id == current_user.id).first()

        if assessment:
            adata = get_assessment_data(assessment, db)
            context = f"""
NGỮ CẢNH: Người dùng đang hỏi về đánh giá cháy nổ của cơ sở "{adata['facility_name']}"
- Loại cơ sở: {adata['facility_type']}
- Tỷ lệ nguy cơ: {adata['risk_percentage']}% ({adata['risk_level']})
- Tổng điểm: {adata['total_score']}/{adata['max_possible_score']}
"""

    # Build conversation history
    history_text = ""
    if data.history:
        for msg in data.history[-6:]:
            role = "Người dùng" if msg.get("role") == "user" else "AI"
            history_text += f"{role}: {msg.get('content', '')}\n"

    prompt = f"""Bạn là chuyên gia tư vấn Phòng cháy chữa cháy (PCCC) tại Việt Nam. Bạn CHỈ trả lời dựa trên các văn bản pháp lý và quy chuẩn đã được cung cấp bên dưới. Không bịa đặt thông tin.

=== VĂN BẢN PHÁP LÝ VÀ QUY CHUẨN ===
{legal_context}
=== HẾT VĂN BẢN PHÁP LÝ ===

{context}

{f"LỊCH SỬ HỘI THOẠI:{chr(10)}{history_text}" if history_text else ""}

CÂU HỎI CỦA NGƯỜI DÙNG: {data.message}

YÊU CẦU:
- Trả lời bằng tiếng Việt, chi tiết, dễ hiểu, thực tế
- PHẢI viện dẫn cụ thể điều khoản pháp luật từ văn bản đã cung cấp
- Nếu câu hỏi liên quan đến ngữ cảnh đánh giá, đưa ra tư vấn cụ thể cho cơ sở đó
- Nếu không tìm thấy thông tin trong văn bản, nói rõ "Thông tin này chưa có trong cơ sở dữ liệu pháp lý hiện tại" và gợi ý nguồn tra cứu
- Nếu không liên quan đến PCCC, nhẹ nhàng hướng người dùng quay lại chủ đề

Trả về JSON:
{{
    "reply": "string - câu trả lời chi tiết, có viện dẫn pháp lý cụ thể",
    "suggestions": ["string - 2-3 câu hỏi gợi ý liên quan"],
    "references": ["string - danh sách văn bản pháp lý đã viện dẫn trong câu trả lời"]
}}
"""

    # Try Gemini API
    try:
        result = await call_gemini(prompt, temperature=0.3)
        return result
    except Exception as e:
        print(f"[AI Chat] Gemini API error: {e}")

    # Fallback: built-in keyword-based responses
    return _chat_fallback(data.message)


def _chat_fallback(message: str) -> dict:
    """Built-in fallback responses when AI API is unavailable."""
    msg = message.lower()

    # Keyword-based responses
    responses = [
        {
            "keywords": ["bình chữa cháy", "bình cứu hỏa", "bcc"],
            "reply": "📋 Quy định về bình chữa cháy:\n\n• Trang bị tối thiểu 1 bình ABC 4kg cho mỗi 50m² sàn\n• Treo ở độ cao 0,8 - 1,5 mét, nơi dễ tiếp cận\n• Kiểm tra áp suất bằng đồng hồ hàng tháng\n• Thay mới khi hết hạn (thường 5-10 năm)\n• Nhấn nút TEST định kỳ\n\n📜 Căn cứ: QCVN 10:2025/BCA, Nghị định 105/2025/NĐ-CP",
            "suggestions": ["Cách sử dụng bình chữa cháy?", "Có mấy loại bình chữa cháy?", "Chi phí mua bình chữa cháy?"]
        },
        {
            "keywords": ["lối thoát", "thoát nạn", "thoát hiểm", "exit"],
            "reply": "🚪 Quy định lối thoát nạn:\n\n• Chiều rộng tối thiểu 1,2 mét\n• KHÔNG được khóa cửa thoát nạn trong giờ hoạt động\n• Lắp đèn EXIT và đèn chiếu sáng sự cố tại mỗi lối ra\n• Niêm yết sơ đồ thoát nạn ở mỗi tầng\n• Không để hàng hóa cản trở lối thoát\n\n📜 Căn cứ: QCVN 06:2022/BXD (Sửa đổi 1:2023)",
            "suggestions": ["Quy định đèn EXIT?", "Sơ đồ thoát nạn cần gì?", "Diễn tập thoát nạn như thế nào?"]
        },
        {
            "keywords": ["điện", "dây điện", "aptomat", "ổ cắm", "rccb", "chập"],
            "reply": "⚡ An toàn điện - phòng cháy:\n\n• Kiểm tra dây điện: nếu vỏ bọc nứt, bong tróc → thay ngay\n• Sờ ổ cắm khi đang dùng: nếu NÓNG → ngắt ngay, gọi thợ điện\n• Ngửi xem có MÙI KHÉT ở tủ điện/ổ cắm → dấu hiệu chập mạch\n• Lắp RCCB 30mA cho khu vực ẩm ướt\n• Lắp aptomat đúng dòng định mức cho từng mạch\n• KHÔNG cắm chồng ổ nối dài\n\n📜 Căn cứ: QCVN 25:2025/BCT, QCVN 25:2025/BKHCN",
            "suggestions": ["Dấu hiệu quá tải điện?", "Chi phí kiểm tra hệ thống điện?", "Cách chọn aptomat phù hợp?"]
        },
        {
            "keywords": ["gas", "bếp", "nấu ăn", "bình gas"],
            "reply": "🔥 An toàn bếp gas:\n\n• Lắp van ngắt gas tự động và đầu dò rò rỉ gas\n• Đặt bình gas xa nguồn nhiệt tối thiểu 1,5 mét\n• Kiểm tra ống dẫn gas: nếu giòn, nứt → thay ngay\n• KHÔNG bao giờ để bếp gas trong phòng ngủ hoặc kho hàng\n• Tắt van bình gas khi không sử dụng\n\n📜 Căn cứ: Nghị định 105/2025/NĐ-CP",
            "suggestions": ["Cách kiểm tra rò rỉ gas?", "Bếp điện an toàn hơn bếp gas?", "Van ngắt gas tự động giá bao nhiêu?"]
        },
        {
            "keywords": ["luật", "pháp luật", "quy định", "nghị định", "thông tư", "55/2024"],
            "reply": "📜 Pháp luật PCCC hiện hành (2024-2025):\n\n1. Luật PCCC và CNCH số 55/2024/QH15 — luật mới nhất\n2. QCVN 06:2022/BXD (Sửa đổi 1:2023) — an toàn cháy cho nhà và công trình\n3. Nghị định 105/2025/NĐ-CP — hướng dẫn chi tiết Luật PCCC\n4. QCVN 10:2025/BCA — trang bị phương tiện PCCC\n5. QCVN 25:2025/BCT — an toàn điện\n6. QCVN 25:2025/BKHCN — thiết bị điện gia đình\n\n⚠️ Các văn bản cũ (Luật PCCC 2001, NĐ 136/2020) đã hết hiệu lực.",
            "suggestions": ["Luật 55/2024 có gì mới?", "Mức phạt vi phạm PCCC?", "Cơ sở nào phải có giấy phép PCCC?"]
        },
        {
            "keywords": ["huấn luyện", "tập huấn", "đào tạo", "diễn tập"],
            "reply": "🎓 Huấn luyện PCCC:\n\n• Tổ chức huấn luyện PCCC cho 100% nhân viên ít nhất 1 lần/năm\n• Nội dung: sử dụng bình chữa cháy, quy trình báo cháy (gọi 114), thoát nạn\n• Diễn tập phương án chữa cháy ít nhất 1 lần/năm\n• Lưu biên bản huấn luyện và diễn tập\n• Liên hệ cơ quan PCCC địa phương để được hỗ trợ\n\n📜 Căn cứ: Luật PCCC 55/2024, Nghị định 105/2025/NĐ-CP",
            "suggestions": ["Chi phí huấn luyện PCCC?", "Liên hệ PCCC địa phương ở đâu?", "Thời gian diễn tập bao lâu?"]
        },
        {
            "keywords": ["cháy", "nguyên nhân", "nguy cơ", "dấu hiệu"],
            "reply": "🔍 Các dấu hiệu nhận biết sớm nguy cơ cháy:\n\n⚡ HỆ THỐNG ĐIỆN:\n• Ổ cắm nóng bất thường khi sử dụng\n• Mùi khét từ tủ điện, công tắc\n• Đèn nhấp nháy, tối sáng không đều\n• Aptomat tự ngắt thường xuyên → quá tải\n\n🔥 NGUỒN NHIỆT:\n• Mùi gas bất thường\n• Tàn thuốc chưa tắt hẳn\n• Thiết bị đun nấu bị hở\n\n⚠️ MÔI TRƯỜNG:\n• Vật liệu dễ cháy chất đống\n• Lối thoát bị cản trở\n• Bình chữa cháy hết hạn/thiếu",
            "suggestions": ["Cách xử lý khi phát hiện cháy?", "Số điện thoại báo cháy?", "Bảo hiểm cháy nổ như thế nào?"]
        },
    ]

    for r in responses:
        if any(kw in msg for kw in r["keywords"]):
            return {"reply": r["reply"], "suggestions": r["suggestions"], "references": []}

    # Default response
    return {
        "reply": "Cảm ơn câu hỏi của bạn! Tôi là trợ lý PCCC.\n\nHiện tại tôi có thể tư vấn về:\n• ⚡ An toàn hệ thống điện\n• 🔥 Phòng cháy bếp gas, nguồn nhiệt\n• 🧯 Bình chữa cháy và thiết bị PCCC\n• 🚪 Lối thoát nạn\n• 📜 Pháp luật PCCC 2024-2025\n• 🎓 Huấn luyện và diễn tập PCCC\n• 🔍 Dấu hiệu nhận biết nguy cơ cháy\n\nHãy đặt câu hỏi cụ thể hơn để tôi tư vấn chi tiết!",
        "suggestions": ["Dấu hiệu nào cho thấy hệ thống điện sắp gây cháy?", "Quy định bình chữa cháy?", "Luật PCCC 55/2024 có gì mới?"],
        "references": []
    }


# ======================== 5. AI REGIONAL SUMMARY ========================

class RegionalRequest(BaseModel):
    province: Optional[str] = None
    facility_type: Optional[str] = None
    limit: int = 50


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

    assessments = query.order_by(Assessment.completed_at.desc()).limit(data.limit).all()

    if not assessments:
        raise HTTPException(status_code=404, detail="Không có đánh giá nào phù hợp")

    # Build summary data
    summary_data = []
    for a in assessments:
        summary_data.append({
            "facility_name": a.facility_name,
            "facility_type": a.facility_type,
            "risk_percentage": a.risk_percentage,
            "risk_level": a.risk_level,
            "total_score": a.total_score,
            "max_possible_score": a.max_possible_score,
            "completed_at": str(a.completed_at) if a.completed_at else None,
        })

    prompt = f"""Bạn là chuyên gia PCCC cấp tỉnh. Hãy phân tích tổng hợp {len(summary_data)} đánh giá nguy cơ cháy nổ sau.

{f"Khu vực: {data.province}" if data.province else "Toàn bộ khu vực"}
{f"Loại cơ sở: {data.facility_type}" if data.facility_type else "Tất cả loại cơ sở"}

DỮ LIỆU:
{json.dumps(summary_data, ensure_ascii=False, indent=2)}

YÊU CẦU PHÂN TÍCH:
1. Tổng quan tình hình an toàn cháy nổ khu vực
2. Phân bố mức nguy cơ (bao nhiêu % cơ sở ở mỗi mức)
3. Loại cơ sở có nguy cơ cao nhất
4. Vấn đề phổ biến nhất
5. Khuyến nghị cho cơ quan quản lý

Trả về JSON:
{{
    "overview": "string - tổng quan 3-5 câu",
    "total_assessed": {len(summary_data)},
    "risk_distribution": {{
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }},
    "avg_risk_percentage": 0.0,
    "highest_risk_facilities": ["string - tên cơ sở nguy cơ cao nhất (top 5)"],
    "common_issues": ["string - vấn đề phổ biến"],
    "recommendations_for_authority": ["string - khuyến nghị cho cơ quan quản lý"],
    "trend_observation": "string - nhận xét xu hướng"
}}
"""

    result = await call_gemini(prompt, temperature=0.3)
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
        "predicted_risk_3m": f"{predicted_3m} — nếu không cải thiện, nguy cơ có thể tăng thêm 5-10%",
        "predicted_risk_6m": f"{predicted_6m} — cần hành động khẩn cấp nếu chưa khắc phục",
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
