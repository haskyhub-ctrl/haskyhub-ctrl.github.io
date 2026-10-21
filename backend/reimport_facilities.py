"""Nạp danh sách cơ sở thuộc diện quản lý từ danh_sach_co_so_latest.csv vào CSDL.

Cách dùng (chạy trong thư mục backend, đã kích hoạt môi trường ảo):

  python reimport_facilities.py --dry-run
      Chỉ đọc file và in báo cáo (số cơ sở, số cơ sở thiếu tọa độ...), không ghi gì.

  python reimport_facilities.py
      Thêm các cơ sở còn thiếu (theo mã cơ sở). Không đụng tới tài khoản đã có. Chạy lại bao nhiêu lần cũng được.

  python reimport_facilities.py --wipe --yes
      THAY TOÀN BỘ: sao lưu CSDL, xóa mọi bài đánh giá cùng dữ liệu đi kèm và mọi tài khoản không phải quản trị,
      rồi nạp lại từ file. Tài khoản quản trị (admin, superadmin) được giữ nguyên.
      Nếu sao lưu thất bại thì dừng, không xóa gì.

Mật khẩu mặc định của tài khoản cơ sở: xem DEFAULT_PASSWORD trong utils/facility_import.py.
"""
import argparse
import os
import sys
import time
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text

from database import SessionLocal, migrate_db, Base, engine
from models import User
from middleware.auth_middleware import hash_password
from utils.facility_import import DEFAULT_PASSWORD, load_records, new_user_mapping, csv_path

# Bảng phụ thuộc vào bài đánh giá và tài khoản, xóa theo thứ tự con trước cha
WIPE_STEPS = [
    ("tác vụ cải thiện", "DELETE FROM improvement_tasks"),
    ("kế hoạch cải thiện", "DELETE FROM improvement_plans"),
    ("phân tích ảnh", "DELETE FROM image_analyses"),
    ("câu trả lời", "DELETE FROM assessment_answers"),
    ("điểm theo nhóm", "DELETE FROM category_scores"),
    ("bài đánh giá", "DELETE FROM assessments"),
    ("thông báo của tài khoản", "DELETE FROM notifications WHERE user_id IN (SELECT id FROM users WHERE role NOT IN ('admin', 'superadmin'))"),
    ("câu hỏi do tài khoản tạo (bỏ liên kết)", "UPDATE questions SET created_by = NULL WHERE created_by IN (SELECT id FROM users WHERE role NOT IN ('admin', 'superadmin'))"),
    ("mẫu câu hỏi do tài khoản tạo (bỏ liên kết)", "UPDATE question_templates SET created_by = NULL WHERE created_by IN (SELECT id FROM users WHERE role NOT IN ('admin', 'superadmin'))"),
    ("tài khoản không phải quản trị", "DELETE FROM users WHERE role NOT IN ('admin', 'superadmin')"),
]


def counts(db):
    out = {}
    for label, sql in (
        ("tài khoản", "SELECT COUNT(*) FROM users"),
        ("tài khoản quản trị", "SELECT COUNT(*) FROM users WHERE role IN ('admin', 'superadmin')"),
        ("bài đánh giá", "SELECT COUNT(*) FROM assessments"),
    ):
        out[label] = db.execute(text(sql)).scalar()
    return out


def wipe(db):
    for label, sql in WIPE_STEPS:
        try:
            res = db.execute(text(sql))
            print(f"  - {label}: {res.rowcount if res.rowcount is not None else '?'} dòng")
        except Exception as e:
            db.rollback()
            msg = str(e).lower()
            if "no such table" in msg or "does not exist" in msg:
                print(f"  - {label}: bảng chưa có, bỏ qua")
                continue
            raise
    db.commit()


def insert_records(db, records, update_existing=False):
    print("Tạo mã băm mật khẩu mặc định...")
    pwd_hash = hash_password(DEFAULT_PASSWORD)
    existing = {c: i for c, i in db.query(User.facility_code, User.id).filter(User.facility_code.isnot(None)).all()}
    emails = set(e for (e,) in db.query(User.email).all())
    now = datetime.utcnow()
    batch, added, skipped = [], 0, 0
    for rec in records:
        if rec["code"] in existing:
            skipped += 1
            continue
        mapping = new_user_mapping(rec, pwd_hash, now)
        if mapping["email"] in emails:
            skipped += 1
            continue
        emails.add(mapping["email"])
        batch.append(mapping)
        if len(batch) >= 2000:
            db.bulk_insert_mappings(User, batch)
            db.commit()
            added += len(batch)
            batch = []
            print(f"  đã nạp {added} cơ sở...")
    if batch:
        db.bulk_insert_mappings(User, batch)
        db.commit()
        added += len(batch)
    return added, skipped


def main():
    ap = argparse.ArgumentParser(description="Nạp danh sách cơ sở thuộc diện quản lý")
    ap.add_argument("--csv", help="đường dẫn file CSV (mặc định: danh_sach_co_so_latest.csv ở thư mục gốc dự án)")
    ap.add_argument("--wipe", action="store_true", help="thay toàn bộ: xóa tài khoản và bài đánh giá cũ rồi nạp lại")
    ap.add_argument("--yes", action="store_true", help="xác nhận cho --wipe")
    ap.add_argument("--dry-run", action="store_true", help="chỉ in báo cáo, không ghi")
    args = ap.parse_args()

    path = args.csv or csv_path()
    if not path or not os.path.exists(path):
        print("LỖI: không tìm thấy file danh_sach_co_so_latest.csv")
        sys.exit(1)

    t0 = time.time()
    print(f"Đọc file: {path}")
    records, st = load_records(path)
    teams = {r["team"] for r in records}
    wards = {r["ward"] for r in records}
    print(f"  {st['rows']} dòng dữ liệu, {len(records)} cơ sở hợp lệ, {len(teams)} đội quản lý, {len(wards)} xã phường")
    print(f"  bỏ qua {st['no_code']} dòng không có mã cơ sở, {st['duplicate_code']} dòng trùng mã")
    with_coords = sum(1 for r in records if r["lat"] is not None)
    print(f"  tọa độ hợp lệ: {with_coords} | để trống: {st['no_coords']} | sai hoặc ngoài vùng: {st['bad_coords']}")
    if not records:
        print("LỖI: file không có cơ sở nào hợp lệ, dừng.")
        sys.exit(1)
    if args.dry_run:
        print("(dry-run) Không ghi gì vào CSDL.")
        return

    Base.metadata.create_all(bind=engine)
    migrate_db()
    db = SessionLocal()
    try:
        print("Trước khi chạy:", counts(db))
        if args.wipe:
            if not args.yes:
                print("LỖI: --wipe xóa dữ liệu, cần thêm --yes để xác nhận.")
                sys.exit(2)
            from utils.backup_service import backup_db
            print("Sao lưu CSDL trước khi xóa...")
            backup = backup_db()
            if not backup:
                print("LỖI: sao lưu thất bại, DỪNG, chưa xóa gì.")
                sys.exit(3)
            print(f"  đã sao lưu: {backup}")
            print("Xóa dữ liệu cũ:")
            wipe(db)
        added, skipped = insert_records(db, records)
        print(f"Đã nạp {added} cơ sở mới, bỏ qua {skipped} (đã có).")
        print("Sau khi chạy:", counts(db))
    finally:
        db.close()
    print(f"Hoàn tất trong {time.time() - t0:.0f} giây.")


if __name__ == "__main__":
    main()
