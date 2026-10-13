import os
import sys
import csv
import re
import uuid
from datetime import datetime

# Fix console encoding
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base, SessionLocal
from models import User
from middleware.auth_middleware import hash_password

# 12 Internal System Categories and Code Map
# A: industrial
# B: warehouse
# C: mixed_residence
# D: hospitality
# E: medical_education
# F: fuel_gas
# G: transport
# H: residential
# I: construction
# J: office
# K: laboratory
# L: agriculture

CODE_TO_SYSTEM_TYPE = {
    "A": "industrial",
    "B": "warehouse",
    "C": "mixed_residence",
    "D": "hospitality",
    "E": "medical_education",
    "F": "fuel_gas",
    "G": "transport",
    "H": "residential",
    "I": "construction",
    "J": "office",
    "K": "laboratory",
    "L": "agriculture",
}

TYPE_MAPPING = {
    # A: Sản xuất công nghiệp
    "Công nghiệp nhẹ": "industrial",
    "Cơ sở luyện kim và cơ khí chế tạo": "industrial",
    "Cơ sở khác phục vụ sản xuất CN": "industrial",
    "Cơ sở sản xuất vật liệu, sản phẩm xây dựng": "industrial",
    "Nhà máy hóa dầu": "industrial,fuel_gas",
    "Nhà máy nước": "industrial",
    "Nhà máy xử lý chất thải": "industrial",
    "Nhà máy điện": "industrial",
    "Sơn, mực in": "industrial",
    "Sản phẩm cao su": "industrial",
    "Nguyên liệu nhựa": "industrial",
    "Hạ tầng cụm công nghiệp": "industrial",
    "Hạ tầng khu công nghiệp": "industrial",
    "Cơ sở khai thác, chế biến khoáng sản": "industrial,agriculture",

    # B: Kho hàng, kho vật liệu
    "Kho hàng nguy hiểm cháy nổ (A-E)": "warehouse",
    "KD hàng hóa dễ cháy ≥ 50m²": "warehouse,mixed_residence",
    "Hàng hóa khó cháy đựng bao bì dễ cháy ≥ 300m²": "warehouse",
    "Bãi chứa hàng ≥ 500m² (trừ xăng/dầu)": "warehouse",
    "Kho dầu": "warehouse,fuel_gas",
    "Kho dự trữ quốc gia": "warehouse",
    "Kho khí hóa lỏng": "warehouse,fuel_gas",
    "Kho vật liệu nổ, tiền chất": "warehouse,fuel_gas",

    # C: Nhà ở kết hợp sản xuất, kinh doanh
    "Nhà ở kết hợp sản xuất, kinh doanh (tổng diện tích phục vụ sản xuất, kinh doanh từ 50 m2 trở lên)": "mixed_residence",
    "Nhà đa năng, Nhà hỗn hợp (trừ Nhà ở kết hợp sản xuất, kinh doanh)": "mixed_residence,office",

    # D: Nhà hàng, khách sạn, chợ, TTTM, dịch vụ
    "Cơ sở nghỉ dưỡng, Cơ sở dịch vụ lưu trú khác": "hospitality",
    "Khách sạn, Nhà khách, Nhà nghỉ": "hospitality",
    "Dịch vụ ăn uống, khác": "hospitality",
    "Cơ sở kinh doanh dịch vụ karaoke, vũ trường": "hospitality",
    "Cơ sở kinh doanh dịch vụ vui chơi, giải trí": "hospitality",
    "Chợ": "hospitality",
    "Siêu thị (độc lập)": "hospitality",
    "Trung tâm thương mại (độc lập)": "hospitality",
    "Nhà hát, rạp chiếu phim, rạp xiếc": "hospitality",
    "Trung tâm hội nghị": "hospitality",
    "Nhà trưng bày; nhà triển lãm": "hospitality",
    "Hạ tầng khu du lịch, TDTT, đào tạo": "hospitality",
    "Sân vận động": "hospitality",
    "Nhà thi đấu, Nhà tập luyện các môn thể thao, bể bơi, Sân thi đấu các môn thể thao có khán đài": "hospitality",
    "Cơ sở thể thao khác (theo Luật thể dục, thể thao)": "hospitality",

    # E: Y tế, giáo dục
    "Bệnh viện": "medical_education",
    "Phòng khám đa khoa, chuyên khoa": "medical_education",
    "Trạm y tế, Nhà hộ sinh, Cơ sở Phòng chống dịch Bệnh, Cơ sở nghiên cứu, thí nghiệm chuyên ngành y tế": "medical_education",
    "Cơ sở y tế khác (theo Luật khám Bệnh, chữa Bệnh)": "medical_education",
    "Nhà điều dưỡng, phục hồi chức năng, chỉnh hình, Nhà dưỡng lão": "medical_education",
    "Cơ sở trợ giúp xã hội": "medical_education",
    "Nhà trẻ, trường mẫu giáo, mầm non": "medical_education",
    "Trường tiểu học": "medical_education",
    "Trường trung học Cơ sở": "medical_education",
    "Trường trung học phổ thông": "medical_education",
    "Trường phổ thông có nhiều cấp học": "medical_education",
    "Trường cao đẳng, đại học, học viện": "medical_education",
    "Trường dạy nghề": "medical_education",
    "Trường trung học chuyên nghiệp": "medical_education",
    "Cơ sở giáo dục khác (theo Luật giáo dục)": "medical_education",

    # F: Xăng dầu, khí gas, vật liệu nổ, hóa chất
    "Cửa hàng xăng dầu": "fuel_gas",
    "Cơ sở KD khí đốt": "fuel_gas",
    "Trạm chiết LPG": "fuel_gas",
    "Trạm phân phối khí": "fuel_gas",
    "Chất lỏng dễ cháy (khác xăng/dầu)": "fuel_gas",
    "Khí công nghiệp": "fuel_gas",
    "Nhiên liệu sinh học": "fuel_gas",
    "Nguồn điện hóa học (pin, ắc quy)": "fuel_gas",
    "Trạm biến áp ≥ 110kV": "fuel_gas",

    # G: Giao thông vận tải, phương tiện
    "Bến xe khách": "transport",
    "Ga, đề-pô đường sắt": "transport",
    "Cảng, bến thủy nội địa": "transport",
    "Nhà ga hành khách/ngoại giao": "transport",
    "Đài kiểm soát không lưu": "transport",
    "Nhà để xe, showroom ≥ 100m²": "transport",
    "Sửa chữa phương tiện đường bộ ≥ 100m²": "transport",
    "Trung tâm đăng kiểm": "transport",

    # H: Nhà ở, khu dân cư
    "Hạ tầng khu đô thị, nhà ở": "residential",
    "Nhà chung cư": "residential",
    "Nhà tập thể": "residential",

    # J: Trụ sở, cơ quan, văn hóa
    "Trụ sở, Nhà làm việc của doanh nghiệp, tổ chức chính trị, xã hội": "office",
    "Trụ sở làm việc của Cơ quan Nhà nước cấp xã": "office",
    "Trụ sở làm việc của Cơ quan Nhà nước cấp tỉnh": "office",
    "Trụ sở làm việc của Cơ quan Nhà nước cấp trung ương": "office",
    "Bưu cục": "office",
    "Bưu điện": "office",
    "Cơ sở cung cấp dịch vụ Bưu chính, viễn thông khác": "office",
    "Bảo tàng; thư viện": "office",
    "Cơ sở tôn giáo, tín ngưỡng": "office",
    "Nhà văn hóa": "office",
    "Cơ sở biểu diễn nghệ thuật, hoạt động văn hóa khác": "office",
    "Công trình di tích lịch sử - văn hóa cấp tỉnh trở lên": "office",

    # K: Nghiên cứu, công nghệ
    "Cơ sở nghiên cứu vũ Trụ, trung tâm Cơ sở dữ liệu chuyên ngành và Cơ sở nghiên cứu chuyên ngành khác": "laboratory",
    "Chất tẩy rửa": "laboratory,industrial",
    "Phân bón, hóa chất BVTV": "laboratory,industrial",
}

def parse_lat_lng(lat_str, lng_str):
    if not lat_str or not lng_str:
        return None, None
    lat_clean = re.sub(r'[^0-9]', '', str(lat_str))
    lng_clean = re.sub(r'[^0-9]', '', str(lng_str))
    if not lat_clean or not lng_clean:
        return None, None

    lat = None
    lng = None
    if lat_clean.startswith('2'):
        if len(lat_clean) >= 4:
            val = float(lat_clean[:2] + '.' + lat_clean[2:])
            if 20.0 <= val <= 23.0:
                lat = round(val, 6)

    if len(lng_clean) >= 5:
        if lng_clean.startswith('105') or lng_clean.startswith('106') or lng_clean.startswith('107') or lng_clean.startswith('10'):
            val = float(lng_clean[:3] + '.' + lng_clean[3:])
            if 105.0 <= val <= 108.0:
                lng = round(val, 6)

    return lat, lng

def run_import():
    csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'danh_sach_co_so_latest.csv')
    if not os.path.exists(csv_file):
        csv_file = 'danh_sach_co_so_latest.csv'
    
    print(f"📖 Reading facilities CSV from {csv_file}...")
    with open(csv_file, encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        rows = list(reader)[2:]

    db = SessionLocal()
    try:
        # Precompute standard bcrypt hash for Pc07@123
        print("🔐 Precomputing default password hash for Pc07@123...")
        default_pwd_hash = hash_password("Pc07@123")
        
        # Check existing codes to avoid duplicate inserts
        print("🔍 Checking existing accounts in database...")
        existing_codes = set(c[0] for c in db.query(User.facility_code).filter(User.facility_code.isnot(None)).all())
        print(f"Already in database: {len(existing_codes)} facility accounts")

        batch = []
        batch_size = 2000
        total_added = 0
        now = datetime.utcnow()

        for idx, r in enumerate(rows):
            if len(r) < 8:
                continue
            code = r[1].strip()
            if not code or not code.isdigit() or len(code) < 5:
                continue
            if code in existing_codes:
                continue
            
            team = r[0].strip()
            name = r[2].strip() or f"Cơ sở {code}"
            lat_raw = r[3].strip()
            lng_raw = r[4].strip()
            province = r[5].strip() or "Tỉnh Bắc Ninh"
            ward = r[6].strip()
            raw_type = r[7].strip()

            lat, lng = parse_lat_lng(lat_raw, lng_raw)

            # Determine facility_types:
            # If no type in list: store empty string or "Chưa có loại hình"
            # If mapped: store comma-separated system types (e.g., "industrial", "warehouse,fuel_gas")
            if not raw_type:
                ftypes = "Chưa có loại hình"
            else:
                ftypes = TYPE_MAPPING.get(raw_type, "mixed_residence")

            u_dict = {
                "id": str(uuid.uuid4()),
                "email": f"{code}@fras.vn",
                "facility_code": code,
                "password_hash": default_pwd_hash,
                "full_name": name,
                "organization": team or "Cơ sở thuộc diện quản lý PCCC",
                "phone": None,
                "province": province,
                "ward": ward,
                "latitude": lat,
                "longitude": lng,
                "facility_types": ftypes,
                "role": "user",
                "is_active": True,
                "is_locked": False,
                "created_at": now,
                "updated_at": now,
            }
            batch.append(u_dict)
            existing_codes.add(code)

            if len(batch) >= batch_size:
                db.bulk_insert_mappings(User, batch)
                db.commit()
                total_added += len(batch)
                print(f"  Inserted {total_added} facilities...")
                batch = []

        if batch:
            db.bulk_insert_mappings(User, batch)
            db.commit()
            total_added += len(batch)

        print(f"🎉 Import complete! Successfully inserted {total_added} facilities.")
        total_users = db.query(User).count()
        facilities_with_coords = db.query(User).filter(User.latitude.isnot(None), User.facility_code.isnot(None)).count()
        facilities_without_coords = db.query(User).filter(User.latitude.is_(None), User.facility_code.isnot(None)).count()
        print(f"📊 Total users in DB: {total_users}")
        print(f"📍 Facilities with coordinates: {facilities_with_coords}")
        print(f"⚪ Facilities without coordinates (pending GPS): {facilities_without_coords}")

    finally:
        db.close()

if __name__ == '__main__':
    run_import()
