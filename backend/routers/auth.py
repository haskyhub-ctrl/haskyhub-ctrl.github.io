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


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    # Allow login by email OR facility_code
    user = db.query(User).filter(
        or_(User.email == data.email, User.facility_code == data.email)
    ).first()
    
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Email/Mã cơ sở hoặc mật khẩu không đúng"
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
