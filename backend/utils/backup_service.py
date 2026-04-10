import os
import time
import asyncio
import sqlite3
import shutil
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backup_service")

# Mặc định sao lưu mỗi 24 giờ (86400 giây). Có thể chỉnh sửa qua biến môi trường.
BACKUP_INTERVAL_SECONDS = int(os.environ.get("BACKUP_INTERVAL_SECONDS", 86400))
# Tên file db gốc
DB_PATH = os.environ.get("DATABASE_URL", "sqlite:///./fras.db").replace("sqlite:///./", "")
# Thư mục lưu trữ sao lưu
BACKUP_DIR = "./backups"

async def auto_backup_task():
    """Chạy ngầm định kỳ sao lưu database"""
    if "sqlite" not in os.environ.get("DATABASE_URL", "sqlite"):
        logger.warning("Không sử dụng SQLite. Việc sao lưu CSDL nên được thực hiện bởi hệ quản trị CSDL (VD: PostgreSQL, MySQL).")
        return
        
    os.makedirs(BACKUP_DIR, exist_ok=True)
    logger.info(f"Bắt đầu dịch vụ tự động sao lưu định kỳ mỗi {BACKUP_INTERVAL_SECONDS/3600:.1f} giờ.")
    
    # Thực hiện 1 lần sao lưu ngay khi khởi động (nếu có dữ liệu)
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0:
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
            await asyncio.sleep(60) # Chờ 1 chút nếu gặp lỗi vòng lặp

def backup_db():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"fras_backup_{timestamp}.db"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Dọn dẹp bản cũ (giữ 7 bản gần nhất)
        cleanup_old_backups(keep_count=7)

        # Tránh lỗi nếu db chưa được tạo
        if os.path.exists(DB_PATH):
            import sqlite3
            source_conn = sqlite3.connect(DB_PATH)
            # Tạo file đích
            dest_conn = sqlite3.connect(backup_path)
            # Khóa và copy an toàn
            with source_conn, dest_conn:
                source_conn.backup(dest_conn)
            source_conn.close()
            dest_conn.close()
            logger.info(f"✅ Đã sao lưu cơ sở dữ liệu hệ thống thành công: {backup_path}")
            return backup_path
        else:
            logger.warning(f"Không tìm thấy file CSDL: {DB_PATH}")
            return None
    except Exception as e:
        logger.error(f"❌ Lỗi khi thực hiện sao lưu: {e}")
        return None

def cleanup_old_backups(keep_count=7):
    """Giữ lại 'keep_count' bản backup mới nhất để tránh đầy ổ cứng"""
    try:
        if not os.path.exists(BACKUP_DIR):
            return
        backups = []
        for f in os.listdir(BACKUP_DIR):
            if f.startswith("fras_backup_") and f.endswith(".db"):
                full_path = os.path.join(BACKUP_DIR, f)
                backups.append((full_path, os.path.getmtime(full_path)))
                
        # Sắp xếp theo ngày gần nhất
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # Chỉ giữ lại keep_count
        if len(backups) > keep_count:
            for old_file, _ in backups[keep_count:]:
                os.remove(old_file)
                logger.info(f"Đã dọn dẹp bản sao lưu cũ: {old_file}")
    except Exception as e:
        logger.error(f"Lỗi khi dọn dẹp bản backup cũ: {e}")
