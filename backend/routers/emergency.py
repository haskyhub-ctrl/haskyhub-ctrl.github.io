import os
import json
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import FireReport

# Ensure fire_reports table exists
Base.metadata.create_all(bind=engine, tables=[FireReport.__table__])

router = APIRouter(prefix="/api/emergency", tags=["Emergency Fire Report 114"])

REPORTS_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fire_reports.json")


class EmergencyReportCreate(BaseModel):
    phone: str
    location_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fire_type: str = "Nhà ở / Hộ gia đình"
    severity: str = "Khói nhiều / Lửa bốc cao"
    notes: Optional[str] = None
    image_url: Optional[str] = None


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

    return {
        "status": "ok",
        "report_id": report.id,
        "message": "Đã tiếp nhận thông tin, vui lòng nghe máy để xác minh thông tin",
        "created_at": report.created_at.isoformat()
    }


@router.get("/reports")
def get_fire_reports(db: Session = Depends(get_db)):
    """View all received emergency fire reports."""
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
