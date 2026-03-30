import sys
import re

sys.path.append('backend')
import seed_data as sd
import seed_data_specific as sds

def aggressive_soften(text):
    if not isinstance(text, str):
        return text

    # Khắc phục từ ngữ quá dài
    replacements = {
        "Tự chế hoặc tích trữ pháo nổ chưa qua đánh giá rủi ro an toàn trong nhà, bảo quản không đúng quy định": "Tự làm hoặc tàng trữ pháo nổ",
        "Tự chế hoặc tích trữ pháo nổ chưa qua đánh giá rủi ro an toàn trong nhà": "Tự làm hoặc tàng trữ pháo nổ",
        "Tự chế hoặc tích trữ pháo nổ trong nhà": "Tự làm hoặc tàng trữ pháo nổ",
        "chưa hoàn thiện hệ thống PCCC theo hồ sơ thiết kế": "Hệ thống tự lắp ráp",
        "hồ sơ thiết kế và nghiệm thu kỹ thuật PCCC": "thiết kế PCCC",
        "hồ sơ kỹ thuật và đo lường điện": "hồ sơ điện",
        "Chưa kiện toàn các hồ sơ kỹ thuật chuyên sâu": "Tự lắp đặt theo nhu cầu cơ bản",
        "Chưa kiện toàn hệ thống pháp lý": "Tự lắp đặt",
        "Tự làm pháo": "Tự làm pháo" # just an exact match
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove strict regex patterns containing 'quy định', 'quy chuẩn'
    patterns = [
        r'\,?\s*không đúng quy định\b',
        r'\,?\s*đúng quy định\b',
        r'\s*theo đúng quy định\b',
        r'\s*theo quy định\b',
        r'\s*theo đúng quy chuẩn\b',
        r'\s*theo quy chuẩn\b',
        r'\s*theo quy chuẩn hiện hành\b',
        r'\s*quy định hiện hành\b',
        r'\,?\s*chưa qua đánh giá rủi ro an toàn\b',
        r'\,?\s*bảo quản không đúng quy định\b',
        r'\,?\s*không đúng quy cách\b',
        r'\,?\s*đúng quy cách\b',
        r'\,?\s*đúng kỹ thuật\b',
        r'\,?\s*không đúng kỹ thuật\b',
        r'\s*chưa có hồ sơ kỹ thuật đồng bộ\b',
        r'\s*chưa đạt điều kiện an toàn tối ưu\b',
        r'\,?\s*được triển khai đồng bộ, an toàn\b',
        r'\,?\s*hoạt động an toàn, ổn định\b',
    ]
    for p in patterns:
        text = re.sub(p, '', text, flags=re.IGNORECASE)

    # Clean up double punctuation & spaces
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s,', ',', text)
    text = re.sub(r',\s*$', '', text)
    text = re.sub(r'^\s*,\s*', '', text)
    text = text.strip()
    
    if len(text) > 0 and text[0].islower():
        text = text[0].upper() + text[1:]
        
    return text

def process_questions(groups):
    for group_id, questions in groups:
        for q in questions:
            q["text"] = aggressive_soften(q["text"])
            for opt in q["options"]:
                opt["text"] = aggressive_soften(opt["text"])

def process_categories(categories):
    for cat in categories:
        cat["name"] = aggressive_soften(cat["name"])
        cat["description"] = aggressive_soften(cat["description"])

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

def write_python_file(filename, vars_to_write, imports=[]):
    with open(filename, "w", encoding="utf-8") as f:
        for imp in imports:
            f.write(f"{imp}\n")
        f.write("\n")
        for var_name, var_value in vars_to_write:
            import pprint
            formatted = pprint.pformat(var_value, indent=4, width=500, sort_dicts=False)
            f.write(f"{var_name} = {formatted}\n\n")

write_python_file("backend/seed_data_new_2.py", [
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

write_python_file("backend/seed_data_specific_new_2.py", [
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

print("Finished rewriting files with Level 5 softening!")
