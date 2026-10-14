from functools import wraps
from fastapi import HTTPException, status
from models import User


def require_role(*roles):
    """Dependency factory that checks user role."""
    def checker(current_user: User):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Bạn không có quyền thực hiện thao tác này. Yêu cầu quyền: {', '.join(roles)}"
            )
        return current_user
    return checker


def is_admin(user: User) -> bool:
    return user.role in ("admin", "superadmin")


def is_superadmin(user: User) -> bool:
    return user.role == "superadmin"
