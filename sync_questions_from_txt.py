"""
Parse danh_sach_cau_hoi_duyet.txt (user-approved) and generate
seed_data.py + seed_data_specific.py for the backend.

This is the SINGLE SOURCE OF TRUTH for all FRAS questions.

Scoring logic v2 — Variable scoring per question:
 - Câu ảnh hưởng TRỰC TIẾP đến nguy cơ cháy nổ: A=0, B=1, C=2, D=3
 - Câu ảnh hưởng GIÁN TIẾP / chỉ số phát hiện: A=0, B=1, C=2, D=2
 - Câu mang tính phòng ngừa / chuẩn bị / hiểu biết: A=0, B=0, C=1, D=2
"""
import re, os, json, pprint

TXT_FILE = "danh_sach_cau_hoi_duyet.txt"
SEED_COMMON = os.path.join("backend", "seed_data.py")
SEED_SPECIFIC = os.path.join("backend", "seed_data_specific.py")

# ========== BẢNG ĐIỂM TÙY BIẾN THEO ID CÂU HỎI ==========
# Mặc định: A=0, B=1, C=2, D=3 (nguy cơ trực tiếp cao)
# "medium": A=0, B=1, C=2, D=2 (ảnh hưởng gián tiếp, chỉ báo gián tiếp)
# "low":    A=0, B=0, C=1, D=2 (mang tính hiểu biết, phòng ngừa, khó thay đổi)

SCORE_PROFILES = {
    # === NHÓM 1: HỆ THỐNG ĐIỆN ===
    # ID1-ID8: Nguy cơ trực tiếp → mặc định (A0 B1 C2 D3)
    # ID9: Hóa đơn tiền điện tăng = chỉ báo gián tiếp, không trực tiếp gây cháy
    9: "medium",
    # ID10: Chuột gặm dây = nguy cơ trung bình, phụ thuộc nhiều yếu tố
    10: "medium",
    # ID11-ID12: Vật dễ cháy gần điện, thiết bị nung nóng → mặc định
    # ID20: Điều hòa, tủ lạnh bất thường → mặc định

    # === NHÓM 2: NGUỒN LỬA/NHIỆT ===
    # ID13-ID19: phần lớn nguy cơ trực tiếp → mặc định
    # ID19: Lửa trại, nướng ngoài trời = nguy cơ tùy tình huống
    19: "medium",

    # === NHÓM 3: LỐI THOÁT NẠN & PCCC ===
    # ID21-ID22: Trực tiếp ảnh hưởng an toàn → mặc định
    # ID25: Biết đường thoát nạn/sơ đồ = phòng ngừa, hiểu biết
    25: "low",
    # ID26: Hàng hóa chật → mặc định

    # === NHÓM 4: MÁY MÓC ===
    # ID27-ID33: Máy móc bất thường → mặc định

    # === NHÓM 5: THIÊN NHIÊN ===
    # ID34: Gần rừng = yếu tố môi trường, không thể thay đổi
    34: "low",
    # ID35: Vật liệu nhà = yếu tố cấu trúc, khó thay đổi
    35: "medium",
    # ID36-ID38: Ảnh hưởng thời tiết → mặc định

    # === NHÓM 6: NGUY CƠ TỰ CHÁY ===
    # ID39-ID45: Phần lớn trực tiếp → mặc định
    # ID44: Phân bón, phế phẩm hữu cơ = khá chuyên biệt
    44: "medium",

    # === NHÓM 7: PHƯƠNG TIỆN GIAO THÔNG ===
    # ID46-ID50: mặc định
    # ID47: Xe chắn lối thoát = liên quan lối thoát → mặc định

    # === NHÓM 8: NGUY CƠ BỔ SUNG ===
    # ID53: Camera, hàng rào = phòng chống phá hoại, gián tiếp
    53: "low",
    # ID54: Đèn lễ hội = tình huống thỉnh thoảng
    54: "medium",
    # ID55: Biết gọi 114 = kiến thức, phòng ngừa
    55: "low",

    # === CÂU HỎI ĐẶC THÙ ===
    # Phần lớn trực tiếp → mặc định
    # Một số câu hiểu biết/quy trình
    65: "low",    # Công nhân nhận biết dấu hiệu = kiến thức
    72: "medium", # Bảo vệ kiểm tra cuối ngày = quy trình
    80: "low",    # Trẻ em biết đường thoát = phòng ngừa
    82: "low",    # Diễn tập thoát nạn ban đêm = phòng ngừa
    92: "low",    # Trường diễn tập sơ tán = phòng ngừa
    97: "low",    # Nhân viên ca đêm biết quy trình = kiến thức
    110: "low",   # Chủ nhà dán sơ đồ, phổ biến = phòng ngừa
}

def get_score_map(qid):
    """Trả về bảng điểm A/B/C/D tùy theo ID câu hỏi."""
    profile = SCORE_PROFILES.get(qid, "high")
    if profile == "high":
        return {"A": 0, "B": 1, "C": 2, "D": 3}
    elif profile == "medium":
        return {"A": 0, "B": 1, "C": 2, "D": 2}
    elif profile == "low":
        return {"A": 0, "B": 0, "C": 1, "D": 2}
    return {"A": 0, "B": 1, "C": 2, "D": 3}

def get_risk_map(qid):
    """Trả về mức nguy cơ A/B/C/D tùy theo profile."""
    profile = SCORE_PROFILES.get(qid, "high")
    if profile == "low":
        return {"A": "safe", "B": "safe", "C": "low", "D": "high"}
    elif profile == "medium":
        return {"A": "safe", "B": "low", "C": "high", "D": "high"}
    else:
        return {"A": "safe", "B": "low", "C": "high", "D": "critical"}

# ========== 1. PARSE TXT FILE ==========
with open(TXT_FILE, encoding="utf-8") as f:
    content = f.read()

# Split into PHAN 1 and PHAN 2
parts = re.split(r'={10,}\s*\n\s*PHẦN 2:', content)
phan1_text = parts[0]
phan2_text = "PHẦN 2:" + parts[1] if len(parts) > 1 else ""

def parse_questions(text):
    """Parse questions from a section of text. Returns list of (group_name, [questions])"""
    groups = []
    current_group = None
    current_questions = []
    
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Group header
        if line.startswith('--- NHÓM:'):
            if current_group and current_questions:
                groups.append((current_group, current_questions))
            gname = line.replace('--- NHÓM:', '').replace('---', '').strip()
            current_group = gname
            current_questions = []
            i += 1
            continue
        
        # Question line: ID123. text...
        m = re.match(r'ID(\d+)\.\s*(.+)', line)
        if m:
            qid = int(m.group(1))
            qtext = m.group(2).strip()
            options = []
            score_map = get_score_map(qid)
            risk_map = get_risk_map(qid)
            i += 1
            # Read options A, B, C, D
            while i < len(lines):
                oline = lines[i].strip()
                om = re.match(r'^([A-D])\.\s*(.+)', oline)
                if om:
                    okey = om.group(1)
                    otext = om.group(2).strip()
                    options.append({
                        "key": okey,
                        "text": otext,
                        "score": score_map[okey],
                        "risk": risk_map[okey],
                    })
                    i += 1
                elif oline == '' or oline.startswith('---') or oline.startswith('===') or re.match(r'ID\d+\.', oline):
                    break
                else:
                    i += 1
            current_questions.append({"id": qid, "text": qtext, "options": options})
            continue
        
        i += 1
    
    if current_group and current_questions:
        groups.append((current_group, current_questions))
    
    return groups

common_groups = parse_questions(phan1_text)
specific_groups = parse_questions(phan2_text)

print(f"=== Parsed from {TXT_FILE} ===")
total_common = 0
for gname, qs in common_groups:
    max_pts = sum(max(o["score"] for o in q["options"]) for q in qs)
    print(f"  Common: {gname} -> {len(qs)} questions (max={max_pts})")
    total_common += len(qs)
total_specific = 0
for gname, qs in specific_groups:
    max_pts = sum(max(o["score"] for o in q["options"]) for q in qs)
    print(f"  Specific: {gname} -> {len(qs)} questions (max={max_pts})")
    total_specific += len(qs)
print(f"  TOTAL: {total_common} common + {total_specific} specific = {total_common + total_specific}")

# Print scoring summary
print(f"\n=== Scoring Profile Summary ===")
for qid, profile in sorted(SCORE_PROFILES.items()):
    print(f"  ID{qid}: {profile}")
print(f"  Others: high (default A=0 B=1 C=2 D=3)")

# ========== 2. CATEGORY METADATA ==========
# Icons and colors for common categories
COMMON_CAT_META = {
    "DẤU HIỆU NGUY CƠ TỪ HỆ THỐNG ĐIỆN": {"icon": "⚡", "color": "#e74c3c"},
    "NGUY CƠ TỪ NGUỒN LỬA/NHIỆT": {"icon": "🔥", "color": "#e67e22"},
    "LỐI THOÁT NẠN VÀ TRANG BỊ PCCC": {"icon": "🚪", "color": "#2ecc71"},
    "DẤU HIỆU BẤT THƯỜNG TỪ MÁY MÓC": {"icon": "⚙️", "color": "#3498db"},
    "TÁC ĐỘNG TỪ THIÊN NHIÊN": {"icon": "🌿", "color": "#27ae60"},
    "NGUY CƠ TỰ CHÁY": {"icon": "💥", "color": "#9b59b6"},
    "PHƯƠNG TIỆN GIAO THÔNG": {"icon": "🚗", "color": "#1abc9c"},
    "NGUY CƠ BỔ SUNG": {"icon": "⚠️", "color": "#f39c12"},
}

COMMON_CAT_NAMES_VI = {
    "DẤU HIỆU NGUY CƠ TỪ HỆ THỐNG ĐIỆN": "Dấu hiệu nguy cơ từ hệ thống điện",
    "NGUY CƠ TỪ NGUỒN LỬA/NHIỆT": "Nguy cơ từ nguồn lửa/nhiệt",
    "LỐI THOÁT NẠN VÀ TRANG BỊ PCCC": "Lối thoát nạn và trang bị PCCC",
    "DẤU HIỆU BẤT THƯỜNG TỪ MÁY MÓC": "Dấu hiệu bất thường từ máy móc",
    "TÁC ĐỘNG TỪ THIÊN NHIÊN": "Tác động từ thiên nhiên",
    "NGUY CƠ TỰ CHÁY": "Nguy cơ tự cháy",
    "PHƯƠNG TIỆN GIAO THÔNG": "Phương tiện giao thông",
    "NGUY CƠ BỔ SUNG": "Nguy cơ bổ sung",
}

# Map specific group name to facility type code
SPECIFIC_FACILITY_MAP = {
    "ĐẶC THÙ: SẢN XUẤT CÔNG NGHIỆP": "A",
    "ĐẶC THÙ: KHO HÀNG, KHO VẬT LIỆU": "B",
    "ĐẶC THÙ: NHÀ Ở KẾT HỢP KINH DOANH": "C",
    "ĐẶC THÙ: NHÀ HÀNG, KHÁCH SẠN, CHỢ, TTTM": "D",
    "ĐẶC THÙ: BỆNH VIỆN, TRƯỜNG HỌC, CƠ SỞ Y TẾ": "E",
    "ĐẶC THÙ: XĂNG DẦU, KHÍ GAS, VẬT LIỆU NỔ": "F",
    "ĐẶC THÙ: PHƯƠNG TIỆN GIAO THÔNG": "G",
    "ĐẶC THÙ: KHU DÂN CƯ, NHÀ TRỌ, NHÀ Ở": "H",
    "ĐẶC THÙ: CÔNG TRÌNH XÂY DỰNG ĐANG THI CÔNG": "I",
    "ĐẶC THÙ: CƠ QUAN, VĂN PHÒNG, TRỤ SỞ": "J",
    "ĐẶC THÙ: NGHIÊN CỨU, PHÒNG THÍ NGHIỆM": "K",
    "ĐẶC THÙ: NÔNG NGHIỆP, CHẾ BIẾN NÔNG LÂM SẢN": "L",
}

SPECIFIC_ICONS = {
    "A": "🏭", "B": "📦", "C": "🏠", "D": "🏪", "E": "🏥",
    "F": "⛽", "G": "🚌", "H": "🏘️", "I": "🏗️", "J": "🏢",
    "K": "🔬", "L": "🌾",
}
SPECIFIC_COLORS = {
    "A": "#e74c3c", "B": "#e67e22", "C": "#f39c12", "D": "#2ecc71",
    "E": "#3498db", "F": "#9b59b6", "G": "#1abc9c", "H": "#e74c3c",
    "I": "#e67e22", "J": "#3498db", "K": "#9b59b6", "L": "#27ae60",
}

FACILITY_TYPES = [
    {"name": "Cơ sở sản xuất công nghiệp", "code": "A"},
    {"name": "Kho hàng, kho vật liệu", "code": "B"},
    {"name": "Nhà ở kết hợp kinh doanh", "code": "C"},
    {"name": "Nhà hàng, khách sạn, chợ, TTTM", "code": "D"},
    {"name": "Bệnh viện, trường học, cơ sở y tế", "code": "E"},
    {"name": "Xăng dầu, khí gas, vật liệu nổ", "code": "F"},
    {"name": "Phương tiện giao thông", "code": "G"},
    {"name": "Khu dân cư, nhà trọ, nhà ở", "code": "H"},
    {"name": "Công trình xây dựng đang thi công", "code": "I"},
    {"name": "Cơ quan, văn phòng, trụ sở", "code": "J"},
    {"name": "Nghiên cứu, phòng thí nghiệm", "code": "K"},
    {"name": "Nông nghiệp, chế biến nông lâm sản", "code": "L"},
]

# ========== 3. GENERATE seed_data.py ==========
with open(SEED_COMMON, "w", encoding="utf-8") as f:
    f.write('"""\nFRAS Question Database - Common Questions\n')
    f.write('AUTO-GENERATED from danh_sach_cau_hoi_duyet.txt\n')
    f.write('DO NOT EDIT MANUALLY - Edit the txt file and re-run sync_questions_from_txt.py\n')
    f.write('\nScoring logic v2:\n')
    f.write('  - "high" (default): A=0, B=1, C=2, D=3 (nguy co truc tiep)\n')
    f.write('  - "medium":         A=0, B=1, C=2, D=2 (anh huong gian tiep)\n')
    f.write('  - "low":            A=0, B=0, C=1, D=2 (phong ngua, hieu biet)\n')
    f.write('"""\n\n')
    
    # FACILITY_TYPES
    f.write(f"FACILITY_TYPES = {json.dumps(FACILITY_TYPES, ensure_ascii=False, indent=4)}\n\n")
    
    # COMMON_CATEGORIES with metadata
    categories = []
    for idx, (gname, qs) in enumerate(common_groups):
        meta = COMMON_CAT_META.get(gname, {"icon": "❓", "color": "#95a5a6"})
        max_score = sum(max(o["score"] for o in q["options"]) for q in qs)
        cat = {
            "name": COMMON_CAT_NAMES_VI.get(gname, gname),
            "description": f"Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - {gname.lower()}",
            "icon": meta["icon"],
            "color": meta["color"],
            "order_index": idx + 1,
            "max_score": max_score,
        }
        categories.append(cat)
    
    f.write(f"COMMON_CATEGORIES = {json.dumps(categories, ensure_ascii=False, indent=4)}\n\n")
    
    # Write each group
    for idx, (gname, qs) in enumerate(common_groups):
        varname = f"GROUP{idx+1}_QUESTIONS"
        # Strip the internal IDs, only keep text and options
        clean_qs = [{"text": q["text"], "options": q["options"]} for q in qs]
        f.write(f"{varname} = {json.dumps(clean_qs, ensure_ascii=False, indent=4)}\n\n")
    
    # ALL_COMMON_QUESTIONS
    f.write("ALL_COMMON_QUESTIONS = [\n")
    for idx in range(len(common_groups)):
        f.write(f"    ({idx}, GROUP{idx+1}_QUESTIONS),\n")
    f.write("]\n")

print(f"✅ Generated {SEED_COMMON} ({len(common_groups)} groups, {total_common} questions)")

# ========== 4. GENERATE seed_data_specific.py ==========
with open(SEED_SPECIFIC, "w", encoding="utf-8") as f:
    f.write('"""\nFRAS Question Database - Specific Questions by Facility Type\n')
    f.write('AUTO-GENERATED from danh_sach_cau_hoi_duyet.txt\n')
    f.write('DO NOT EDIT MANUALLY - Edit the txt file and re-run sync_questions_from_txt.py\n"""\n\n')
    
    all_specs = []
    for gname, qs in specific_groups:
        ftype = SPECIFIC_FACILITY_MAP.get(gname, "all")
        icon = SPECIFIC_ICONS.get(ftype, "❓")
        color = SPECIFIC_COLORS.get(ftype, "#95a5a6")
        
        # Clean name: "ĐẶC THÙ: SẢN XUẤT CÔNG NGHIỆP" -> "Đặc thù: Sản xuất công nghiệp"
        clean_name = gname.replace("ĐẶC THÙ: ", "Đặc thù: ")
        
        max_score = sum(max(o["score"] for o in q["options"]) for q in qs)
        
        spec_var = f"SPECIFIC_CATEGORY_{ftype}"
        spec_data = {
            "name": clean_name,
            "description": f"Dấu hiệu nguy cơ cháy nổ - {clean_name.lower()}",
            "facility_type": ftype,
            "icon": icon,
            "color": color,
            "questions": [{"text": q["text"], "options": q["options"]} for q in qs],
        }
        all_specs.append((spec_var, spec_data))
        f.write(f"{spec_var} = {json.dumps(spec_data, ensure_ascii=False, indent=4)}\n\n")
    
    # ALL_SPECIFIC_CATEGORIES list
    f.write("ALL_SPECIFIC_CATEGORIES = [\n")
    for spec_var, _ in all_specs:
        f.write(f"    {spec_var},\n")
    f.write("]\n")

print(f"✅ Generated {SEED_SPECIFIC} ({len(specific_groups)} groups, {total_specific} questions)")
print(f"\n🎯 TOTAL: {total_common + total_specific} questions")
print(f"\n⚠️  Next: Delete fras.db and restart server to apply new questions")
