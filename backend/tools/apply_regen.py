"""Áp dụng đáp án soạn lại (data/faq_regen/regen.json) vào kho_seed/faq_bank_2026.json, gộp theo câu hỏi (giữ câu do nơi khác vừa thêm).
Chạy tools/review_regen.py trước. Câu nào không đạt kiểm tra bị loại khỏi ngân hàng (khi hỏi sẽ đi qua RAG), không giữ đáp án cũ.
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "faq_regen"
rows = json.load(open(D / "regen.json", encoding="utf-8"))
bad = {r["question"] for r in json.load(open(D / "flagged.json", encoding="utf-8")) if r.get("issues")}
BANK = ROOT / "kho_seed" / "faq_bank_2026.json"
shutil.copy(BANK, BANK.with_suffix(f".bak-regen-{datetime.now():%Y%m%d%H%M}.json"))
bank = json.load(open(BANK, encoding="utf-8"))
new = {r["question"]: r["new"] for r in rows if r.get("new") and r["question"] not in bad}
known = {r["question"] for r in rows}
out, replaced, dropped = [], 0, []
for x in bank:
    if x["question"] in new:
        x["answer"] = new[x["question"]]; replaced += 1; out.append(x)
    elif x["question"] in known:
        dropped.append(x["question"])
    else:
        out.append(x)
json.dump(out, open(BANK, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"thay {replaced}, loại {len(dropped)}: {dropped}")
