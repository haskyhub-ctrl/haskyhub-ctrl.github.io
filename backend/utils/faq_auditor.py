"""Bộ công cụ quản lý và kiểm tra định kỳ Ngân hàng 200 câu hỏi thường gặp (FAQ) PCCC & CNCH.

Tính năng:
1. Rà soát định kỳ 1 tuần/lần (Weekly Audit):
   - Quét toàn bộ câu hỏi và đáp án trong ngân hàng.
   - Phát hiện các căn cứ văn bản đã hết hiệu lực (NĐ 136/2020, NĐ 50/2024, NĐ 144/2021, NĐ 167/2013...).
   - Kiểm tra các quy định đã cải cách 2026 (bãi bỏ nghiệm thu Công an, bãi bỏ chứng nhận huấn luyện...).
   - Đánh dấu các câu quá 7 ngày chưa rà soát để cán bộ kiểm tra, cập nhật.
2. Tự động đồng bộ và nạp ngân hàng 200 câu hỏi chuẩn vào cơ sở dữ liệu.
3. Chạy tự động trong vòng lặp nền hằng tuần (mỗi thứ Hai hoặc sau 7 ngày).
"""
import asyncio
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any

from sqlalchemy.orm import Session
from models import KbQuestion
from utils.kb_qa import question_key

VN_TZ = timezone(timedelta(hours=7))

OBSOLETE_PATTERNS = [
    (r"\b136/2020(?:/NĐ-CP)?\b", "Nghị định 136/2020/NĐ-CP đã hết hiệu lực (thay bằng NĐ 105/2025 và NĐ 347/2026)"),
    (r"\b50/2024(?:/NĐ-CP)?\b", "Nghị định 50/2024/NĐ-CP đã hết hiệu lực (thay bằng NĐ 105/2025 và NĐ 347/2026)"),
    (r"\b144/2021(?:/NĐ-CP)?\b", "Nghị định 144/2021/NĐ-CP về xử phạt PCCC đã hết hiệu lực (thay bằng NĐ 106/2025/NĐ-CP)"),
    (r"\b167/2013(?:/NĐ-CP)?\b", "Nghị định 167/2013/NĐ-CP đã hết hiệu lực"),
    (r"\b79/2014(?:/NĐ-CP)?\b", "Nghị định 79/2014/NĐ-CP đã hết hiệu lực từ lâu"),
    (r"\bLuật\s+PCCC\s+(?:năm\s+)?2001\b", "Luật PCCC 2001 đã được thay thế toàn diện bởi Luật số 55/2024/QH15"),
    (r"\bLuật\s+số\s+40/2013/QH13\b", "Luật sửa đổi 2013 đã hết hiệu lực"),
    (r"\bchứng\s+nhận\s+(?:huấn\s+luyện\s+)?(?:có\s+thời\s+hạn|giá\s+trị)\s+0?5\s+năm\b", "Chứng nhận huấn luyện đã bị bãi bỏ theo Luật 55/2024/QH15; thay bằng huấn luyện định kỳ 5 năm"),
]

AUDIT_REPORT_PATH = Path(__file__).resolve().parent.parent / "data" / "faq_audit_report.json"


def audit_faq_bank(db: Session) -> Dict[str, Any]:
    """Rà soát toàn bộ ngân hàng câu hỏi thường gặp:
    - Tìm văn bản cũ
    - Kiểm tra thời hạn rà soát (> 7 ngày)
    - Phân loại trạng thái: Hợp lệ / Cần rà soát / Chứa căn cứ cũ
    """
    now = datetime.now(VN_TZ)
    items = db.query(KbQuestion).filter(KbQuestion.status == "approved").all()
    
    total = len(items)
    outdated_list = []
    due_review_list = []
    valid_count = 0
    
    for q in items:
        text_check = f"{q.question or ''} {q.answer or ''}"
        issues = []
        
        # 1. Kiểm tra văn bản hết hiệu lực
        for pattern, reason in OBSOLETE_PATTERNS:
            if re.search(pattern, text_check, re.IGNORECASE):
                issues.append(reason)
                
        # 2. Kiểm tra thời hạn rà soát (quá 7 ngày kể từ lần rà soát gần nhất)
        review_date = q.answered_at or q.created_at or datetime.min
        if review_date.tzinfo is None:
            review_date = review_date.replace(tzinfo=timezone.utc).astimezone(VN_TZ)
            
        days_since_review = (now - review_date).days
        is_due = days_since_review >= 7
        
        if issues:
            outdated_list.append({
                "id": q.id,
                "question": q.question,
                "issues": issues,
                "last_reviewed": review_date.strftime("%d/%m/%Y"),
                "days_ago": days_since_review
            })
        elif is_due:
            due_review_list.append({
                "id": q.id,
                "question": q.question,
                "last_reviewed": review_date.strftime("%d/%m/%Y"),
                "days_ago": days_since_review
            })
        else:
            valid_count += 1
            
    status_summary = "hoan_hao" if not outdated_list and not due_review_list else "can_ra_soat"
    
    report = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "total_faqs": total,
        "valid_count": valid_count,
        "outdated_count": len(outdated_list),
        "due_review_count": len(due_review_list),
        "status_summary": status_summary,
        "outdated_items": outdated_list,
        "due_review_items": due_review_list[:20],  # top 20 câu cần rà soát
    }
    
    # Ghi báo cáo ra file json
    try:
        AUDIT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(AUDIT_REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[FAQ Auditor] Không lưu được báo cáo: {e}")
        
    return report


def get_latest_audit_report() -> Dict[str, Any]:
    """Đọc báo cáo rà soát mới nhất từ đĩa."""
    if AUDIT_REPORT_PATH.exists():
        try:
            with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "timestamp": "Chưa chạy rà soát",
        "total_faqs": 0,
        "valid_count": 0,
        "outdated_count": 0,
        "due_review_count": 0,
        "status_summary": "chua_chay",
        "outdated_items": [],
        "due_review_items": []
    }


def seed_200_faqs(db: Session, force_update: bool = False) -> Dict[str, int]:
    """Nạp bộ 200 câu hỏi chuẩn vào cơ sở dữ liệu.
    Nguồn: kho_seed/faq_bank_2026.json (hoặc kho_seed/faq.json).
    """
    bank_path = Path(__file__).resolve().parent.parent / "kho_seed" / "faq_bank_2026.json"
    if not bank_path.exists():
        bank_path = Path(__file__).resolve().parent.parent / "kho_seed" / "faq.json"
        
    if not bank_path.exists():
        return {"added": 0, "updated": 0, "total": 0}
        
    with open(bank_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    added = 0
    updated = 0
    now = datetime.now(timezone.utc)
    
    for item in data:
        q_text = item.get("question", "").strip()
        a_text = item.get("answer", "").strip()
        if not q_text or not a_text:
            continue
            
        key = question_key(q_text)
        existing = db.query(KbQuestion).filter(KbQuestion.question_key == key).first()
        
        if not existing:
            new_row = KbQuestion(
                question=q_text,
                question_key=key,
                answer=a_text,
                status="approved",
                source="faq_bank_2026",
                times_asked=0,
                created_at=now,
                answered_at=now
            )
            db.add(new_row)
            added += 1
        elif force_update:
            existing.answer = a_text
            existing.status = "approved"
            existing.answered_at = now
            updated += 1
            
    if added or updated:
        db.commit()
        
    return {"added": added, "updated": updated, "total": len(data)}


async def weekly_faq_audit_loop(interval_hours: float = 168.0):
    """Vòng lặp chạy ngầm tự động rà soát ngân hàng câu hỏi định kỳ 1 tuần/lần (168 giờ)."""
    print(f"[FAQ Auditor] Bắt đầu dịch vụ tự động rà soát hiệu lực FAQ định kỳ mỗi {interval_hours} giờ.")
    while True:
        try:
            from database import SessionLocal
            db = SessionLocal()
            try:
                report = audit_faq_bank(db)
                print(f"[FAQ Auditor] Đã rà soát {report['total_faqs']} câu: {report['valid_count']} đạt chuẩn, {report['outdated_count']} chứa căn cứ cũ, {report['due_review_count']} đến hạn rà soát.")
            finally:
                db.close()
        except Exception as e:
            print(f"[FAQ Auditor] Lỗi rà soát định kỳ: {e}")
            
        await asyncio.sleep(interval_hours * 3600)
