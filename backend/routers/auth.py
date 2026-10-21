import os
import csv
import uuid
import random
import string
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models import User
from schemas import UserRegister, UserLogin, UserResponse, UserUpdate, TokenResponse, PasswordChangeRequest
from middleware.auth_middleware import (
    hash_password, verify_password, create_access_token, get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def find_facility_in_csv(code: str):
    """Tra cứu cơ sở trong danh_sach_co_so_latest.csv (đã nạp sẵn vào bộ nhớ, đọc tọa độ kiểu Việt Nam)."""
    from utils.facility_import import find_in_csv
    rec = find_in_csv(code)
    if not rec:
        return None
    return {
        "organization": rec["team"],
        "team": rec["team"],
        "code": code,
        "name": rec["name"],
        "lat": rec["lat"],
        "lng": rec["lng"],
        "province": rec["province"],
        "ward": rec["ward"],
        "raw_type": rec["type_label"],
        "facility_types": rec["facility_types"],
        "type_label": rec["type_label"],
        "land_area": rec["land_area"],
        "built_area": rec["built_area"],
        "workers_office": rec["workers_office"],
        "workers_after": rec["workers_after"],
    }


DEFAULT_FACILITY_PASSWORD = "Pc07@123"


def lookup_and_create_facility_user(code: str, db: Session):
    """Create an account on first login, but only for facilities on the official list."""
    info = find_facility_in_csv(code)
    if not info:
        return None
    now = datetime.utcnow()
    user = User(
        id=str(uuid.uuid4()),
        email=f"{code}@fras.vn",
        facility_code=code,
        full_name=info["name"] or f"Cơ sở {code}",
        organization=info["organization"] or "Cơ sở diện quản lý PCCC",
        password_hash=hash_password(DEFAULT_FACILITY_PASSWORD),
        role="user",
        ward=info["ward"],
        province=info["province"] or "Tỉnh Bắc Ninh",
        latitude=info["lat"],
        longitude=info["lng"],
        facility_types=info.get("facility_types") or "Chưa có loại hình",
        management_team=info.get("team"),
        facility_type_label=info.get("type_label") or None,
        land_area=info.get("land_area"),
        built_area=info.get("built_area"),
        workers_office=info.get("workers_office"),
        workers_after=info.get("workers_after"),
        is_active=True,
        is_locked=False,
        created_at=now,
        updated_at=now
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def generate_facility_code(db: Session) -> str:
    """Generate a unique 13-digit facility code."""
    while True:
        code = ''.join(random.choices(string.digits, k=13))
        existing = db.query(User).filter(User.facility_code == code).first()
        if not existing:
            return code


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã được sử dụng")
    
    facility_code = generate_facility_code(db)
    
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        organization=data.organization,
        phone=data.phone,
        facility_code=facility_code,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"sub": user.id, "role": user.role})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user)
    )


@router.get("/facility/{code}")
def get_facility_info(code: str, db: Session = Depends(get_db)):
    """Tra cứu thông tin cơ sở phục vụ khảo sát và đăng nhập."""
    code = code.strip()
    user = db.query(User).filter(User.facility_code == code).first()
    if user:
        return {
            "found": True,
            "facility_code": user.facility_code,
            "full_name": user.full_name,
            "organization": user.organization or "Cơ sở diện quản lý PCCC",
            "ward": user.ward or "",
            "province": user.province or "Tỉnh Bắc Ninh",
            "facility_types": user.facility_types or "Chưa có loại hình",
            "latitude": user.latitude,
            "longitude": user.longitude,
        }
    info = find_facility_in_csv(code)
    if info:
        return {
            "found": True,
            "facility_code": code,
            "full_name": info["name"],
            "organization": info["organization"],
            "ward": info["ward"],
            "province": info["province"],
            "facility_types": "Chưa có loại hình",
            "latitude": info["lat"],
            "longitude": info["lng"],
        }
    return {
        "found": False,
        "facility_code": code,
        "full_name": f"Cơ sở quản lý ({code})",
        "province": "Tỉnh Bắc Ninh"
    }


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    ident = data.email.strip()
    pw = data.password.strip()

    # Allow login by email OR facility_code OR username 'admin'
    admin_ident = "admin@fras.vn" if ident.lower() in ["admin", "admin@fras.vn", "admin@fras-ai.com"] else ident
    user = db.query(User).filter(
        or_(User.email == admin_ident, User.email == ident, User.facility_code == ident)
    ).first()

    # Check if this is a numeric facility code (e.g. 13-digit code)
    is_numeric_code = ident.isdigit() and len(ident) >= 6

    # First login of a listed facility: create its account (default password only)
    if not user and is_numeric_code and pw == DEFAULT_FACILITY_PASSWORD:
        user = lookup_and_create_facility_user(ident, db)

    if user:
        # If user has generic placeholder name but CSV has details, enrich it
        if user.facility_code and user.full_name and user.full_name.startswith("Cơ sở quản lý ("):
            info = find_facility_in_csv(user.facility_code)
            if info and info.get("name"):
                user.full_name = info["name"]
                if info.get("ward"):
                    user.ward = info["ward"]
                if info.get("organization"):
                    user.organization = info["organization"]
                db.commit()
                db.refresh(user)

        if not verify_password(pw, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Mật khẩu không chính xác"
            )
    else:
        raise HTTPException(
            status_code=401,
            detail="Tài khoản hoặc Mã cơ sở không tồn tại"
        )

    if user.is_locked:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị khóa")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị vô hiệu hóa")

    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id, "role": user.role})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user)
    )



@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.full_name is not None:
        current_user.full_name = data.full_name
    if data.organization is not None:
        current_user.organization = data.organization
    if data.phone is not None:
        current_user.phone = data.phone
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.put("/change-password", response_model=dict)
def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Mật khẩu cũ không chính xác"
        )
    
    current_user.password_hash = hash_password(data.new_password)
    current_user.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Đổi mật khẩu thành công"}
