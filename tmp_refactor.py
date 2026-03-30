import json
import re

def soften_text(text):
    if not isinstance(text, str):
        return text
        
    replacements = {
        "vi phạm quy định PCCC": "chưa đáp ứng tiêu chuẩn an toàn",
        "Vi phạm quy định PCCC": "Tình trạng hạ tầng an toàn",
        "tuân thủ quy định về an toàn PCCC": "đáp ứng tiêu chuẩn an toàn hiện hành",
        "tuân thủ quy định phòng cháy": "đáp ứng tiêu chuẩn an toàn",
        "tuân thủ quy định": "đáp ứng tiêu chuẩn an toàn",
        "hoạt động không phép về PCCC": "chưa hoàn thiện hệ thống PCCC theo hồ sơ thiết kế",
        "không phép": "chưa có hồ sơ kỹ thuật đồng bộ",
        "trái phép": "chưa qua đánh giá rủi ro an toàn",
        "có giấy phép hàn cắt": "có quy trình kiểm soát an toàn nghiêm ngặt",
        "chưa có giấy phép chính thức": "chưa ban hành quy trình bằng văn bản",
        "Cảnh sát PCCC": "đơn vị tư vấn chuyên môn",
        "quá hạn kiểm định": "lâu ngày chưa được kiểm tra kỹ thuật lại",
        "không kiểm định": "chưa được kiểm tra kỹ thuật bảo đảm",
        "đăng ký kiểm định": "thực hiện kiểm tra kỹ thuật",
        "bắt buộc": "cơ bản",
        "cảnh báo sớm nguy cơ cháy nổ": "cảnh báo sớm sự cố",
        "điện lắp đặt tự phát": "hệ thống điện đấu nối theo nhu cầu phát sinh, thiếu thiết kế tổng thể",
        "hồ sơ pháp lý PCCC": "hồ sơ thiết kế và nghiệm thu kỹ thuật PCCC",
        "hồ sơ pháp lý về an toàn điện": "hồ sơ kỹ thuật và đo lường điện",
        "Không có bất kỳ hồ sơ pháp lý nào": "Chưa kiện toàn các hồ sơ kỹ thuật chuyên sâu",
        "xử lý đúng quy định": "xử lý an toàn, phân loại rõ ràng",
        "pháp lý": "kỹ thuật chuyên sâu",
    }
    
    for old, new in replacements.items():
        # Case insensitive replacement for some
        text = text.replace(old, new)
        
    return text

def process_questions(groups):
    for group_id, questions in groups:
        for q in questions:
            q["text"] = soften_text(q["text"])
            for opt in q["options"]:
                opt["text"] = soften_text(opt["text"])

import sys
sys.path.append('.')
import backend.seed_data as sd
import backend.seed_data_specific as sds

# Apply text softening
process_questions(sd.ALL_COMMON_QUESTIONS)

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

sd.COMMON_CATEGORIES[2]["name"] = "Tình trạng hạ tầng và lối thoát nạn"

# Specific ID reductions (IDs: 19, 31, 36, 90)
# ID 19 -> sd.GROUP1_QUESTIONS[18]
# ID 31 -> sd.GROUP3_QUESTIONS[0]
# ID 36 -> sd.GROUP3_QUESTIONS[5]
# ID 90 -> sd.GROUP8_QUESTIONS[9]

target_qs = [
    sd.GROUP1_QUESTIONS[18],
    sd.GROUP3_QUESTIONS[0],
    sd.GROUP3_QUESTIONS[5],
    sd.GROUP8_QUESTIONS[9]
]

for q in target_qs:
    # Set scores to 0, 0, 1, 1 to reduce weight
    q["options"][0]["score"] = 0
    q["options"][1]["score"] = 0
    q["options"][2]["score"] = 1
    q["options"][3]["score"] = 1

# Generate the MD file
with open("c:/Users/Hasky/.gemini/antigravity/scratch/fras/danh_sach_tat_ca_cau_hoi_da_sua.md", "w", encoding="utf-8") as f:
    f.write("# Toàn Bộ 210 Câu Hỏi Đã Được Làm Mềm (Level 3)\n\n")
    f.write("> **Các câu hỏi nhạy cảm và toàn bộ tùy chọn đã được thay thế để tập trung 100% vào Tình trạng rủi ro vật lý thay vì pháp lý.**\n")
    f.write("> **Các câu (ID 19, 31, 36, 90) đã được giảm điểm số (0, 0, 1, 1).**\n\n")
    
    global_id = 1
    
    f.write("## PHẦN 1: CÁC CÂU HỎI CHUNG\n\n")
    for group_idx, questions in sd.ALL_COMMON_QUESTIONS:
        cat_name = sd.COMMON_CATEGORIES[group_idx]["name"]
        f.write(f"### Dành mục: {cat_name}\n\n")
        for q in questions:
            f.write(f"**ID {global_id}: {q['text']}**\n")
            f.write(f"*(Các câu hỏi giảm tỷ trọng)*\n" if global_id in [19, 31, 36, 90] else "")
            for opt in q["options"]:
                f.write(f"- {opt['key']} (Điểm: {opt['score']}): {opt['text']}\n")
            f.write("\n")
            global_id += 1

    f.write("## PHẦN 2: CÁC CÂU HỎI ĐẶC THÙ NGÀNH\n\n")
    for group_idx, questions in spec_groups:
        # get name from category
        cats = [sds.SPECIFIC_CATEGORY_A, sds.SPECIFIC_CATEGORY_B, sds.SPECIFIC_CATEGORY_C,
                sds.SPECIFIC_CATEGORY_D, sds.SPECIFIC_CATEGORY_E, sds.SPECIFIC_CATEGORY_F,
                sds.SPECIFIC_CATEGORY_G, sds.SPECIFIC_CATEGORY_H, sds.SPECIFIC_CATEGORY_I,
                sds.SPECIFIC_CATEGORY_J, sds.SPECIFIC_CATEGORY_K, sds.SPECIFIC_CATEGORY_L]
        cat_name = cats[group_idx]["name"]
        f.write(f"### Dành mục: {cat_name}\n\n")
        for q in questions:
            f.write(f"**ID {global_id}: {q['text']}**\n")
            for opt in q["options"]:
                f.write(f"- {opt['key']} (Điểm: {opt['score']}): {opt['text']}\n")
            f.write("\n")
            global_id += 1

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

write_python_file("c:/Users/Hasky/.gemini/antigravity/scratch/fras/backend/seed_data_new.py", [
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

write_python_file("c:/Users/Hasky/.gemini/antigravity/scratch/fras/backend/seed_data_specific_new.py", [
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
