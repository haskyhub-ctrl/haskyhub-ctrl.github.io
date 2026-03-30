import json

keywords = ["vi phạm", "trái phép", "không phép", "pháp lý", "bắt buộc", "thẩm duyệt", "nghiệm thu", "giấy phép", "quy định", "bị phạt", "cảnh sát pccc"]

with open("c:/Users/Hasky/.gemini/antigravity/scratch/fras/cau_hoi_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("c:/Users/Hasky/.gemini/antigravity/scratch/fras/tmp_violations.md", "w", encoding="utf-8") as f:
    f.write("# Các Câu Hỏi Có Tính Chất 'Điều Tra Vi Phạm' Cần Xem Xét\n\n")
    for q in data:
        text_to_check = q.get("text", "").lower()
        options = q.get("options", [])
        opts_text = " ".join([opt.get("text", "").lower() for opt in options])
        
        found_keywords = [kw for kw in keywords if kw in text_to_check or kw in opts_text]
        
        if found_keywords:
            f.write(f"### ID: {q.get('id')}\n")
            f.write(f"**Câu hỏi:** {q.get('text')}\n")
            f.write(f"**Từ khóa phát hiện:** {', '.join(found_keywords)}\n")
            f.write("**Các lựa chọn (options):**\n")
            for opt in options:
                f.write(f"- {opt.get('key')}: {opt.get('text')}\n")
            f.write("\n---\n\n")
