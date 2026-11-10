"""
Thống kê tổng hợp số liệu FRAS phục vụ báo cáo sáng kiến (chỉ đọc, chỉ in số đếm, không in thông tin cá nhân).
Chạy trên máy chủ: cd backend && venv/bin/python tools/thong_ke_sang_kien.py [--tu-ngay 2026-08-12]
"""
import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import SessionLocal  # noqa: E402
from models import Assessment, User, ImprovementPlan, ImprovementTask  # noqa: E402

MUC = {"safe": "An toàn", "low": "Thấp", "medium": "Trung bình", "high": "Cao", "critical": "Rất cao"}


def pct(a, b):
    return f"{(100.0 * a / b):.1f}%" if b else "0%"


def thong_ke(db, tu_ngay=None):
    q = db.query(Assessment).filter(Assessment.status == "completed", Assessment.is_demo.isnot(True))
    if tu_ngay:
        q = q.filter(Assessment.completed_at >= tu_ngay)
    ds = q.all()
    n = len(ds)
    co_so = len({a.user_id for a in ds})
    muc = Counter(a.risk_level for a in ds)
    loai = Counter(a.facility_type or "khac" for a in ds)

    ton_tai = da_khac_phuc = 0
    for a in ds:
        try:
            items = json.loads(a.mitigation_data or "{}").get("items", [])
        except Exception:
            items = []
        ton_tai += len(items)
        da_khac_phuc += sum(1 for it in items if it.get("resolved"))

    print(f"  Số cuộc khảo sát hoàn thành: {n}")
    print(f"  Số cơ sở (tài khoản) đã khảo sát: {co_so}")
    for k in ("safe", "low", "medium", "high", "critical"):
        print(f"    - {MUC[k]}: {muc.get(k, 0)} ({pct(muc.get(k, 0), n)})")
    cao = muc.get("high", 0) + muc.get("critical", 0)
    print(f"    => Nguy cơ cao và rất cao: {cao} ({pct(cao, n)})")
    print(f"  Tồn tại phát hiện (danh mục khắc phục): {ton_tai}")
    print(f"  Tồn tại đã khắc phục: {da_khac_phuc} ({pct(da_khac_phuc, ton_tai)})")
    print("  Theo loại hình:")
    for k, v in loai.most_common():
        print(f"    - {k}: {v} ({pct(v, n)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tu-ngay", default="2026-08-12", help="Mốc so sánh (mặc định ngày QĐ 2234/QĐ-UBND)")
    args = ap.parse_args()
    moc = datetime.strptime(args.tu_ngay, "%Y-%m-%d")

    db = SessionLocal()
    try:
        print(f"=== THỐNG KÊ FRAS lúc {datetime.now():%d/%m/%Y %H:%M} ===")
        print(f"Tài khoản: {db.query(User).count()}")
        print(f"Đội quản lý có cơ sở: {db.query(User.management_team).filter(User.management_team.isnot(None)).distinct().count()}")
        print(f"Xã, phường có cơ sở: {db.query(User.ward).filter(User.ward.isnot(None)).distinct().count()}")
        demo = db.query(Assessment).filter(Assessment.is_demo.is_(True)).count()
        dang_lam = db.query(Assessment).filter(Assessment.status != "completed").count()
        print(f"Bài đánh giá (mọi trạng thái): {db.query(Assessment).count()} | dữ liệu mẫu: {demo} | chưa hoàn thành: {dang_lam}")
        print(f"Kế hoạch khắc phục: {db.query(ImprovementPlan).count()} | nhiệm vụ: {db.query(ImprovementTask).count()}"
              f" | nhiệm vụ hoàn thành: {db.query(ImprovementTask).filter(ImprovementTask.status == 'completed').count()}")

        log = Path(__file__).resolve().parent.parent / "data" / "chat_history.jsonl"
        if log.exists():
            dong = [l for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]
            sau = 0
            for l in dong:
                try:
                    if json.loads(l).get("time", "") >= args.tu_ngay:
                        sau += 1
                except Exception:
                    pass
            print(f"Lượt hỏi đáp Trợ lý ảo: {len(dong)} (từ {args.tu_ngay}: {sau})")

        print("\n--- TOÀN BỘ ---")
        thong_ke(db)
        print(f"\n--- TỪ NGÀY {moc:%d/%m/%Y} ---")
        thong_ke(db, moc)
    finally:
        db.close()


if __name__ == "__main__":
    main()
