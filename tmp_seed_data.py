import sqlite3
import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

db_path = "backend/fras.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the admin user id
cursor.execute("SELECT id FROM users WHERE email='admin@fras.vn'")
row = cursor.fetchone()
if not row:
    print("Admin user not found. Please run the backend once first to seed users.")
    conn.close()
    exit(1)
user_id = row[0]

# Sample data in Bac Ninh region (approx 21.18, 106.06)
sample_data = [
    ("Công ty May Bắc Ninh", "KCN Quế Võ, Bắc Ninh", 75, "high", 21.18, 106.07),
    ("Xưởng sản xuất đồ gỗ", "Đồng Kỵ, Từ Sơn, Bắc Ninh", 45, "medium", 21.12, 106.00),
    ("Nhà máy Điện tử Samsung", "KCN Yên Phong, Bắc Ninh", 10, "low", 21.21, 105.95),
    ("Chợ đêm Bắc Ninh", "Tiền An, Bắc Ninh", 90, "critical", 21.18, 106.06),
    ("Kho xăng dầu Kinh Bắc", "Quế Võ, Bắc Ninh", 85, "critical", 21.15, 106.12),
]

now = datetime.utcnow().isoformat()

for name, addr, score, risk, lat, lng in sample_data:
    aid = generate_uuid()
    cursor.execute("""
        INSERT INTO assessments 
        (id, user_id, facility_name, facility_address, total_score, max_possible_score, risk_level, risk_percentage, status, latitude, longitude, started_at, completed_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (aid, user_id, name, addr, score, 100, risk, score, "completed", lat, lng, now, now, now))

conn.commit()
print(f"✅ Seeded {len(sample_data)} sample assessments in Bac Ninh.")
conn.close()
