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

def get_db_info():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url or "sqlite" in db_url:
        try:
            from dotenv import load_dotenv
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env_file = os.path.join(backend_dir, ".env")
            if os.path.exists(env_file):
                load_dotenv(env_file, override=True)
                db_url = os.environ.get("DATABASE_URL")
        except Exception:
            pass
    return db_url or "sqlite:///./fras.db"

async def auto_backup_task():
    """Chạy ngầm định kỳ sao lưu database (hỗ trợ cả PostgreSQL và SQLite)."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    logger.info(f"Bắt đầu dịch vụ tự động sao lưu định kỳ mỗi {BACKUP_INTERVAL_SECONDS/3600:.1f} giờ.")
    
    # Thực hiện 1 lần sao lưu khi khởi động
    backup_db()
        
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
        cleanup_old_backups(keep_count=10)
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

def cleanup_old_backups(keep_count=10):
    """Giữ lại 'keep_count' bản backup mới nhất để tránh đầy ổ cứng."""
    try:
        if not os.path.exists(BACKUP_DIR):
            return
        backups = []
        valid_exts = (".db", ".sql", ".dump", ".sql.gz")
        for f in os.listdir(BACKUP_DIR):
            if f.startswith("fras_backup_") and any(f.endswith(ext) for ext in valid_exts):
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
