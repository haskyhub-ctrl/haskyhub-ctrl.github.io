import os
import time
import asyncio
import shutil
import subprocess
from urllib.parse import urlparse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backup_service")

# Mặc định sao lưu mỗi 24 giờ (86400 giây). Có thể chỉnh sửa qua biến môi trường.
BACKUP_INTERVAL_SECONDS = int(os.environ.get("BACKUP_INTERVAL_SECONDS", 86400))
BACKUP_DIR = "./backups"

VALID_BACKUP_EXTS = (".db", ".sql", ".dump", ".sql.gz")


def get_db_info():
    # Same URL the app itself uses (already resolves SQLite to an absolute path)
    from database import DATABASE_URL
    return DATABASE_URL


def safe_backup_path(file_name: str):
    """Return the full path of a backup file, or None if the name is not a plain backup file name.
    Blocks names like '../main.py' that would reach files outside the backups folder."""
    if not file_name or os.path.basename(file_name) != file_name:
        return None
    if not file_name.startswith("fras_backup_") or not file_name.endswith(VALID_BACKUP_EXTS):
        return None
    return os.path.join(BACKUP_DIR, file_name)


def _latest_backup_age_seconds():
    if not os.path.isdir(BACKUP_DIR):
        return None
    times = [os.path.getmtime(os.path.join(BACKUP_DIR, f)) for f in os.listdir(BACKUP_DIR)
             if f.startswith("fras_backup_") and f.endswith(VALID_BACKUP_EXTS)]
    return (time.time() - max(times)) if times else None


async def auto_backup_task():
    """Chạy ngầm định kỳ sao lưu database (hỗ trợ cả PostgreSQL và SQLite)."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    logger.info(f"Bắt đầu dịch vụ tự động sao lưu định kỳ mỗi {BACKUP_INTERVAL_SECONDS/3600:.1f} giờ.")
    
    # Sao lưu khi khởi động, trừ khi đã có bản sao lưu gần đây
    # (mỗi lần deploy đều khởi động lại; không để các lần deploy đẩy mất bản sao lưu của các ngày trước)
    age = _latest_backup_age_seconds()
    if age is None or age >= BACKUP_INTERVAL_SECONDS:
        backup_db()
    else:
        logger.info(f"Bỏ qua sao lưu khi khởi động: đã có bản sao lưu {age/3600:.1f} giờ trước.")
        
    while True:
        try:
            await asyncio.sleep(BACKUP_INTERVAL_SECONDS)
            backup_db()
        except asyncio.CancelledError:
            logger.info("Dịch vụ tự động sao lưu đã dừng.")
            break
        except Exception as e:
            logger.error(f"Lỗi khi sao lưu tự động: {e}")
            await asyncio.sleep(60)

def backup_db():
    """Thực hiện sao lưu cơ sở dữ liệu (tự động phân biệt PostgreSQL hoặc SQLite)."""
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        cleanup_old_backups(keep_count=14)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_url = get_db_info()

        if db_url.startswith("postgresql"):
            backup_filename = f"fras_backup_{timestamp}.sql"
            backup_path = os.path.join(BACKUP_DIR, backup_filename)
            
            # Phân tích chuỗi kết nối
            parsed = urlparse(db_url)
            user = parsed.username or "postgres"
            password = parsed.password or ""
            host = parsed.hostname or "localhost"
            port = parsed.port or 5432
            dbname = parsed.path.lstrip("/") or "fras"

            env = os.environ.copy()
            if password:
                env["PGPASSWORD"] = password

            cmd = [
                "pg_dump",
                "-U", user,
                "-h", host,
                "-p", str(port),
                "-d", dbname,
                "-f", backup_path,
                "--clean",
                "--if-exists",
            ]

            logger.info(f"Đang thực hiện pg_dump database '{dbname}' vào {backup_path}...")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=120)

            if result.returncode != 0:
                logger.error(f"pg_dump thất bại (code {result.returncode}): {result.stderr}")
                # Fallback: nếu pg_dump không có trong PATH, log chi tiết
                return None

            if os.path.exists(backup_path) and os.path.getsize(backup_path) > 0:
                logger.info(f"✅ Đã sao lưu PostgreSQL thành công: {backup_path} ({os.path.getsize(backup_path)} bytes)")
                return backup_path
            else:
                logger.error("File sao lưu rỗng hoặc không được tạo")
                return None

        else:
            # SQLite fallback
            backup_filename = f"fras_backup_{timestamp}.db"
            backup_path = os.path.join(BACKUP_DIR, backup_filename)
            raw_path = db_url.replace("sqlite:///./", "").replace("sqlite:///", "")
            if not raw_path or raw_path.startswith("sqlite"):
                raw_path = "fras.db"

            if os.path.exists(raw_path):
                import sqlite3
                source_conn = sqlite3.connect(raw_path)
                dest_conn = sqlite3.connect(backup_path)
                with source_conn, dest_conn:
                    source_conn.backup(dest_conn)
                source_conn.close()
                dest_conn.close()
                logger.info(f"✅ Đã sao lưu SQLite thành công: {backup_path}")
                return backup_path
            else:
                logger.warning(f"Không tìm thấy file CSDL SQLite: {raw_path}")
                return None

    except Exception as e:
        logger.error(f"❌ Lỗi khi thực hiện sao lưu: {e}")
        return None

def cleanup_old_backups(keep_count=14):
    """Giữ lại 'keep_count' bản backup mới nhất để tránh đầy ổ cứng."""
    try:
        if not os.path.exists(BACKUP_DIR):
            return
        backups = []
        for f in os.listdir(BACKUP_DIR):
            # Files uploaded by an admin are kept; only automatic/manual backups rotate
            if f.startswith("fras_backup_") and not f.startswith("fras_backup_uploaded_") and f.endswith(VALID_BACKUP_EXTS):
                full_path = os.path.join(BACKUP_DIR, f)
                backups.append((full_path, os.path.getmtime(full_path)))
                
        # Sắp xếp theo ngày gần nhất
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # Chỉ giữ lại keep_count bản
        if len(backups) > keep_count:
            for old_file, _ in backups[keep_count:]:
                os.remove(old_file)
                logger.info(f"Đã dọn dẹp bản sao lưu cũ: {old_file}")
    except Exception as e:
        logger.error(f"Lỗi khi dọn dẹp bản backup cũ: {e}")

def restore_db(backup_path: str):
    """Phục hồi cơ sở dữ liệu từ file sao lưu (PostgreSQL hoặc SQLite)."""
    try:
        if not os.path.exists(backup_path):
            logger.error(f"File sao lưu không tồn tại: {backup_path}")
            return False, "File sao lưu không tồn tại trên hệ thống"

        db_url = get_db_info()

        if db_url.startswith("postgresql"):
            parsed = urlparse(db_url)
            user = parsed.username or "postgres"
            password = parsed.password or ""
            host = parsed.hostname or "localhost"
            port = parsed.port or 5432
            dbname = parsed.path.lstrip("/") or "fras"

            env = os.environ.copy()
            if password:
                env["PGPASSWORD"] = password

            # Never wait forever for table locks held by open requests (that froze the whole site)
            env["PGOPTIONS"] = "-c lock_timeout=60000"
            # Close idle pooled connections so they don't hold locks on the tables being replaced
            try:
                from database import engine
                engine.dispose()
            except Exception:
                pass

            cmd = [
                "psql",
                "-U", user,
                "-h", host,
                "-p", str(port),
                "-d", dbname,
                "-f", backup_path,
                "-q",
                "--single-transaction",     # all-or-nothing: a failed restore leaves data untouched
                "-v", "ON_ERROR_STOP=1",
            ]

            logger.info(f"Đang phục hồi CSDL PostgreSQL từ {backup_path}...")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=180)

            if result.returncode != 0:
                logger.error(f"psql restore thất bại (code {result.returncode}): {result.stderr}")
                return False, f"Lỗi psql: {result.stderr[:200]}"

            logger.info(f"✅ Đã phục hồi CSDL PostgreSQL thành công từ: {backup_path}")
            return True, "Khôi phục dữ liệu PostgreSQL thành công!"

        else:
            # SQLite restore
            raw_path = db_url.replace("sqlite:///./", "").replace("sqlite:///", "")
            if not raw_path or raw_path.startswith("sqlite"):
                raw_path = "fras.db"

            shutil.copyfile(backup_path, raw_path)
            logger.info(f"✅ Đã phục hồi CSDL SQLite thành công từ: {backup_path}")
            return True, "Khôi phục dữ liệu SQLite thành công!"

    except Exception as e:
        logger.error(f"❌ Lỗi khi phục hồi CSDL: {e}")
        return False, str(e)

def delete_backup_file(file_name: str):
    """Xóa file sao lưu chỉ định."""
    try:
        backup_path = safe_backup_path(file_name)
        if not backup_path or not os.path.exists(backup_path):
            return False, "File không tồn tại"
        os.remove(backup_path)
        logger.info(f"Đã xóa file sao lưu: {file_name}")
        return True, "Đã xóa file sao lưu"
    except Exception as e:
        logger.error(f"Lỗi khi xóa file sao lưu: {e}")
        return False, str(e)
