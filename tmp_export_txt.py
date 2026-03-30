import sys
sys.path.append('backend')
from seed_data import ALL_COMMON_QUESTIONS, COMMON_CATEGORIES
from seed_data_specific import (
    SPECIFIC_CATEGORY_A, SPECIFIC_CATEGORY_B, SPECIFIC_CATEGORY_C,
    SPECIFIC_CATEGORY_D, SPECIFIC_CATEGORY_E, SPECIFIC_CATEGORY_F,
    SPECIFIC_CATEGORY_G, SPECIFIC_CATEGORY_H, SPECIFIC_CATEGORY_I,
    SPECIFIC_CATEGORY_J, SPECIFIC_CATEGORY_K, SPECIFIC_CATEGORY_L
)

specific_categories = [
    SPECIFIC_CATEGORY_A, SPECIFIC_CATEGORY_B, SPECIFIC_CATEGORY_C,
    SPECIFIC_CATEGORY_D, SPECIFIC_CATEGORY_E, SPECIFIC_CATEGORY_F,
    SPECIFIC_CATEGORY_G, SPECIFIC_CATEGORY_H, SPECIFIC_CATEGORY_I,
    SPECIFIC_CATEGORY_J, SPECIFIC_CATEGORY_K, SPECIFIC_CATEGORY_L
]

with open("danh_sach_cau_hoi_duyet.txt", "w", encoding="utf-8") as f:
    global_id = 1
    
    f.write("========== PHẦN 1: CÁC NHÓM NGUYÊN NHÂN CHUNG ==========\n\n")
    # Common questions
    for cat_idx, questions in ALL_COMMON_QUESTIONS:
        cat_name = COMMON_CATEGORIES[cat_idx]["name"]
        f.write(f"--- NHÓM: {cat_name.upper()} ---\n\n")
        
        for q in questions:
            f.write(f"ID{global_id}. {q['text']}\n")
            for opt in q["options"]:
                f.write(f"{opt['key']}. {opt['text']}\n")
            f.write("\n")
            global_id += 1
            
    f.write("========== PHẦN 2: CÁC NHÓM NGUYÊN NHÂN ĐẶC THÙ NGÀNH ==========\n\n")
    # Specific questions
    for cat in specific_categories:
        cat_name = cat["name"]
        f.write(f"--- NHÓM: {cat_name.upper()} ---\n\n")
        
        for q in cat["questions"]:
            f.write(f"ID{global_id}. {q['text']}\n")
            for opt in q["options"]:
                f.write(f"{opt['key']}. {opt['text']}\n")
            f.write("\n")
            global_id += 1

print("Done exporting to danh_sach_cau_hoi_duyet.txt (grouped by category)")
