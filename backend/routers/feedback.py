import os
import random
import string
import uuid
from datetime import datetime, date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc

from database import get_db
from models import Feedback, User, AdminAuditLog
from schemas import (
    FeedbackCreate, FeedbackResponse, FeedbackAdminUpdate, FeedbackStats
)
from middleware.auth_middleware import get_current_user, get_optional_user
from middleware.rbac import require_role

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

FEEDBACK_UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "feedback")
os.makedirs(FEEDBACK_UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

CATEGORIES = [
    "Góp ý chung",
    "Phản ánh vi phạm / nguy cơ PCCC",
    "Thủ tục hành chính & Pháp lý",
    "Đề xuất cải tiến tính năng",
    "Báo lỗi kỹ thuật phần mềm",
]


def generate_feedback_code():
    """Tạo mã tiếp nhận định dạng GY<YYMMDD>-<4 ký tự ngẫu nhiên> (ví dụ: GY261026-9A3F)."""
    today_str = datetime.utcnow().strftime("%y%m%d")
    rand_chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"GY{today_str}-{rand_chars}"


def log_admin_action(db: Session, admin_id: str, action: str, target_id: str = None, details: str = None, ip: str = None):
    try:
        log = AdminAuditLog(
            admin_id=admin_id,
            action=action,
            target_type="feedback",
            target_id=target_id,
            new_value=details,
            ip_address=ip,
        )
        db.add(log)
        db.commit()
    except Exception:
        pass


@router.get("/categories")
def get_feedback_categories():
    """Trả về danh mục các loại góp ý / phản ánh."""
    return CATEGORIES


@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form("Góp ý chung"),
    sender_name: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    facility_name: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Tiếp nhận thư góp ý / phản ánh từ người dân hoặc cơ sở."""
    title_clean = title.strip()
    content_clean = content.strip()
    if len(title_clean) < 3:
        raise HTTPException(status_code=400, detail="Tiêu đề góp ý phải có ít nhất 3 ký tự")
    if len(content_clean) < 5:
        raise HTTPException(status_code=400, detail="Nội dung góp ý phải có ít nhất 5 ký tự")

    attachment_url = None
    attachment_name = None

    if file and file.filename:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Định dạng tệp không được hỗ trợ. Chỉ chấp nhận: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )
        
        file_bytes = await file.read()
        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Kích thước tệp vượt quá giới hạn cho phép (tối đa 10MB)")

        unique_fname = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{ext}"
        save_path = os.path.join(FEEDBACK_UPLOAD_DIR, unique_fname)
        with open(save_path, "wb") as f_out:
            f_out.write(file_bytes)

        attachment_url = f"/uploads/feedback/{unique_fname}"
        attachment_name = file.filename

    # Sinh mã tiếp nhận duy nhất
    for _ in range(10):
        code = generate_feedback_code()
        exists = db.query(Feedback).filter(Feedback.feedback_code == code).first()
        if not exists:
            break

    client_ip = request.client.host if request.client else None

    # Tự động gắn thông tin nếu user đã đăng nhập
    user_id = None
    if current_user:
        user_id = current_user.id
        if not sender_name:
            sender_name = current_user.full_name
        if not phone:
            phone = current_user.phone
        if not email:
            email = current_user.email
        if not facility_name:
            facility_name = current_user.organization

    feedback = Feedback(
        feedback_code=code,
        sender_name=sender_name.strip() if sender_name else None,
        phone=phone.strip() if phone else None,
        email=email.strip() if email else None,
        facility_name=facility_name.strip() if facility_name else None,
        address=address.strip() if address else None,
        category=category.strip() if category else "Góp ý chung",
        title=title_clean,
        content=content_clean,
        attachment_url=attachment_url,
        attachment_name=attachment_name,
        status="pending",
        ip_address=client_ip,
        user_id=user_id,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.post("/submit-json", response_model=FeedbackResponse)
def submit_feedback_json(
    request: Request,
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Tiếp nhận góp ý qua JSON payload (khi không đính kèm tệp)."""
    title_clean = payload.title.strip()
    content_clean = payload.content.strip()
    if len(title_clean) < 3:
        raise HTTPException(status_code=400, detail="Tiêu đề góp ý phải có ít nhất 3 ký tự")
    if len(content_clean) < 5:
        raise HTTPException(status_code=400, detail="Nội dung góp ý phải có ít nhất 5 ký tự")

    for _ in range(10):
        code = generate_feedback_code()
        exists = db.query(Feedback).filter(Feedback.feedback_code == code).first()
        if not exists:
            break

    client_ip = request.client.host if request.client else None
    user_id = None
    sender_name = payload.sender_name
    phone = payload.phone
    email = payload.email
    facility_name = payload.facility_name

    if current_user:
        user_id = current_user.id
        if not sender_name:
            sender_name = current_user.full_name
        if not phone:
            phone = current_user.phone
        if not email:
            email = current_user.email
        if not facility_name:
            facility_name = current_user.organization

    feedback = Feedback(
        feedback_code=code,
        sender_name=sender_name.strip() if sender_name else None,
        phone=phone.strip() if phone else None,
        email=email.strip() if email else None,
        facility_name=facility_name.strip() if facility_name else None,
        address=payload.address.strip() if payload.address else None,
        category=payload.category.strip() if payload.category else "Góp ý chung",
        title=title_clean,
        content=content_clean,
        attachment_url=payload.attachment_url,
        attachment_name=payload.attachment_name,
        status="pending",
        ip_address=client_ip,
        user_id=user_id,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/track/{query}")
def track_feedback(query: str, db: Session = Depends(get_db)):
    """Tra cứu trạng thái và phản hồi của thư góp ý theo Mã tiếp nhận hoặc Số điện thoại."""
    query_clean = query.strip()
    if not query_clean:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp mã tiếp nhận hoặc số điện thoại")

    # Thử tìm theo mã tiếp nhận
    feedbacks = db.query(Feedback).filter(
        or_(
            func.lower(Feedback.feedback_code) == query_clean.lower(),
            Feedback.phone == query_clean
        )
    ).order_by(desc(Feedback.created_at)).all()

    if not feedbacks:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy góp ý nào với thông tin '{query_clean}'. Vui lòng kiểm tra lại mã tiếp nhận hoặc SĐT."
        )

    return [
        {
            "feedback_code": fb.feedback_code,
            "category": fb.category,
            "title": fb.title,
            "content": fb.content,
            "attachment_url": fb.attachment_url,
            "attachment_name": fb.attachment_name,
            "status": fb.status,
            "admin_response": fb.admin_response,
            "responder_name": fb.responder_name,
            "responded_at": fb.responded_at.strftime("%H:%M %d/%m/%Y") if fb.responded_at else None,
            "created_at": fb.created_at.strftime("%H:%M %d/%m/%Y") if fb.created_at else None,
        }
        for fb in feedbacks
    ]


# ======================== ADMIN ENDPOINTS ========================

@router.get("/admin/stats", response_model=FeedbackStats)
def get_admin_feedback_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Thống kê tổng quan hòm thư góp ý dành cho Quản trị viên."""
    require_role("admin", "superadmin")(current_user)

    today_start = datetime.combine(date.today(), datetime.min.time())
    total = db.query(func.count(Feedback.id)).scalar() or 0
    pending = db.query(func.count(Feedback.id)).filter(Feedback.status == "pending").scalar() or 0
    processing = db.query(func.count(Feedback.id)).filter(Feedback.status == "processing").scalar() or 0
    resolved = db.query(func.count(Feedback.id)).filter(Feedback.status == "resolved").scalar() or 0
    rejected = db.query(func.count(Feedback.id)).filter(Feedback.status == "rejected").scalar() or 0
    today = db.query(func.count(Feedback.id)).filter(Feedback.created_at >= today_start).scalar() or 0

    return {
        "total": total,
        "pending": pending,
        "processing": processing,
        "resolved": resolved,
        "rejected": rejected,
        "today": today,
    }


@router.get("/admin/list")
def get_admin_feedbacks(
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Danh sách các thư góp ý kèm bộ lọc và phân trang."""
    require_role("admin", "superadmin")(current_user)

    q = db.query(Feedback)

    if status and status != "all":
        q = q.filter(Feedback.status == status)

    if category and category != "all":
        q = q.filter(Feedback.category == category)

    if search:
        s = f"%{search.strip()}%"
        q = q.filter(
            or_(
                Feedback.feedback_code.ilike(s),
                Feedback.title.ilike(s),
                Feedback.content.ilike(s),
                Feedback.sender_name.ilike(s),
                Feedback.phone.ilike(s),
                Feedback.facility_name.ilike(s),
                Feedback.address.ilike(s),
            )
        )

    total = q.count()
    items = q.order_by(desc(Feedback.created_at)).offset((page - 1) * limit).limit(limit).all()

    return {
        "items": [
            {
                "id": item.id,
                "feedback_code": item.feedback_code,
                "sender_name": item.sender_name,
                "phone": item.phone,
                "email": item.email,
                "facility_name": item.facility_name,
                "address": item.address,
                "category": item.category,
                "title": item.title,
                "content": item.content,
                "attachment_url": item.attachment_url,
                "attachment_name": item.attachment_name,
                "status": item.status,
                "admin_response": item.admin_response,
                "responder_name": item.responder_name,
                "responded_at": item.responded_at.isoformat() if item.responded_at else None,
                "created_at": item.created_at.isoformat() if item.created_at else None,
            }
            for item in items
        ],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit if total > 0 else 1,
    }


@router.get("/admin/{feedback_id}", response_model=FeedbackResponse)
def get_feedback_detail(
    feedback_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xem chi tiết một thư góp ý."""
    require_role("admin", "superadmin")(current_user)
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Không tìm thấy thư góp ý")
    return fb


@router.put("/admin/{feedback_id}/respond", response_model=FeedbackResponse)
def respond_feedback(
    feedback_id: str,
    payload: FeedbackAdminUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cán bộ Quản trị cập nhật trạng thái và nhập câu trả lời / phản hồi."""
    require_role("admin", "superadmin")(current_user)

    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Không tìm thấy thư góp ý")

    valid_statuses = {"pending", "processing", "resolved", "rejected"}
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Trạng thái xử lý không hợp lệ")

    old_status = fb.status
    fb.status = payload.status
    if payload.admin_response is not None:
        fb.admin_response = payload.admin_response.strip()

    responder = payload.responder_name or current_user.full_name or "Cán bộ quản trị"
    fb.responder_name = responder
    fb.responded_at = datetime.utcnow()

    db.commit()
    db.refresh(fb)

    # Ghi log hoạt động admin
    client_ip = request.client.host if request.client else None
    log_admin_action(
        db,
        admin_id=current_user.id,
        action=f"respond_feedback_{payload.status}",
        target_id=feedback_id,
        details=f"Đổi từ {old_status} sang {payload.status}. Phản hồi: {payload.admin_response[:100] if payload.admin_response else ''}",
        ip=client_ip
    )

    return fb


@router.delete("/admin/{feedback_id}")
def delete_feedback(
    feedback_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xóa một thư góp ý."""
    require_role("admin", "superadmin")(current_user)

    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Không tìm thấy thư góp ý")

    # Xóa file đính kèm nếu có
    if fb.attachment_url and fb.attachment_url.startswith("/uploads/feedback/"):
        fname = os.path.basename(fb.attachment_url)
        fpath = os.path.join(FEEDBACK_UPLOAD_DIR, fname)
        if os.path.exists(fpath):
            try:
                os.remove(fpath)
            except Exception:
                pass

    db.delete(fb)
    db.commit()

    client_ip = request.client.host if request.client else None
    log_admin_action(
        db,
        admin_id=current_user.id,
        action="delete_feedback",
        target_id=feedback_id,
        details=f"Xóa thư góp ý mã {fb.feedback_code}",
        ip=client_ip
    )

    return {"message": "Đã xóa thư góp ý thành công"}
