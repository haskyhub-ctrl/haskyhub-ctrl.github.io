"""Bổ sung khối hỏi lại "?? " cho các đáp án đã soạn lại (regen.json) mà còn thiếu, dựa trên nội dung đáp án.
  python tools/add_followups.py
"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from utils.rag_search import _call_llm, _extract_json_block  # noqa: E402

F = ROOT / "data" / "faq_regen" / "regen.json"
PROMPT = """Câu hỏi của người dân: {q}

Đáp án đã soạn:
{a}

Nhiệm vụ: nếu kết luận trong đáp án còn phụ thuộc vào thông tin người hỏi chưa nêu (loại hình cơ sở, tổng diện tích sàn, số tầng, chiều cao, số phòng/người, công năng, thời điểm xây dựng, tình trạng hồ sơ...), hãy nêu 2 đến 3 câu hỏi ngắn, cụ thể để người hỏi bổ sung, sao cho khi có đủ thì xác định được chính xác trường hợp áp dụng. Xưng "bạn", không xưng tên riêng. Nếu câu hỏi thuần kiến thức chung, không phụ thuộc quy mô/loại hình thì trả mảng rỗng.
Trả về DUY NHẤT JSON: {{"questions": ["...", "..."]}}"""


def one(r):
    a = r.get("new") or ""
    if not a or re.search(r"^\s*\?\?\s", a, re.M):
        return r
    try:
        raw = _call_llm(PROMPT.format(q=r["question"], a=a[:3500]), temperature=0.2, max_tokens=300, is_json=True, fast=True, timeout=40.0)
        qs = (_extract_json_block(raw) or {}).get("questions") or []
        qs = [q.strip().rstrip("?") + "?" for q in qs if isinstance(q, str) and 10 < len(q) < 200][:3]
    except Exception as e:
        print("lỗi:", r["question"][:50], e)
        return r
    if qs:
        marker = re.search(r"\n\s*~~ ", a)
        block = "\n" + "\n".join("?? " + q for q in qs)
        a = (a[:marker.start()].rstrip() + "\n" + block + a[marker.start():]) if marker else a.rstrip() + "\n" + block
        r["new"] = a
        r["followups"] = qs
    return r


rows = json.load(open(F, encoding="utf-8"))
with ThreadPoolExecutor(4) as ex:
    rows = list(ex.map(one, rows))
json.dump(rows, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("đã thêm hỏi lại cho", sum(1 for r in rows if r.get("followups")), "/", len(rows), "câu")
