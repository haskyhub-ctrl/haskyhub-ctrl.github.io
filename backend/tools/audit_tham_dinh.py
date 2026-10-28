"""Rà toàn bộ ngân hàng câu trả lời sẵn: câu nào trả lời về diện thẩm định thiết kế PCCC mâu thuẫn với Phụ lục III thì liệt kê.
  python tools/audit_tham_dinh.py        (thoát mã 1 nếu còn sai)
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from utils.tham_dinh import check_reply, evaluate  # noqa: E402

_N = r"(?:(?<![\d.])5\.000\s*m3|(?<![\d.])5\.000\s*m³|(?<![\d.])1\.500\s*m3)"
OLD = re.compile(r"(thẩm\s*(định|duyệt)[^.\n]{0,120}" + _N + "|" + _N + r"[^.\n]{0,120}thẩm\s*(định|duyệt))", re.I)
bank = json.load(open(os.path.join(ROOT, "kho_seed", "faq_bank_2026.json"), encoding="utf-8"))
bad = []
for x in bank:
    chk = check_reply(x["question"], x["answer"])
    stale = OLD.search(x["answer"])
    if not chk["ok"] or stale:
        bad.append((x["question"], chk["problem"] or "Dùng ngưỡng khối tích cũ cho thẩm định: " + stale.group(0)[:100]))
for q, why in bad:
    print("SAI:", q[:90], "\n     ", why[:220])
print(f"\n{len(bank) - len(bad)}/{len(bank)} câu không phát hiện sai lệch về diện thẩm định")
sys.exit(1 if bad else 0)
