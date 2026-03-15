"""
Notifications Router — Alert & Notification System.
Manages user notifications for high-risk assessments, reminders, etc.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Notification
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("/")
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List user notifications, newest first."""
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )

    return [
        {
            "id": n.id,
            "type": n.notification_type,
            "title": n.title,
            "message": n.message,
            "link": n.link,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in notifications
    ]


@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get count of unread notifications."""
    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False,
        )
        .count()
    )
    return {"count": count}


@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a notification as read."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id,
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông báo")

    notification.is_read = True
    db.commit()
    return {"status": "ok"}


@router.put("/read-all")
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark all notifications as read."""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False,
    ).update({"is_read": True})
    db.commit()
    return {"status": "ok"}


def create_notification(db: Session, user_id: str, notification_type: str,
                        title: str, message: str, link: str = None):
    """Helper function to create a notification."""
    notification = Notification(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link,
    )
    db.add(notification)
    db.commit()
    return notification
