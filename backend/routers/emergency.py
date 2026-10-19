import os
import json
import base64
from datetime import datetime
from typing import Optional, List
import httpx
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import FireReport, User
from middleware.auth_middleware import get_current_user
from middleware.rbac import require_role

# Ensure fire_reports table exists
Base.metadata.create_all(bind=engine, tables=[FireReport.__table__])

router = APIRouter(prefix="/api/emergency", tags=["Emergency Fire Report 114"])

REPORTS_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fire_reports.json")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8685857438:AAE4m0Ew0yh1ov_gnN3ANEz2_wu8GALN-3Y")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1003941425126")


def get_target_chat_ids() -> List[str]:
    """Get target Telegram chat/channel IDs."""
    chat_ids = set()
    if TELEGRAM_CHAT_ID:
        for cid in TELEGRAM_CHAT_ID.split(","):
            cid = cid.strip()
            if cid:
                chat_ids.add(cid)
        return list(chat_ids)

    # Discover recent chats from bot updates
    if TELEGRAM_BOT_TOKEN:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            resp = httpx.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("result", []):
                    # Check message
                    msg = item.get("message") or item.get("channel_post") or item.get("my_chat_member")
                    if msg:
                        chat = msg.get("chat") if isinstance(msg, dict) and "chat" in msg else msg
                        if isinstance(chat, dict) and "id" in chat:
                            chat_ids.add(str(chat["id"]))
        except Exception as e:
            print(f"[Telegram Discovery] Error: {e}")

    return list(chat_ids)


def send_telegram_alert(report: FireReport, image_bytes: Optional[bytes] = None):
    """Send emergency 114 notification to Telegram bot/group.
    Zero disk usage: If image_bytes is provided, it streams directly to Telegram sendPhoto
    and is never saved to the server disk.
    """
    if not TELEGRAM_BOT_TOKEN:
        return

    chat_ids = get_target_chat_ids()
    if not chat_ids:
        print("[Telegram Alert] Notice: No chat IDs found. Please send a message to @BAOCHAY114_bot or add it to your group.")
        return

    maps_link = ""
    if report.latitude and report.longitude:
        maps_link = f"\n🗺️ <b>Bản đồ:</b> <a href=\"https://www.google.com/maps?q={report.latitude},{report.longitude}\">Mở vị trí hiện trường</a>"

    text = (
        f"🚨 <b>BÁO CHÁY KHẨN CẤP 114 - BẮC NINH</b> 🚨\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⏰ <b>Thời gian:</b> {report.created_at.strftime('%H:%M:%S ngày %d/%m/%Y')}\n"
        f"📞 <b>Người báo:</b> <code>{report.phone}</code> (<a href=\"tel:{report.phone}\">Bấm gọi ngay</a>)\n"
        f"📍 <b>Địa chỉ:</b> {report.location_address}\n"
        f"🏠 <b>Loại hình:</b> {report.fire_type}\n"
        f"🔥 <b>Mức độ:</b> {report.severity}\n"
        f"{maps_link}\n"
    )
    if report.notes:
        text += f"📝 <b>Ghi chú:</b> {report.notes}\n"
    text += f"━━━━━━━━━━━━━━━━━━\n<i>Hệ thống Cảnh báo Cháy Thông minh PCCC Bắc Ninh</i>"

    for cid in chat_ids:
        try:
            if image_bytes:
                # Direct stream to Telegram sendPhoto (0 bytes saved on VPS disk!)
                photo_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
                files = {"photo": ("fire_scene.jpg", image_bytes, "image/jpeg")}
                data = {
                    "chat_id": cid,
                    "caption": text[:1024],
                    "parse_mode": "HTML"
                }
                resp = httpx.post(photo_url, data=data, files=files, timeout=15)
                print(f"[Telegram Alert] Sent photo alert to chat {cid}: status {resp.status_code}")
            else:
                send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": cid,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                }
                httpx.post(send_url, json=payload, timeout=8)
                print(f"[Telegram Alert] Sent notification to chat {cid}")
        except Exception as e:
            print(f"[Telegram Alert] Failed to send to chat {cid}: {e}")


class EmergencyReportCreate(BaseModel):
    phone: str
    location_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fire_type: str = "Nhà ở / Hộ gia đình"
    severity: str = "Khói nhiều / Lửa bốc cao"
    notes: Optional[str] = None
    image_url: Optional[str] = None
    image_base64: Optional[str] = None  # Direct stream to Telegram, 0 disk usage


class EmergencyReportResponse(BaseModel):
    id: str
    phone: str
    location_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fire_type: str
    severity: str
    notes: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


@router.post("/report")
def submit_fire_report(data: EmergencyReportCreate, db: Session = Depends(get_db)):
    """Public endpoint: Citizens submit emergency fire report to 114."""
    phone_clean = data.phone.strip()
    addr_clean = data.location_address.strip()
    if not phone_clean:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp số điện thoại để cán bộ 114 liên hệ xác minh")
    if not addr_clean:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp địa điểm xảy ra đám cháy")

    report = FireReport(
        phone=phone_clean,
        location_address=addr_clean,
        latitude=data.latitude,
        longitude=data.longitude,
        fire_type=data.fire_type,
        severity=data.severity,
        notes=data.notes.strip() if data.notes else None,
        image_url=data.image_url,
        status="received"
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    # Append to local JSON file for easy checking
    try:
        current_logs = []
        if os.path.exists(REPORTS_LOG_FILE):
            with open(REPORTS_LOG_FILE, "r", encoding="utf-8") as f:
                current_logs = json.load(f)

        current_logs.insert(0, {
            "id": report.id,
            "created_at": report.created_at.strftime("%H:%M:%S %d/%m/%Y"),
            "phone": report.phone,
            "location_address": report.location_address,
            "latitude": report.latitude,
            "longitude": report.longitude,
            "fire_type": report.fire_type,
            "severity": report.severity,
            "notes": report.notes,
            "status": report.status,
        })
        with open(REPORTS_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(current_logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Fire Report Log] Warning: could not write to JSON log: {e}")

    # Decode image in RAM only (never written to disk)
    image_bytes = None
    if data.image_base64:
        try:
            b64_str = data.image_base64
            if "," in b64_str:
                b64_str = b64_str.split(",", 1)[1]
            image_bytes = base64.b64decode(b64_str)
            print(f"[Fire Report] Received image of size: {len(image_bytes)} bytes. Forwarding to Telegram (0 disk usage).")
        except Exception as e:
            print(f"[Fire Report] Warning: Could not decode base64 image: {e}")

    # Send instant Telegram alert to Officers
    try:
        send_telegram_alert(report, image_bytes=image_bytes)
    except Exception as e:
        print(f"[Telegram Error] Could not send alert: {e}")

    return {
        "status": "ok",
        "report_id": report.id,
        "message": "Đã tiếp nhận thông tin, vui lòng nghe máy để xác minh thông tin",
        "created_at": report.created_at.isoformat()
    }


@router.get("/reports")
def get_fire_reports(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """View all received emergency fire reports (admin only: contains phone numbers)."""
    require_role("admin", "superadmin")(current_user)
    reports = db.query(FireReport).order_by(FireReport.created_at.desc()).limit(100).all()
    return [
        {
            "id": r.id,
            "created_at": r.created_at.strftime("%H:%M:%S %d/%m/%Y") if r.created_at else None,
            "phone": r.phone,
            "location_address": r.location_address,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "fire_type": r.fire_type,
            "severity": r.severity,
            "notes": r.notes,
            "status": r.status,
        }
        for r in reports
    ]


@router.get("/telegram-status")
def get_telegram_status(current_user: User = Depends(get_current_user)):
    """Check Telegram bot status and active chat IDs (admin only)."""
    require_role("admin", "superadmin")(current_user)
    chats = get_target_chat_ids()
    return {
        "bot_configured": bool(TELEGRAM_BOT_TOKEN),
        "bot_token_preview": TELEGRAM_BOT_TOKEN[:10] + "..." if TELEGRAM_BOT_TOKEN else None,
        "active_chat_ids": chats,
        "status": "ready" if chats else "waiting_for_user_chat"
    }
