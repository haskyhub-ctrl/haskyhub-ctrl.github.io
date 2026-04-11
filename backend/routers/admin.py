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
