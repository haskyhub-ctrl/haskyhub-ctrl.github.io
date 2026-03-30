import sys
import re

sys.path.append('backend')
import seed_data as sd
import seed_data_specific as sds

def soften_text(text):
    if not isinstance(text, str):
        return text
        
    replacements = {
        # 1. Bỏ "tại cơ sở", "của cơ sở"
        "tại cơ sở": "",
        "Tại cơ sở": "",
        "của cơ sở": "",
        
        # 2. Xóa/thay thế "đáp ứng tiêu chuẩn"
        "chưa đáp ứng tiêu chuẩn an toàn": "chưa đạt điều kiện an toàn tối ưu",
        "đáp ứng tiêu chuẩn an toàn hiện hành": "được triển khai đồng bộ, an toàn",
        "đáp ứng tiêu chuẩn an toàn": "hoạt động an toàn, ổn định",
        "chưa đáp ứng tiêu chuẩn PCCC": "chưa hoàn thiện đồng bộ",
        "đáp ứng tiêu chuẩn PCCC": "hoạt động an toàn",
        "tiêu chuẩn an toàn chuyên sâu": "các giải pháp kỹ thuật tối ưu",
        "tiêu chuẩn an toàn": "yêu cầu vận hành an toàn",
        "đúng tiêu chuẩn với": "đồng bộ cùng",
        "chưa có hệ thống an toàn đạt chuẩn": "hệ thống được thiết lập theo nhu cầu cơ bản",
        "chưa có hệ thống an toàn chuyên sâu": "chưa có hệ thống đồng bộ",
        
        # Sửa cấu trúc dư thừa sau khi xóa "tại cơ sở"
        " ? ": " ",
        ", ,": ",",
        "  ": " ",
        "( ": "(",
        " )": ")",
    }
    
    for old, new in replacements.items():
        # simple text replace
        text = text.replace(old, new)
        
    # fix capitalization and spaces
    text = text.strip()
    if text.startswith("có ") or text.startswith("Có "):
        pass
        
    # Fix trailing spaces before question marks
    text = text.replace(" ?", "?")
    
    # Optional: If the sentence starts with lowercase because "Tại cơ sở" was removed
    if len(text) > 0 and text[0].islower():
        text = text[0].upper() + text[1:]
        
    return text

def process_questions(groups):
    for group_id, questions in groups:
        for q in questions:
            q["text"] = soften_text(q["text"])
            for opt in q["options"]:
                opt["text"] = soften_text(opt["text"])

def process_categories(categories):
    for cat in categories:
        cat["name"] = soften_text(cat["name"])
        cat["description"] = soften_text(cat["description"])

# Apply text softening
process_questions(sd.ALL_COMMON_QUESTIONS)
process_categories(sd.COMMON_CATEGORIES)

spec_groups = [
    (0, sds.SPECIFIC_CATEGORY_A["questions"]),
    (1, sds.SPECIFIC_CATEGORY_B["questions"]),
    (2, sds.SPECIFIC_CATEGORY_C["questions"]),
    (3, sds.SPECIFIC_CATEGORY_D["questions"]),
    (4, sds.SPECIFIC_CATEGORY_E["questions"]),
    (5, sds.SPECIFIC_CATEGORY_F["questions"]),
    (6, sds.SPECIFIC_CATEGORY_G["questions"]),
    (7, sds.SPECIFIC_CATEGORY_H["questions"]),
    (8, sds.SPECIFIC_CATEGORY_I["questions"]),
    (9, sds.SPECIFIC_CATEGORY_J["questions"]),
    (10, sds.SPECIFIC_CATEGORY_K["questions"]),
    (11, sds.SPECIFIC_CATEGORY_L["questions"]),
]
process_questions(spec_groups)

# Generate the python files directly using pprint
def write_python_file(filename, vars_to_write, imports=[]):
    with open(filename, "w", encoding="utf-8") as f:
        for imp in imports:
            f.write(f"{imp}\n")
        f.write("\n")
        for var_name, var_value in vars_to_write:
            import pprint
            formatted = pprint.pformat(var_value, indent=4, width=500, sort_dicts=False)
            f.write(f"{var_name} = {formatted}\n\n")

write_python_file("backend/seed_data_new.py", [
    ("FACILITY_TYPES", sd.FACILITY_TYPES),
    ("COMMON_CATEGORIES", sd.COMMON_CATEGORIES),
    ("GROUP1_QUESTIONS", sd.GROUP1_QUESTIONS),
    ("GROUP2_QUESTIONS", sd.GROUP2_QUESTIONS),
    ("GROUP3_QUESTIONS", sd.GROUP3_QUESTIONS),
    ("GROUP4_QUESTIONS", sd.GROUP4_QUESTIONS),
    ("GROUP5_QUESTIONS", sd.GROUP5_QUESTIONS),
    ("GROUP6_QUESTIONS", sd.GROUP6_QUESTIONS),
    ("GROUP7_QUESTIONS", sd.GROUP7_QUESTIONS),
    ("GROUP8_QUESTIONS", sd.GROUP8_QUESTIONS),
    ("ALL_COMMON_QUESTIONS", sd.ALL_COMMON_QUESTIONS)
])

write_python_file("backend/seed_data_specific_new.py", [
    ("SPECIFIC_CATEGORY_A", sds.SPECIFIC_CATEGORY_A),
    ("SPECIFIC_CATEGORY_B", sds.SPECIFIC_CATEGORY_B),
    ("SPECIFIC_CATEGORY_C", sds.SPECIFIC_CATEGORY_C),
    ("SPECIFIC_CATEGORY_D", sds.SPECIFIC_CATEGORY_D),
    ("SPECIFIC_CATEGORY_E", sds.SPECIFIC_CATEGORY_E),
    ("SPECIFIC_CATEGORY_F", sds.SPECIFIC_CATEGORY_F),
    ("SPECIFIC_CATEGORY_G", sds.SPECIFIC_CATEGORY_G),
    ("SPECIFIC_CATEGORY_H", sds.SPECIFIC_CATEGORY_H),
    ("SPECIFIC_CATEGORY_I", sds.SPECIFIC_CATEGORY_I),
    ("SPECIFIC_CATEGORY_J", sds.SPECIFIC_CATEGORY_J),
    ("SPECIFIC_CATEGORY_K", sds.SPECIFIC_CATEGORY_K),
    ("SPECIFIC_CATEGORY_L", sds.SPECIFIC_CATEGORY_L),
])

print("Finished rewriting files!")
