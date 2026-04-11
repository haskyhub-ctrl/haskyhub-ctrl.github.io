import sqlite3
import uuid
import random
from datetime import datetime, timedelta

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

# Province configs for Bac Ninh and Bac Giang
# Coordinates: lat between min_max lat, lng between min_max lng
PROVINCES = [
    {
        "name": "Bắc Ninh",
        "districts": [
            "TP Bắc Ninh", "TX Từ Sơn", "Huyện Yên Phong", "Huyện Quế Võ",
            "Huyện Thuận Thành", "Huyện Gia Bình", "Huyện Lương Tài",
            "Huyện Kim Thanh"
        ],
        "lat_min": 21.05, "lat_max": 21.28,
        "lng_min": 105.90, "lng_max": 106.15
    },
    {
        "name": "Bắc Giang",
        "districts": [
            "TP Bắc Giang", "TX Việt Yên", "TX Yên Dũng", "Huyện Tân Yên",
            "Huyện Lạng Giang", "Huyện Lục Nam", "Huyện Lục Ngạn",
            "Huyện Sơn Động", "Huyện Yên Thế", "Huyện Hiệp Hòa"
        ],
        "lat_min": 21.10, "lat_max": 21.55,
        "lng_min": 106.00, "lng_max": 106.50
    }
]

FACILITY_TYPES = [
    "Cơ sở sản xuất công nghiệp", "Kho hàng, kho vật liệu",
    "Nhà ở kết hợp kinh doanh", "Nhà hàng, khách sạn, chợ, TTTM",
    "Bệnh viện, trường học, cơ sở y tế", "Xăng dầu, khí gas, vật liệu nổ",
    "Phương tiện giao thông", "Khu dân cư, nhà trọ, nhà ở",
    "Công trình xây dựng đang thi công", "Cơ quan, văn phòng, trụ sở",
    "Nghiên cứu, phòng thí nghiệm", "Nông nghiệp, chế biến nông lâm sản"
]

# Street names
STREETS = [
    "Đường Quốc lộ 1", "Đường Trần Phú", "Đường Lê Lợi", "Đường Nguyễn Trãi",
    "Đường Trần Hưng Đạo", "Đường Phan Đình Giót", "Đường Võ Nguyên Giáp",
    "Đường Chu Văn An", "Đường Hoàng Quốc Việt", "Đường Phạm Văn Đồng",
    "KCN Quế Võ", "KCN Yên Phong", "KCN Tiên Sơn", "KCN Hòa Mỹ",
    "KCN Đại Đồng", "Đại lộ Bắc Ninh", "Đường vành đai", "Đường tỉnh lộ 287",
    "Đường tỉnh lộ 295", "Đường Văn Lâm"
]

now = datetime.utcnow()
now_iso = now.isoformat()

print("Generating 1000 random assessments...")

for i in range(1, 1001):
    # Random province
    province = random.choice(PROVINCES)
    # Random district within province
    district = random.choice(province["districts"])

    # Random coordinates within province bounds
    lat = random.uniform(province["lat_min"], province["lat_max"])
    lng = random.uniform(province["lng_min"], province["lng_max"])

    # Random facility type
    facility_type = random.choice(FACILITY_TYPES)

    # Random street
    street = random.choice(STREETS)
    address = f"{street}, {district}, {province['name']}"

    # Random score: 0-100
    score = random.randint(0, 100)
    risk_pct = score

    # Determine risk level based on score
    if score < 25:
        risk = "low"
    elif score < 50:
        risk = "medium"
    elif score < 75:
        risk = "high"
    else:
        risk = "critical"

    # Random area (m2)
    area = random.randint(50, 5000)

    # Random worker count
    workers = random.randint(5, 500)

    # Random completed date within last 180 days
    days_ago = random.randint(0, 180)
    completed_date = now - timedelta(days=days_ago)
    completed_iso = completed_date.isoformat()
    started_iso = (completed_date - timedelta(hours=random.randint(1, 48))).isoformat()

    aid = generate_uuid()
    facility_name = f"Cơ sở test {i}"

    cursor.execute("""
        INSERT INTO assessments
        (id, user_id, facility_name, facility_type, facility_address,
         facility_area, worker_count, total_score, max_possible_score,
         risk_level, risk_percentage, status, latitude, longitude,
         started_at, completed_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        aid, user_id, facility_name, facility_type, address,
        area, workers, score, 100,
        risk, risk_pct, "completed", lat, lng,
        started_iso, completed_iso, completed_iso
    ))

    if i % 100 == 0:
        print(f"  ... generated {i}/1000")

conn.commit()
print("✅ Done! Inserted 1000 random assessments across Bắc Ninh and Bắc Giang.")
conn.close()
