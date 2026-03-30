import json

ids_to_keep = [120, 122, 132, 154, 40, 167, 54, 82, 19, 31, 36, 90]

with open("c:/Users/Hasky/.gemini/antigravity/scratch/fras/cau_hoi_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("c:/Users/Hasky/.gemini/antigravity/scratch/fras/tmp_check_ids.txt", "w", encoding="utf-8") as f:
    for q in data:
        if q.get("id") in ids_to_keep:
            f.write(f"ID: {q.get('id')} - {q.get('text')}\n")
