"""Soạn lại toàn bộ đáp án ngân hàng câu hỏi bằng đúng quy trình RAG của Trợ lý (cùng form: >> kết luận, mục 1-4, căn cứ trong kho).
Kết quả ghi vào data/faq_regen/regen.json (chưa đụng vào kho_seed). Chạy tiếp được nếu bị ngắt.
  python tools/regen_faq.py [số luồng]
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from utils.rag_search import ask_ai_chi          # noqa: E402
from utils.answer_check import verify_answer     # noqa: E402
from utils.chat_format import clean_reply        # noqa: E402

BANK = ROOT / "kho_seed" / "faq_bank_2026.json"
OUT = ROOT / "data" / "faq_regen" / "regen.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


def one(item):
    q = item["question"]
    t = time.time()
    try:
        res = ask_ai_chi(question=q)
        if isinstance(res, dict) and res.get("source_type") in ("notebooklm", "docs", "web", "general"):
            res = verify_answer(q, res, 40.0)["result"]
        reply = clean_reply(res.get("reply", "")) if isinstance(res, dict) else ""
        return {"question": q, "old": item["answer"], "new": reply, "source_type": res.get("source_type") if isinstance(res, dict) else None, "secs": round(time.time() - t, 1)}
    except Exception as e:
        return {"question": q, "old": item["answer"], "new": "", "error": str(e)}


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    bank = json.load(open(BANK, encoding="utf-8"))
    done = {r["question"]: r for r in (json.load(open(OUT, encoding="utf-8")) if OUT.exists() else []) if r.get("new") and (not os.getenv("NEED_TT") or "truyền tin" in r["new"].lower())}
    todo = [x for x in bank if x["question"] not in done]
    print(f"{len(done)} đã xong, {len(todo)} còn lại", flush=True)
    results = list(done.values())
    with ThreadPoolExecutor(workers) as ex:
        for r in ex.map(one, todo):
            results.append(r)
            json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"[{len(results)}/{len(bank)}] {r.get('secs')}s {'OK' if r['new'] else 'LỖI'} {r['question'][:60]}", flush=True)


if __name__ == "__main__":
    main()
