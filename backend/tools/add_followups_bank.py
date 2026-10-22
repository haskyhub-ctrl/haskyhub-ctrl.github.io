"""Bổ sung khối hỏi lại "?? " cho các đáp án trong faq_bank_2026.json còn thiếu (AI quyết định có cần không)."""
import json, re, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
sys.argv = sys.argv[:1]
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import importlib.util
src = (ROOT / "tools" / "add_followups.py").read_text(encoding="utf-8").split("rows = json.load")[0]
ns = {"__file__": str(ROOT / "tools" / "add_followups.py")}
exec(compile(src, "add_followups_head", "exec"), ns)
one = ns["one"]
BANK = ROOT / "kho_seed" / "faq_bank_2026.json"
bank = json.load(open(BANK, encoding="utf-8"))
shutil.copy(BANK, BANK.with_suffix(".bak-followups.json"))
def work(x):
    r = one({"question": x["question"], "new": x["answer"]})
    if r.get("followups"):
        x["answer"] = r["new"]
        return 1
    return 0
with ThreadPoolExecutor(4) as ex:
    n = sum(ex.map(work, [x for x in bank if not re.search(r"^\s*\?\?\s", x["answer"], re.M)]))
json.dump(bank, open(BANK, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("đã thêm hỏi lại cho", n, "câu")
