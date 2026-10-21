"""Đọc, chuẩn hóa và nạp danh sách cơ sở thuộc diện quản lý (file danh_sach_co_so_latest.csv).

File này là bản xuất (CSV) từ bảng tính danh sách cơ sở: 3 dòng đầu là tiêu đề, các cột theo thứ tự
  0 Đội quản lý | 1 Mã cơ sở | 2 Tên cơ sở | 3 Vĩ độ | 4 Kinh độ | 5 Tỉnh thành | 6 Phường xã | 7 Loại hình |
  8 Tổng diện tích khu đất | 9 Tổng diện tích xây dựng | 10 Số người làm việc trong giờ hành chính |
  11 Số người làm việc ngoài giờ hành chính.
Tọa độ ghi theo kiểu Việt Nam (dấu phẩy thập phân: "21,220896"), có dòng 0 hoặc để trống.
"""
import csv
import os
import re
import uuid
from datetime import datetime

NO_TEAM_LABEL = "Chưa phân đội"
DEFAULT_PASSWORD = "Pc07@123"

# Vùng địa lý hợp lệ (Bắc Ninh sau khi hợp nhất với Bắc Giang), dùng để loại tọa độ nhập sai
LAT_RANGE = (20.8, 22.2)
LNG_RANGE = (105.3, 107.4)

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


def csv_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "..", "danh_sach_co_so_latest.csv"),
              os.path.join(here, "..", "danh_sach_co_so_latest.csv"),
              os.path.join(os.getcwd(), "danh_sach_co_so_latest.csv"),
              os.path.join(os.getcwd(), "..", "danh_sach_co_so_latest.csv")):
        if os.path.exists(p):
            return os.path.abspath(p)
    return ""


def _decimal(text):
    """Đọc số thập phân kiểu Việt Nam ("21,220896") hoặc kiểu quốc tế ("21.220896")."""
    s = (text or "").strip().replace(" ", "")
    if not s:
        return None
    if "," in s and "." in s:            # "1.234,56": dấu chấm là phân cách hàng nghìn
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def parse_coords(lat_text, lng_text):
    """Trả về (lat, lng) hợp lệ hoặc (None, None) nếu trống, bằng 0, ngoài vùng hay không đọc được."""
    lat, lng = _decimal(lat_text), _decimal(lng_text)
    if not lat or not lng:
        return None, None
    if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1] and LNG_RANGE[0] <= lng <= LNG_RANGE[1]):
        return None, None
    return round(lat, 6), round(lng, 6)


def _int(text):
    v = _decimal(text)
    return int(round(v)) if v is not None else None


def normalize_province(text):
    t = (text or "").strip()
    if not t or t.lower() in ("bắc ninh", "tỉnh bắc ninh"):
        return "Tỉnh Bắc Ninh"
    return t[:100]


def row_to_record(row):
    """Một dòng CSV thành dict đã chuẩn hóa; None nếu dòng không có mã cơ sở hợp lệ."""
    if len(row) < 8:
        return None
    code = row[1].strip()
    if not code.isdigit() or len(code) < 5:
        return None
    lat, lng = parse_coords(row[3], row[4])
    raw_type = row[7].strip()
    cell = lambda i: row[i] if len(row) > i else ""
    return {
        "code": code,
        "team": (row[0].strip() or NO_TEAM_LABEL)[:300],
        "name": (row[2].strip() or f"Cơ sở {code}")[:500],
        "lat": lat,
        "lng": lng,
        "coords_raw": bool((row[3].strip() and row[4].strip()) and _decimal(row[3]) and _decimal(row[4])),
        "province": normalize_province(row[5]),
        "ward": row[6].strip()[:100],
        "type_label": raw_type[:300],
        "facility_types": TYPE_MAPPING.get(raw_type, "mixed_residence") if raw_type else "Chưa có loại hình",
        "land_area": _decimal(cell(8)),
        "built_area": _decimal(cell(9)),
        "workers_office": _int(cell(10)),
        "workers_after": _int(cell(11)),
    }


_WARD_RE = re.compile(r"^(xã|phường|thị trấn)\s+(.+)$", re.I)


def _ward_key(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def normalize_wards(records):
    """Thống nhất tên xã phường: ô thì ghi "Xã Đại Đồng", ô thì chỉ "Đại Đồng", ô thì ghi thường.
    Lấy tiền tố (Xã hoặc Phường) và cách viết phổ biến nhất của chính tên đó trong danh sách để gán cho mọi dòng."""
    from collections import Counter, defaultdict
    prefixes = defaultdict(Counter)
    spellings = defaultdict(Counter)
    for r in records:
        m = _WARD_RE.match(re.sub(r"\s+", " ", r["ward"]).strip())
        if m:
            key = _ward_key(m.group(2))
            prefixes[key][m.group(1).lower()] += 1
            spellings[key][re.sub(r"\s+", " ", m.group(2)).strip()] += 1
    canon = {}
    for key, cnt in prefixes.items():
        prefix = cnt.most_common(1)[0][0]
        best = max(spellings[key].items(), key=lambda kv: (kv[0] != kv[0].lower(), kv[1]))[0]
        canon[key] = f"{prefix.capitalize()} {best}"
    changed = 0
    for r in records:
        raw = re.sub(r"\s+", " ", r["ward"]).strip()
        m = _WARD_RE.match(raw)
        key = _ward_key(m.group(2) if m else raw)
        new = canon.get(key, raw)
        if new != r["ward"]:
            changed += 1
        r["ward"] = new
    return changed


def load_records(path=None):
    """Đọc toàn bộ file CSV. Trả về (records, bao_cao). Dòng trùng mã giữ dòng cuối."""
    path = path or csv_path()
    stats = {"rows": 0, "no_code": 0, "duplicate_code": 0, "no_coords": 0, "bad_coords": 0}
    by_code = {}
    with open(path, encoding="utf-8-sig", errors="replace", newline="") as f:
        for i, row in enumerate(csv.reader(f)):
            if i < 3 or not any(c.strip() for c in row):      # 3 dòng tiêu đề, dòng trống
                continue
            stats["rows"] += 1
            rec = row_to_record(row)
            if not rec:
                stats["no_code"] += 1
                continue
            if rec["lat"] is None:
                stats["bad_coords" if rec["coords_raw"] else "no_coords"] += 1
            if rec["code"] in by_code:
                stats["duplicate_code"] += 1
            by_code[rec["code"]] = rec
    records = list(by_code.values())
    stats["ward_fixed"] = normalize_wards(records)
    return records, stats


_csv_index = {"sig": None, "map": {}}


def find_in_csv(code: str):
    """Tra một mã cơ sở trong file CSV (nạp một lần vào bộ nhớ, tự nạp lại khi file đổi)."""
    path = csv_path()
    if not path:
        return None
    sig = (path, os.path.getmtime(path))
    if _csv_index["sig"] != sig:
        try:
            recs, _ = load_records(path)
            _csv_index["map"] = {r["code"]: r for r in recs}
            _csv_index["sig"] = sig
        except Exception:
            return None
    return _csv_index["map"].get(code)


def user_fields(rec: dict) -> dict:
    """Các trường của bảng users lấy từ một bản ghi cơ sở."""
    return {
        "full_name": rec["name"],
        "organization": rec["team"],
        "management_team": rec["team"],
        "province": rec["province"],
        "ward": rec["ward"],
        "latitude": rec["lat"],
        "longitude": rec["lng"],
        "facility_types": rec["facility_types"],
        "facility_type_label": rec["type_label"] or None,
        "land_area": rec["land_area"],
        "built_area": rec["built_area"],
        "workers_office": rec["workers_office"],
        "workers_after": rec["workers_after"],
    }


def new_user_mapping(rec: dict, password_hash: str, now=None) -> dict:
    now = now or datetime.utcnow()
    d = {
        "id": str(uuid.uuid4()),
        "email": f"{rec['code']}@fras.vn",
        "facility_code": rec["code"],
        "password_hash": password_hash,
        "phone": None,
        "role": "user",
        "is_active": True,
        "is_locked": False,
        "created_at": now,
        "updated_at": now,
    }
    d.update(user_fields(rec))
    return d
