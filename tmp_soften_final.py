import sys
import re

sys.path.append('backend')
import seed_data as sd
import seed_data_specific as sds

# ===== EXACT REPLACEMENTS: từng cụm từ cụ thể cần loại bỏ =====
EXACT_REPLACEMENTS = {
    # --- Loại bỏ "quy định", "tiêu chuẩn", "quy chuẩn" ---
    "đúng chiều rộng quy định": "đủ rộng",
    "theo quy định": "",
    "đúng quy định": "",
    "không đúng quy định": "",
    "bảo quản không đúng quy định": "",
    "tuân thủ quy định phòng cháy": "đảm bảo an toàn cháy nổ",
    "tuân thủ quy định": "",
    "quy định hiện hành": "",
    "theo đúng quy chuẩn": "",
    "theo quy chuẩn": "",
    "đạt tiêu chuẩn": "đạt yêu cầu",
    "tiêu chuẩn PCCC": "yêu cầu an toàn",
    "đúng tiêu chuẩn": "phù hợp",
    "đạt chuẩn": "phù hợp",
    "chưa đạt chuẩn": "chưa đạt",
    "tiêu chuẩn khoảng cách an toàn": "khoảng cách an toàn",
    "đúng chuẩn": "phù hợp",
    "theo TCVN/IEC": "",
    "có đạt không": "",
    "không rõ có đạt chuẩn không": "chưa kiểm tra lại",

    # --- Loại bỏ "giấy phép", "kiểm định", "thẩm duyệt", "nghiệm thu" ---
    "có giấy phép": "có chuyên môn",
    "giấy phép còn hiệu lực": "hồ sơ kỹ thuật đầy đủ",
    "giấy phép sắp hết hạn đang gia hạn": "đang cập nhật hồ sơ",
    "giấy phép đã hết hạn": "hồ sơ chưa cập nhật",
    "giấy phép vận chuyển": "hồ sơ vận chuyển",
    "giấy phép kinh doanh, chưa hoàn thành thủ tục thẩm duyệt và nghiệm thu PCCC": "giấy tờ kinh doanh cơ bản, chưa có hồ sơ thiết kế PCCC",
    "giấy phép": "hồ sơ kỹ thuật",
    "đã thực hiện kiểm tra kỹ thuật đúng hạn": "được kiểm tra kỹ thuật định kỳ",
    "kiểm định đúng hạn": "kiểm tra định kỳ",
    "kiểm định còn hạn": "kiểm tra gần đây",
    "lâu ngày chưa được kiểm tra kỹ thuật lại nhưng vẫn đang sử dụng, chưa gia hạn": "lâu ngày chưa kiểm tra, vẫn đang sử dụng",
    "lâu ngày chưa được kiểm tra kỹ thuật lại nhưng vẫn hoạt động": "lâu ngày chưa kiểm tra, vẫn đang hoạt động",
    "chưa từng kiểm định": "chưa từng kiểm tra kỹ thuật",
    "chưa được kiểm tra kỹ thuật bảo đảm": "chưa được kiểm tra",
    "có biên bản kiểm định": "có biên bản kiểm tra",
    "thẩm duyệt thiết kế PCCC, nghiệm thu PCCC, giấy chứng nhận PCCC": "hồ sơ thiết kế và lắp đặt PCCC",
    "thẩm duyệt thiết kế, biên bản nghiệm thu, giấy chứng nhận PCCC còn hiệu lực": "hồ sơ thiết kế, lắp đặt và vận hành PCCC đầy đủ",
    "thẩm duyệt và nghiệm thu": "thiết kế và lắp đặt",
    "thẩm duyệt thiết kế PCCC": "thiết kế PCCC",
    "thẩm duyệt": "thiết kế",
    "nghiệm thu PCCC": "lắp đặt PCCC",
    "nghiệm thu điện": "lắp đặt điện",
    "biên bản nghiệm thu": "hồ sơ lắp đặt",
    "giấy chứng nhận PCCC": "hồ sơ PCCC",
    "được thẩm duyệt": "có thiết kế bài bản",

    # --- Loại bỏ "vi phạm", "xử phạt", "chế tài" ---
    "chế tài xử lý vi phạm": "nhắc nhở",
    "xử phạt vi phạm": "nhắc nhở",
    "vi phạm nhỏ": "lỗi nhỏ",
    "bỏ qua vi phạm": "bỏ qua",
    "vi phạm": "lỗi",

    # --- Loại bỏ "cơ quan chức năng", "Cảnh sát PCCC" ---
    "cơ quan chức năng yêu cầu": "có yêu cầu",
    "khi cơ quan chức năng yêu cầu": "khi được yêu cầu",
    "Cảnh sát PCCC": "lực lượng PCCC",
    "C.sát PCCC": "lực lượng PCCC",
    "Cảnh sát": "lực lượng chức năng",
    "liên lạc lực lượng C.sát PCCC": "liên lạc lực lượng PCCC địa phương",

    # --- Loại bỏ "Hệ thống tự lắp ráp" (lỗi cũ) ---
    "cơ sở Hệ thống tự lắp ráp": "hệ thống PCCC tự lắp đặt theo nhu cầu",
    "Hệ thống tự lắp ráp": "Hệ thống tự lắp đặt",

    # --- Loại bỏ thêm các cụm sót ---
    "Có quy định cấm nhưng kiểm tra không thường xuyên": "Có quy tắc nội bộ nhưng kiểm tra không thường xuyên",
    "Cấm tuyệt đối bếp lửa/gas tại gian hàng, kiểm tra hàng ngày, xử phạt vi phạm": "Cấm tuyệt đối bếp lửa/gas tại gian hàng, kiểm tra hàng ngày, nhắc nhở nghiêm",
    "có biển cấm và chế tài": "có biển cấm và nhắc nhở",
    "có biển cấm, có chế tài": "có biển cấm, nhắc nhở nghiêm",
    "Đo kiểm điện trở nối đất hàng năm, đạt tiêu chuẩn ≤ 10Ω, có biên bản kiểm định": "Đo kiểm điện trở nối đất hàng năm, đạt ≤ 10Ω, có biên bản kiểm tra",    
    "chưa phân vùng chính thức": "chưa phân vùng rõ ràng",
    "Phân vùng theo TCVN/IEC": "Phân vùng nguy hiểm rõ ràng",
    "Hệ thống nối đất chống tĩnh điện cho bồn chứa xăng dầu và vòi bơm có được đo kiểm định kỳ không": "Hệ thống nối đất chống tĩnh điện cho bồn chứa xăng dầu và vòi bơm có được đo kiểm tra định kỳ không",
    "nhân viên không nhắc khách về quy định": "nhân viên không nhắc khách",
    "tình trạng kiểm định và vận hành": "tình trạng kiểm tra và vận hành",
    "gần rơm hơn quy định": "gần rơm",
    "Có quy định cơ bản rút phích cắm": "Có nhắc nhở rút phích cắm",

    # --- Loại bỏ "đối phó kiểm tra" ---
    "để đối phó kiểm tra": "",
    "khi có đoàn thanh tra": "khi được nhắc nhở",

    # --- Rút gọn câu ID30 ---
    "Tự chế hoặc tích trữ pháo nổ chưa qua đánh giá rủi ro an toàn trong nhà, bảo quản không đúng quy định": "Tự làm pháo hoặc tàng trữ pháo nổ trong nhà",
    "Tự chế hoặc tích trữ pháo nổ chưa qua đánh giá rủi ro an toàn trong nhà": "Tự làm pháo hoặc tàng trữ pháo nổ trong nhà",
    "Tự làm hoặc tàng trữ pháo nổ": "Tự làm pháo hoặc tàng trữ pháo nổ trong nhà",

    # --- clean up ---
    "hồ sơ kỹ thuật chuyên sâu về an toàn điện (thiết kế điện có thiết kế bài bản, lắp đặt điện, biên bản kiểm tra định kỳ)": "hồ sơ kỹ thuật về hệ thống điện (bản vẽ thiết kế, biên bản kiểm tra định kỳ)",
    "Tự lắp đặt theo nhu cầu cơ bản về hệ thống điện, hệ thống điện đấu nối theo nhu cầu phát sinh, thiếu thiết kế tổng thể": "Hệ thống điện tự đấu nối theo nhu cầu phát sinh, thiếu thiết kế tổng thể",
    "đơn vị có giấy phép": "đơn vị chuyên môn",
    "có đầy đủ thiết kế PCCC cơ bản (thiết kế PCCC, lắp đặt PCCC, hồ sơ PCCC)": "có hồ sơ thiết kế và lắp đặt hệ thống PCCC",
}

def apply_replacements(text):
    if not isinstance(text, str):
        return text
    for old, new in EXACT_REPLACEMENTS.items():
        text = text.replace(old, new)
    
    # Cleanup double spaces, trailing commas, leading commas
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s,', ',', text)
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r',\s*$', '', text)
    text = re.sub(r'^\s*,\s*', '', text)
    text = re.sub(r'\s+\?', '?', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = text.strip()
    
    if len(text) > 0 and text[0].islower():
        text = text[0].upper() + text[1:]
    
    return text

def process_questions(groups):
    for group_id, questions in groups:
        for q in questions:
            q["text"] = apply_replacements(q["text"])
            for opt in q["options"]:
                opt["text"] = apply_replacements(opt["text"])

def process_categories(categories):
    for cat in categories:
        cat["name"] = apply_replacements(cat["name"])
        cat["description"] = apply_replacements(cat["description"])

# Apply text softening to common
process_questions(sd.ALL_COMMON_QUESTIONS)
process_categories(sd.COMMON_CATEGORIES)

# Apply to specific
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

# Also clean category names/descriptions for specifics
for cat_obj in [sds.SPECIFIC_CATEGORY_A, sds.SPECIFIC_CATEGORY_B, sds.SPECIFIC_CATEGORY_C,
                sds.SPECIFIC_CATEGORY_D, sds.SPECIFIC_CATEGORY_E, sds.SPECIFIC_CATEGORY_F,
                sds.SPECIFIC_CATEGORY_G, sds.SPECIFIC_CATEGORY_H, sds.SPECIFIC_CATEGORY_I,
                sds.SPECIFIC_CATEGORY_J, sds.SPECIFIC_CATEGORY_K, sds.SPECIFIC_CATEGORY_L]:
    cat_obj["name"] = apply_replacements(cat_obj["name"])
    cat_obj["description"] = apply_replacements(cat_obj["description"])

# ===== Write new seed files =====
def write_python_file(filename, vars_to_write):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n")
        for var_name, var_value in vars_to_write:
            import pprint
            formatted = pprint.pformat(var_value, indent=4, width=500, sort_dicts=False)
            f.write(f"{var_name} = {formatted}\n\n")

write_python_file("backend/seed_data.py", [
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

write_python_file("backend/seed_data_specific.py", [
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

print("✅ Đã ghi đè seed_data.py và seed_data_specific.py")

# ===== Xuất file txt để duyệt =====
specific_categories = [
    sds.SPECIFIC_CATEGORY_A, sds.SPECIFIC_CATEGORY_B, sds.SPECIFIC_CATEGORY_C,
    sds.SPECIFIC_CATEGORY_D, sds.SPECIFIC_CATEGORY_E, sds.SPECIFIC_CATEGORY_F,
    sds.SPECIFIC_CATEGORY_G, sds.SPECIFIC_CATEGORY_H, sds.SPECIFIC_CATEGORY_I,
    sds.SPECIFIC_CATEGORY_J, sds.SPECIFIC_CATEGORY_K, sds.SPECIFIC_CATEGORY_L
]

with open("danh_sach_cau_hoi_duyet.txt", "w", encoding="utf-8") as f:
    global_id = 1
    
    f.write("========== PHẦN 1: CÁC NHÓM NGUYÊN NHÂN CHUNG ==========\n\n")
    for cat_idx, questions in sd.ALL_COMMON_QUESTIONS:
        cat_name = sd.COMMON_CATEGORIES[cat_idx]["name"]
        f.write(f"--- NHÓM: {cat_name.upper()} ---\n\n")
        for q in questions:
            f.write(f"ID{global_id}. {q['text']}\n")
            for opt in q["options"]:
                f.write(f"{opt['key']}. {opt['text']}\n")
            f.write("\n")
            global_id += 1
            
    f.write("========== PHẦN 2: CÁC NHÓM NGUYÊN NHÂN ĐẶC THÙ NGÀNH ==========\n\n")
    for cat in specific_categories:
        cat_name = cat["name"]
        f.write(f"--- NHÓM: {cat_name.upper()} ---\n\n")
        for q in cat["questions"]:
            f.write(f"ID{global_id}. {q['text']}\n")
            for opt in q["options"]:
                f.write(f"{opt['key']}. {opt['text']}\n")
            f.write("\n")
            global_id += 1

print(f"✅ Đã xuất {global_id - 1} câu hỏi vào danh_sach_cau_hoi_duyet.txt")

# ===== Kiểm tra xem còn sót từ nhạy cảm nào không =====
sensitive_words = ["quy định", "quy chuẩn", "tiêu chuẩn", "vi phạm", "giấy phép", "kiểm định", 
                   "thẩm duyệt", "nghiệm thu", "xử phạt", "chế tài", "đối phó"]
with open("danh_sach_cau_hoi_duyet.txt", "r", encoding="utf-8") as f:
    content = f.read()
    found_any = False
    for word in sensitive_words:
        lines_found = [line.strip() for line in content.split('\n') if word in line.lower()]
        if lines_found:
            found_any = True
            print(f"\n⚠️ Vẫn còn từ '{word}' trong {len(lines_found)} dòng:")
            for line in lines_found[:5]:
                print(f"   → {line[:120]}")
    if not found_any:
        print("\n🎉 Sạch hoàn toàn! Không còn từ nhạy cảm nào.")
