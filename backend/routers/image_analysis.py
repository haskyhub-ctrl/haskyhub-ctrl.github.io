"""
Image Analysis Router — AI Visual Fire Risk Assessment.
Upload/capture photos of facilities, Gemini Vision API identifies visible fire hazards.
"""
import os
import uuid
import json
import base64
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models import User, ImageAnalysis, Assessment
from middleware.auth_middleware import get_current_user
from utils.image_prompt import build_image_analysis_prompt, parse_vision_response

router = APIRouter(prefix="/api/image", tags=["Image Analysis"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")

# Ensure uploads directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    assessment_id: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload an image and analyze it for fire hazards using Gemini Vision API."""
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Chỉ hỗ trợ file ảnh (JPEG, PNG, WebP)",
        )

    # Read file content
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File ảnh quá lớn (tối đa 10MB)")

    # Save file
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(content)

    # Validate assessment_id if provided
    if assessment_id:
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id,
        ).first()
        if not assessment:
            assessment_id = None

    # Call Gemini Vision API
    analysis_result = None
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if api_key:
        try:
            import httpx

            image_b64 = base64.b64encode(content).decode("utf-8")
            mime_type = file.content_type or "image/jpeg"
            prompt = build_image_analysis_prompt()

            primary_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
            fallback_models = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-2.5-flash", "gemini-3.5-flash-lite"]
            models_to_try = [primary_model] + [m for m in fallback_models if m != primary_model]

            for model_name in models_to_try:
                try:
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        resp = await client.post(
                            f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}",
                            json={
                                "contents": [
                                    {
                                        "parts": [
                                            {"text": prompt},
                                            {
                                                "inline_data": {
                                                    "mime_type": mime_type,
                                                    "data": image_b64,
                                                }
                                            },
                                        ]
                                    }
                                ],
                                "generationConfig": {"temperature": 0.2},
                            },
                        )

                        if resp.status_code == 200:
                            data = resp.json()
                            raw_content = data["candidates"][0]["content"]["parts"][0]["text"]
                            analysis_result = parse_vision_response(raw_content)
                            break
                        else:
                            print(f"[Vision API] Model {model_name} HTTP {resp.status_code}")
                            if resp.status_code in (404, 429, 500, 502, 503):
                                continue
                            break
                except Exception as ex:
                    print(f"[Vision API] Model {model_name} exception: {ex}")
                    continue

        except Exception as e:
            analysis_result = {
                "hazards": [],
                "overall_risk": "unknown",
                "summary": f"Lỗi phân tích: {str(e)}",
                "safe_aspects": "",
            }

    if not analysis_result:
        analysis_result = {
            "hazards": [],
            "overall_risk": "unknown",
            "summary": "Không thể phân tích: thiếu API key Gemini",
            "safe_aspects": "",
        }

    # Save to database
    img_analysis = ImageAnalysis(
        user_id=current_user.id,
        assessment_id=assessment_id,
        image_filename=filename,
        analysis_result=json.dumps(analysis_result, ensure_ascii=False),
        overall_risk=analysis_result.get("overall_risk", "unknown"),
        hazards_count=len(analysis_result.get("hazards", [])),
    )
    db.add(img_analysis)
    db.commit()
    db.refresh(img_analysis)

    return {
        "id": img_analysis.id,
        "image_url": f"/uploads/{filename}",
        "analysis": analysis_result,
        "overall_risk": img_analysis.overall_risk,
        "hazards_count": img_analysis.hazards_count,
        "created_at": img_analysis.created_at.isoformat(),
    }


@router.get("/history")
def get_image_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's image analysis history."""
    analyses = (
        db.query(ImageAnalysis)
        .filter(ImageAnalysis.user_id == current_user.id)
        .order_by(ImageAnalysis.created_at.desc())
        .limit(50)
        .all()
    )

    results = []
    for a in analyses:
        parsed = {}
        if a.analysis_result:
            try:
                parsed = json.loads(a.analysis_result)
            except json.JSONDecodeError:
                parsed = {}

        results.append({
            "id": a.id,
            "image_url": f"/uploads/{a.image_filename}",
            "overall_risk": a.overall_risk,
            "hazards_count": a.hazards_count,
            "summary": parsed.get("summary", ""),
            "assessment_id": a.assessment_id,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        })

    return results


@router.get("/{analysis_id}")
def get_image_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed image analysis."""
    analysis = db.query(ImageAnalysis).filter(
        ImageAnalysis.id == analysis_id,
        ImageAnalysis.user_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Không tìm thấy phân tích")

    parsed = {}
    if analysis.analysis_result:
        try:
            parsed = json.loads(analysis.analysis_result)
        except json.JSONDecodeError:
            parsed = {}

    return {
        "id": analysis.id,
        "image_url": f"/uploads/{analysis.image_filename}",
        "analysis": parsed,
        "overall_risk": analysis.overall_risk,
        "hazards_count": analysis.hazards_count,
        "assessment_id": analysis.assessment_id,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
    }


@router.delete("/{analysis_id}")
def delete_image_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an image analysis."""
    analysis = db.query(ImageAnalysis).filter(
        ImageAnalysis.id == analysis_id,
        ImageAnalysis.user_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Không tìm thấy phân tích")

    # Delete file
    filepath = os.path.join(UPLOAD_DIR, analysis.image_filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.delete(analysis)
    db.commit()
    return {"status": "ok"}
