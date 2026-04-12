import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from database import get_db
from models import User, Assessment, AdminAuditLog, QuestionCategory, Question
from schemas import (
    UserResponse, UserRoleUpdate, UserLockUpdate,
    AdminStats, AuditLogResponse, PasswordResetRequest
)
from middleware.auth_middleware import get_current_user, hash_password
from middleware.rbac import require_role


class AddUserRequest(BaseModel):
    email: str
    password: str
    full_name: str
    organization: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "user"

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def log_action(db: Session, admin_id: str, action: str, target_type: str = None,
               target_id: str = None, old_value=None, new_value=None, ip: str = None):
    log = AdminAuditLog(
        admin_id=admin_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        old_value=json.dumps(old_value) if old_value else None,
        new_value=json.dumps(new_value) if new_value else None,
        ip_address=ip,
    )
    db.add(log)
    db.commit()


@router.get("/stats", response_model=AdminStats)
def get_admin_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    total_users = db.query(func.count(User.id)).scalar()
    total_assessments = db.query(func.count(Assessment.id)).filter(
        Assessment.status == "completed"
    ).scalar()
    
    avg_risk = db.query(func.avg(Assessment.risk_percentage)).filter(
        Assessment.status == "completed"
    ).scalar() or 0
    
    high_risk = db.query(func.count(Assessment.id)).filter(
        Assessment.status == "completed",
        Assessment.risk_level.in_(["high", "critical"])
    ).scalar()
    
    month_assessments = db.query(func.count(Assessment.id)).filter(
        Assessment.created_at >= month_start
    ).scalar()
    
    month_users = db.query(func.count(User.id)).filter(
        User.created_at >= month_start
    ).scalar()
    
    return AdminStats(
        total_users=total_users,
        total_assessments=total_assessments,
        avg_risk_score=round(avg_risk, 1),
        high_risk_count=high_risk,
        assessments_this_month=month_assessments,
        new_users_this_month=month_users,
    )


@router.get("/users", response_model=List[UserResponse])
def list_users(
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    query = db.query(User)
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%")) |
            (User.organization.ilike(f"%{search}%"))
        )
    users = query.order_by(User.created_at.desc()).all()
    return [UserResponse.model_validate(u) for u in users]


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: str,
    data: UserRoleUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("superadmin")(current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    old_role = user.role
    user.role = data.role
    log_action(db, current_user.id, "change_role", "user", user_id,
               {"role": old_role}, {"role": data.role},
               request.client.host if request.client else None)
    db.commit()
    return {"status": "ok"}


@router.put("/users/{user_id}/lock")
def toggle_user_lock(
    user_id: str,
    data: UserLockUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    user.is_locked = data.is_locked
    action = "lock_user" if data.is_locked else "unlock_user"
    log_action(db, current_user.id, action, "user", user_id,
               ip=request.client.host if request.client else None)
    db.commit()
    return {"status": "ok"}


@router.put("/users/{user_id}/reset-password", response_model=dict)
def reset_user_password(
    user_id: str,
    data: PasswordResetRequest,
    current_admin: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_admin)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    user.password_hash = hash_password(data.new_password)
    user.updated_at = datetime.utcnow()
    
    log_action(db, current_admin.id, "reset_password", "user", user_id)
    db.commit()
    
    return {"message": f"Đã đặt lại mật khẩu cho người dùng {user.email}"}


@router.post("/users/add")
def add_single_user(
    data: AddUserRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a single user by admin."""
    require_role("admin", "superadmin")(current_user)

    # Check duplicate email
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Email {data.email} đã tồn tại")

    # Validate role
    if data.role not in ("user", "admin", "superadmin"):
        raise HTTPException(status_code=400, detail="Role không hợp lệ")

    new_user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        organization=data.organization or "",
        phone=data.phone or "",
        role=data.role,
    )
    db.add(new_user)
    db.flush()

    log_action(db, current_user.id, "add_user", "user", new_user.id,
               new_value={"email": data.email, "role": data.role},
               ip=request.client.host if request.client else None)
    db.commit()
    return {"status": "ok", "user_id": new_user.id, "email": data.email}


@router.get("/assessments")
def list_all_assessments(
    risk_level: Optional[str] = None,
    facility_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    query = db.query(Assessment).filter(Assessment.status == "completed")
    if risk_level:
        query = query.filter(Assessment.risk_level == risk_level)
    if facility_type:
        query = query.filter(Assessment.facility_type == facility_type)
    
    assessments = query.order_by(Assessment.created_at.desc()).all()
    results = []
    for a in assessments:
        user = db.get(User, a.user_id)
        data = {
            "id": a.id,
            "facility_name": a.facility_name,
            "facility_type": a.facility_type,
            "facility_address": a.facility_address or "",
            "total_score": a.total_score,
            "max_possible_score": a.max_possible_score,
            "risk_level": a.risk_level,
            "risk_percentage": a.risk_percentage,
            "status": a.status,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            "user_name": user.full_name if user else "N/A",
            "user_email": user.email if user else "N/A",
            "organization": user.organization if user else "N/A",
        }
        results.append(data)
    return results


@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    logs = (
        db.query(AdminAuditLog)
        .order_by(AdminAuditLog.created_at.desc())
        .limit(limit)
        .all()
    )
    results = []
    for log in logs:
        admin = db.get(User, log.admin_id)
        r = AuditLogResponse.model_validate(log)
        r.admin_name = admin.full_name if admin else "N/A"
        results.append(r)
    return results


@router.get("/reports/risk-distribution")
def risk_distribution(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    results = (
        db.query(Assessment.risk_level, func.count(Assessment.id))
        .filter(Assessment.status == "completed")
        .group_by(Assessment.risk_level)
        .all()
    )
    return {level: count for level, count in results}


@router.get("/reports/monthly-trend")
def monthly_trend(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_role("admin", "superadmin")(current_user)
    
    now = datetime.utcnow()
    months = []
    for i in range(5, -1, -1):
        d = now - timedelta(days=i * 30)
        start = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if i > 0:
            end = (start + timedelta(days=32)).replace(day=1)
        else:
            end = now
        
        count = db.query(func.count(Assessment.id)).filter(
            Assessment.created_at >= start,
            Assessment.created_at < end,
            Assessment.status == "completed"
        ).scalar()
        
        avg = db.query(func.avg(Assessment.risk_percentage)).filter(
            Assessment.created_at >= start,
            Assessment.created_at < end,
            Assessment.status == "completed"
        ).scalar()
        
        months.append({
            "month": start.strftime("%m/%Y"),
            "count": count,
            "avg_score": round(avg or 0, 1),
        })
    
    return months


@router.get("/map-data")
def get_map_data(
    risk_level: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all completed assessments + imported facilities for map display."""
    require_role("admin", "superadmin")(current_user)

    results = []
    assessed_user_ids = set()

    # 1. Completed assessments — try assessment coords first, fallback to user coords
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
            results.append({
                "id": a.id,
                "facility_name": a.facility_name,
                "facility_type": a.facility_type,
                "facility_address": a.facility_address,
                "latitude": lat,
                "longitude": lng,
                "risk_level": a.risk_level,
                "risk_percentage": a.risk_percentage,
                "total_score": a.total_score,
                "max_possible_score": a.max_possible_score,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
                "user_name": user.full_name if user else "N/A",
                "organization": user.organization if user else "N/A",
                "source": "assessment",
            })

    # 2. Imported facilities (users with coordinates) that have no assessment
    if not risk_level or risk_level == "unassessed":
        facility_users = db.query(User).filter(
            User.latitude.isnot(None),
            User.longitude.isnot(None),
            User.facility_code.isnot(None),
        ).all()
        for u in facility_users:
            if u.id in assessed_user_ids:
                continue
            results.append({
                "id": u.id,
                "facility_name": u.full_name,
                "facility_type": u.facility_types,
                "facility_address": f"{u.ward or ''}, {u.province or ''}".strip(", "),
                "latitude": u.latitude,
                "longitude": u.longitude,
                "risk_level": "unassessed",
                "risk_percentage": 0,
                "total_score": 0,
                "max_possible_score": 0,
                "completed_at": None,
                "user_name": u.full_name,
                "organization": u.organization or u.full_name,
                "source": "facility",
            })

    return results


import os
from fastapi.responses import FileResponse
from utils.backup_service import backup_db

@router.post("/manual-backup")
def trigger_manual_backup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kích hoạt sao lưu thủ công."""
    require_role("admin", "superadmin")(current_user)
    backup_file = backup_db()
    if backup_file and os.path.exists(backup_file):
        log_action(db, current_user.id, "manual_backup", "system", None)
        return {"status": "ok", "message": "Đã sao lưu thành công", "file": os.path.basename(backup_file)}
    else:
        raise HTTPException(status_code=500, detail="Sao lưu thất bại, kiểm tra log hệ thống")

@router.get("/download-backup")
def download_backup(
    file_name: str,
    current_user: User = Depends(get_current_user),
):
    """Tải xuống file sao lưu."""
    require_role("admin", "superadmin")(current_user)
    backup_path = os.path.join("./backups", file_name)
    if os.path.exists(backup_path):
        return FileResponse(backup_path, filename=file_name, media_type="application/octet-stream")
    raise HTTPException(status_code=404, detail="File backup không tồn tại")

@router.get("/backups")
def list_backups(
    current_user: User = Depends(get_current_user),
):
    """Lấy danh sách các file sao lưu hiện có."""
    require_role("admin", "superadmin")(current_user)
    backup_dir = "./backups"
    if not os.path.exists(backup_dir):
        return []
    
    files = []
    for f in os.listdir(backup_dir):
        if f.startswith("fras_backup_") and f.endswith(".db"):
            path = os.path.join(backup_dir, f)
            files.append({
                "file_name": f,
                "size_kb": round(os.path.getsize(path) / 1024, 2),
                "created_at": datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
            })
    files.sort(key=lambda x: x["created_at"], reverse=True)
    return files


# ========================================================================
# ASSESSMENT MANAGEMENT — Xóa đơn, Xóa hàng loạt, Tạo dữ liệu mẫu
# ========================================================================

# 34 tỉnh sau sáp nhập 2025 — tọa độ trung tâm
PROVINCE_COORDS = {
    "Hà Nội": (21.0285, 105.8542),
    "Hải Phòng": (20.8449, 106.6881),
    "Hồ Chí Minh": (10.7769, 106.7009),
    "Đà Nẵng": (16.0544, 108.2022),
    "Cần Thơ": (10.0452, 105.7469),
    "Bắc Ninh": (21.1861, 106.0763),
    "Quảng Ninh": (21.0064, 107.2925),
    "Vĩnh Phúc": (21.3609, 105.5474),
    "Hưng Yên": (20.6463, 106.0511),
    "Hải Dương": (20.9373, 106.3145),
    "Thái Bình": (20.4458, 106.3421),
    "Nam Định": (20.4388, 106.1621),
    "Ninh Bình": (20.2506, 105.9745),
    "Thanh Hóa": (19.8071, 105.7852),
    "Nghệ An": (19.2342, 104.9200),
    "Hà Tĩnh": (18.3559, 105.8877),
    "Quảng Bình": (17.4689, 106.6228),
    "Quảng Trị": (16.7943, 107.0916),
    "Thừa Thiên Huế": (16.4637, 107.5909),
    "Quảng Nam": (15.5394, 108.0191),
    "Quảng Ngãi": (15.1214, 108.7922),
    "Bình Định": (13.7765, 109.2236),
    "Phú Yên": (13.0882, 109.0926),
    "Khánh Hòa": (12.2388, 109.1967),
    "Ninh Thuận": (11.5645, 108.9882),
    "Bình Thuận": (11.0904, 108.0721),
    "Kon Tum": (14.3497, 108.0004),
    "Gia Lai": (13.9894, 108.0000),
    "Đắk Lắk": (12.7100, 108.2378),
    "Đắk Nông": (12.0000, 107.6900),
    "Lâm Đồng": (11.5424, 108.4272),
    "Bình Phước": (11.7512, 106.7235),
    "Tây Ninh": (11.3600, 106.1000),
    "Bình Dương": (11.1332, 106.4770),
}

FACILITY_TYPES = [
    "industrial", "warehouse", "mixed_residence", "hospitality",
    "medical_education", "fuel_gas", "transport", "residential",
    "construction", "office", "laboratory", "agriculture"
]

RISK_LEVELS = ["safe", "low", "medium", "high", "critical"]


class BulkDeleteRequest(BaseModel):
    ids: List[str]


class GenerateDemoRequest(BaseModel):
    count: int = 10
    risk_distribution: str = "random"  # random | high_focus | balanced
    province: str = "Bắc Ninh"
    facility_type: Optional[str] = None  # null = random


@router.get("/assessments")
def list_admin_assessments(
    risk_level: Optional[str] = None,
    facility_type: Optional[str] = None,
    include_demo: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Danh sách tất cả bài đánh giá cho admin (kèm thông tin user)."""
    require_role("admin", "superadmin")(current_user)
    query = db.query(Assessment).filter(Assessment.status == "completed")
    if risk_level:
        query = query.filter(Assessment.risk_level == risk_level)
    if facility_type:
        query = query.filter(Assessment.facility_type == facility_type)
    if not include_demo:
        query = query.filter(Assessment.is_demo == False)
    assessments = query.order_by(Assessment.created_at.desc()).all()
    result = []
    for a in assessments:
        user = db.query(User).filter(User.id == a.user_id).first()
        result.append({
            "id": a.id,
            "facility_name": a.facility_name,
            "facility_type": a.facility_type,
            "facility_address": a.facility_address,
            "total_score": a.total_score,
            "max_possible_score": a.max_possible_score,
            "risk_level": a.risk_level,
            "risk_percentage": a.risk_percentage,
            "is_demo": getattr(a, "is_demo", False),
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            "user_name": user.full_name if user else "N/A",
            "organization": user.organization if user else "N/A",
            "province": user.province if user else None,
            "latitude": a.latitude,
            "longitude": a.longitude,
        })
    return result


@router.delete("/assessments/demo")
def delete_all_demo_assessments(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Xóa toàn bộ dữ liệu demo (is_demo=True)."""
    require_role("admin", "superadmin")(current_user)
    demos = db.query(Assessment).filter(Assessment.is_demo == True).all()
    count = len(demos)
    for a in demos:
        db.delete(a)
    db.commit()
    log_action(db, current_user.id, "delete_all_demo", "assessment", None,
               None, {"count": count},
               request.client.host if request.client else None)
    return {"deleted": count, "message": f"Đã xóa {count} bài đánh giá demo"}


@router.delete("/assessments/bulk")
def bulk_delete_assessments(
    data: BulkDeleteRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Xóa hàng loạt bài đánh giá theo danh sách ID."""
    require_role("admin", "superadmin")(current_user)
    if not data.ids:
        raise HTTPException(status_code=400, detail="Danh sách ID không được rỗng")
    deleted = 0
    for aid in data.ids:
        a = db.query(Assessment).filter(Assessment.id == aid).first()
        if a:
            db.delete(a)
            deleted += 1
    db.commit()
    log_action(db, current_user.id, "bulk_delete_assessments", "assessment", None,
               None, {"ids": data.ids, "deleted": deleted},
               request.client.host if request.client else None)
    return {"deleted": deleted, "message": f"Đã xóa {deleted} bài đánh giá"}


@router.delete("/assessments/{assessment_id}")
def delete_assessment(
    assessment_id: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Xóa một bài đánh giá (admin có thể xóa bất kỳ)."""
    require_role("admin", "superadmin")(current_user)
    a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài đánh giá")
    facility_name = a.facility_name
    db.delete(a)
    db.commit()
    log_action(db, current_user.id, "delete_assessment", "assessment", assessment_id,
               {"facility_name": facility_name}, None,
               request.client.host if request.client else None)
    return {"deleted": True, "message": f"Đã xóa '{facility_name}'"}


@router.post("/assessments/generate")
def generate_demo_assessments(
    data: GenerateDemoRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Tạo dữ liệu mẫu (is_demo=True) để test phân tích."""
    import random
    require_role("admin", "superadmin")(current_user)

    count = max(1, min(data.count, 100))
    province = data.province if data.province in PROVINCE_COORDS else "Bắc Ninh"
    base_lat, base_lng = PROVINCE_COORDS[province]

    # Phân bổ nguy cơ
    if data.risk_distribution == "high_focus":
        weights = [2, 5, 10, 35, 25]        # safe/low/med/high/critical
    elif data.risk_distribution == "balanced":
        weights = [20, 20, 20, 20, 20]
    else:  # random
        weights = [10, 20, 30, 25, 15]

    risk_map = {
        "safe":     (0, 20),
        "low":      (20, 40),
        "medium":   (40, 60),
        "high":     (60, 80),
        "critical": (80, 100),
    }

    facility_names_map = {
        "industrial": ["Xưởng cơ khí", "Nhà máy may", "Xưởng gỗ nội thất", "Nhà máy điện tử", "Xưởng nhựa"],
        "warehouse":  ["Kho vật tư", "Kho thành phẩm", "Kho hóa chất", "Kho lạnh", "Kho ngoại quan"],
        "mixed_residence": ["Nhà ở hỗn hợp tầng 1", "Nhà phố kinh doanh", "Chung cư mini"],
        "hospitality": ["Quán ăn", "Nhà hàng", "Khách sạn", "Quán cà phê"],
        "residential": ["Khu dân cư liền kề", "Chung cư", "Nhà trọ công nhân", "Biệt thự khu dân cư"],
        "office": ["Văn phòng công ty", "Tòa nhà văn phòng", "Trung tâm thương mại"],
        "construction": ["Công trình đang xây", "Nhà xưởng đang xây"],
        "fuel_gas": ["Cây xăng", "Kho LPG", "Trạm nạp gas"],
        "medical_education": ["Bệnh viện", "Trường học", "Nhà trẻ", "Trung tâm y tế"],
        "agriculture": ["Kho nông sản", "Nhà kho thóc lúa"],
        "transport": ["Bến xe", "Ga tàu", "Xưởng sửa chữa ô tô"],
        "laboratory": ["Phòng thí nghiệm", "Trung tâm nghiên cứu"],
    }

    # Dùng admin account làm user_id (hoặc tạo user demo nếu cần)
    admin_user = db.query(User).filter(User.id == current_user.id).first()

    created = []
    for i in range(count):
        ftype = data.facility_type if data.facility_type else random.choice(FACILITY_TYPES)
        risk_level = random.choices(RISK_LEVELS, weights=weights)[0]
        rmin, rmax = risk_map[risk_level]
        risk_pct = round(random.uniform(rmin, rmax), 1)

        names = facility_names_map.get(ftype, ["Cơ sở kinh doanh"])
        fname = f"{random.choice(names)} số {random.randint(1, 99)}"

        # Rải điểm xung quanh trung tâm tỉnh (±0.15 độ ≈ ~16km)
        lat = round(base_lat + random.uniform(-0.15, 0.15), 6)
        lng = round(base_lng + random.uniform(-0.15, 0.15), 6)

        streets = ["Đường Lý Thái Tổ", "Đường Nguyễn Trãi", "Phố Hàn Thuyên",
                   "Đường Trần Hưng Đạo", "Ngõ Đoàn Kết", "Đường Lê Lợi"]
        address = f"{random.randint(1, 200)} {random.choice(streets)}, {province}"

        a = Assessment(
            user_id=current_user.id,
            facility_name=fname,
            facility_type=ftype,
            facility_address=address,
            facility_area=round(random.uniform(50, 2000), 0),
            worker_count=random.randint(2, 200),
            latitude=lat,
            longitude=lng,
            total_score=int(risk_pct * 2),
            max_possible_score=200,
            risk_level=risk_level,
            risk_percentage=risk_pct,
            status="completed",
            is_demo=True,
            completed_at=datetime.utcnow(),
        )
        db.add(a)
        created.append({"facility_name": fname, "risk_level": risk_level, "risk_percentage": risk_pct})

    db.commit()
    log_action(db, current_user.id, "generate_demo", "assessment", None,
               None, {"count": count, "province": province},
               request.client.host if request.client else None)
    return {
        "created": len(created),
        "province": province,
        "message": f"Đã tạo {len(created)} bài đánh giá demo tại {province}",
        "items": created,
    }

