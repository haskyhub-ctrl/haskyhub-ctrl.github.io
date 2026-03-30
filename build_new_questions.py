import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Import all new question data
from new_questions_common import GROUP1, GROUP2, GROUP3
from new_questions_common2 import GROUP4, GROUP5, GROUP6, GROUP7, GROUP8
from new_questions_specific1 import SPEC_C, SPEC_H
from new_questions_specific2 import SPEC_A, SPEC_B
from new_questions_specific3 import SPEC_D, SPEC_E, SPEC_F, SPEC_G, SPEC_I, SPEC_J, SPEC_K, SPEC_L

# ===== COMMON CATEGORIES =====
COMMON_CATEGORIES = [
    {"name": "Dấu hiệu nguy cơ từ hệ thống điện", "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ do hệ thống điện"},
    {"name": "Nguy cơ từ nguồn lửa/nhiệt", "description": "Dấu hiệu nguy cơ cháy từ việc sử dụng lửa, gas, nhiệt"},
    {"name": "Lối thoát nạn và trang bị PCCC", "description": "Dấu hiệu bất thường liên quan đến lối thoát và phương tiện PCCC"},
    {"name": "Dấu hiệu bất thường từ máy móc", "description": "Dấu hiệu cảnh báo sớm từ thiết bị, máy móc công nghiệp"},
    {"name": "Tác động từ thiên nhiên", "description": "Dấu hiệu nguy cơ cháy do tác động thời tiết, môi trường"},
    {"name": "Nguy cơ tự cháy", "description": "Dấu hiệu nguy cơ tự phát cháy từ vật liệu, hóa chất, pin"},
    {"name": "Phương tiện giao thông", "description": "Dấu hiệu nguy cơ cháy nổ liên quan đến phương tiện đỗ trong nhà"},
    {"name": "Nguy cơ bổ sung", "description": "Các dấu hiệu nguy cơ khác cần lưu ý"},
]

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

ALL_COMMON_QUESTIONS = [
    (0, GROUP1), (1, GROUP2), (2, GROUP3), (3, GROUP4),
    (4, GROUP5), (5, GROUP6), (6, GROUP7), (7, GROUP8),
]

# ===== Write seed_data.py =====
import pprint
with open("backend/seed_data.py", "w", encoding="utf-8") as f:
    for vn, vv in [("FACILITY_TYPES", FACILITY_TYPES), ("COMMON_CATEGORIES", COMMON_CATEGORIES),
                    ("GROUP1_QUESTIONS", GROUP1), ("GROUP2_QUESTIONS", GROUP2), ("GROUP3_QUESTIONS", GROUP3),
                    ("GROUP4_QUESTIONS", GROUP4), ("GROUP5_QUESTIONS", GROUP5), ("GROUP6_QUESTIONS", GROUP6),
                    ("GROUP7_QUESTIONS", GROUP7), ("GROUP8_QUESTIONS", GROUP8), ("ALL_COMMON_QUESTIONS", ALL_COMMON_QUESTIONS)]:
        f.write(f"\n{vn} = {pprint.pformat(vv, indent=4, width=500, sort_dicts=False)}\n")

# ===== Write seed_data_specific.py =====
spec_map = [("SPECIFIC_CATEGORY_A", SPEC_A), ("SPECIFIC_CATEGORY_B", SPEC_B), ("SPECIFIC_CATEGORY_C", SPEC_C),
            ("SPECIFIC_CATEGORY_D", SPEC_D), ("SPECIFIC_CATEGORY_E", SPEC_E), ("SPECIFIC_CATEGORY_F", SPEC_F),
            ("SPECIFIC_CATEGORY_G", SPEC_G), ("SPECIFIC_CATEGORY_H", SPEC_H), ("SPECIFIC_CATEGORY_I", SPEC_I),
            ("SPECIFIC_CATEGORY_J", SPEC_J), ("SPECIFIC_CATEGORY_K", SPEC_K), ("SPECIFIC_CATEGORY_L", SPEC_L)]
with open("backend/seed_data_specific.py", "w", encoding="utf-8") as f:
    for vn, vv in spec_map:
        f.write(f"\n{vn} = {pprint.pformat(vv, indent=4, width=500, sort_dicts=False)}\n")

print("✅ Đã ghi seed_data.py và seed_data_specific.py")

# ===== Export txt =====
all_specs = [SPEC_A, SPEC_B, SPEC_C, SPEC_D, SPEC_E, SPEC_F, SPEC_G, SPEC_H, SPEC_I, SPEC_J, SPEC_K, SPEC_L]
with open("danh_sach_cau_hoi_duyet.txt", "w", encoding="utf-8") as f:
    gid = 1
    total_common = 0
    f.write("=" * 60 + "\n")
    f.write("PHẦN 1: CÂU HỎI CHUNG (áp dụng cho mọi loại cơ sở)\n")
    f.write("=" * 60 + "\n\n")
    for ci, qs in ALL_COMMON_QUESTIONS:
        cn = COMMON_CATEGORIES[ci]["name"]
        f.write(f"--- NHÓM: {cn.upper()} ---\n\n")
        for q in qs:
            f.write(f"ID{gid}. {q['text']}\n")
            for o in q['options']:
                f.write(f"{o['key']}. {o['text']}\n")
            f.write("\n")
            gid += 1
            total_common += 1
    
    total_spec = 0
    f.write("=" * 60 + "\n")
    f.write("PHẦN 2: CÂU HỎI ĐẶC THÙ NGÀNH\n")
    f.write("=" * 60 + "\n\n")
    for sp in all_specs:
        f.write(f"--- NHÓM: {sp['name'].upper()} ---\n\n")
        for q in sp['questions']:
            f.write(f"ID{gid}. {q['text']}\n")
            for o in q['options']:
                f.write(f"{o['key']}. {o['text']}\n")
            f.write("\n")
            gid += 1
            total_spec += 1

print(f"✅ Tổng: {total_common} câu chung + {total_spec} câu đặc thù = {total_common + total_spec} câu")
print(f"   (Giảm từ 210 → {total_common + total_spec} câu)")

# Copy to artifacts
import shutil
shutil.copy2("danh_sach_cau_hoi_duyet.txt", r"C:\Users\Hasky\.gemini\antigravity\brain\306eaf9d-d505-4ac6-a19f-731608d9ef25\danh_sach_cau_hoi_duyet.txt")
print("✅ Đã copy vào artifacts")
