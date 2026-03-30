import json

keywords = ["hoạt động chui", "hoạt động không phép", "trái phép", "vi phạm", "xử phạt", "đình chỉ", "không phép", "tự chế"]

with open("c:/Users/Hasky/.gemini/antigravity/scratch/fras/cau_hoi_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for q in data:
    text_to_check = q.get("text", "").lower()
    options = q.get("options", [])
    opts_text = " ".join([opt.get("text", "").lower() for opt in options])
    
    found_keywords = [kw for kw in keywords if kw in text_to_check or kw in opts_text]
    
    if found_keywords:
        print(f"ID {q.get('id')}: {q.get('text')}")
        print(f"Keywords: {', '.join(found_keywords)}")
        for i, opt in enumerate(options):
            print(f"  - {opt.get('text')}")
        print("-" * 40)
