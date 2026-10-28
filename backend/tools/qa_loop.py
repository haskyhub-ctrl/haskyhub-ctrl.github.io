"""Công cụ cho vòng lặp rà soát Trợ lý ảo hằng tuần (chạy bởi routine, 2 sub-agent: người hỏi và người rà soát).

Lệnh:
  python tools/qa_loop.py suggestions            In danh sách câu hỏi gợi ý mặc định (để người hỏi đan xen)
  python tools/qa_loop.py filter in.json         Bỏ các câu trùng hoặc gần giống câu đã hỏi ở các tuần trước (ghi đè in.json, in số câu còn lại)
  python tools/qa_loop.py ask  in.json out.json  Gửi từng câu hỏi trong in.json (["câu 1", ...]) tới /api/ai/chat, ghi out.json
  python tools/qa_loop.py apply verdicts.json    Áp dụng kết luận của người rà soát vào ngân hàng câu hỏi
      verdicts.json: [{"question": "...", "verdict": "ok|fix|drop", "answer": "đáp án đã sửa (khi fix, hoặc ok để nạp vào kho)", "value": "high|low (chỉ cho ok)", "reason": "..."}]
  Biến môi trường FRAS_BASE (mặc định http://localhost:8000).
Không tự commit hay đẩy lên GitHub; mọi thay đổi nằm trong thư mục làm việc để cán bộ xem và duyệt.
"""
import json
import os
import re
import shutil
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "kho_seed" / "faq_bank_2026.json"
BASE = os.getenv("FRAS_BASE", "http://localhost:8000").rstrip("/")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _ask_one(q):
    req = urllib.request.Request(BASE + "/api/ai/chat", data=json.dumps({"message": q}).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (FRAS qa loop)"})
    t = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=150))
        return {"question": q, "answer": r.get("reply", ""), "source_type": r.get("source_type"), "secs": round(time.time() - t, 1)}
    except Exception as e:
        return {"question": q, "answer": "", "error": str(e), "secs": round(time.time() - t, 1)}


def cmd_suggestions():
    js = (ROOT.parent / "frontend" / "js" / "chatbot.js").read_text(encoding="utf-8")
    m = re.search(r"suggestionPool\s*[:=]\s*\[(.*?)\]", js, re.S)
    pool = re.findall(r"['\"`]([^'\"`]{8,})['\"`]", m.group(1)) if m else []
    print(json.dumps(pool, ensure_ascii=False, indent=1))


HISTORY = ROOT / "data" / "qa_loop" / "asked_questions.json"


def _toks(q):
    return set(re.findall(r"\w+", q.lower()))


def _load_history():
    return json.load(open(HISTORY, encoding="utf-8")) if HISTORY.exists() else []


def cmd_filter(src):
    hist = [_toks(q) for q in _load_history()]
    qs, seen, kept = json.load(open(src, encoding="utf-8")), [], []
    for q in qs:
        t = _toks(q)
        if any(t and h and len(t & h) / len(t | h) >= 0.75 for h in hist + seen):
            continue
        kept.append(q); seen.append(t)
    json.dump(kept, open(src, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"giữ {len(kept)}/{len(qs)} câu (bỏ {len(qs) - len(kept)} câu trùng lịch sử); lịch sử {len(hist)} câu")


def cmd_ask(src, dst):
    qs = json.load(open(src, encoding="utf-8"))
    out = []
    for i, q in enumerate(qs, 1):
        out.append(_ask_one(q))
        print(f"[{i}/{len(qs)}] {out[-1]['secs']}s {q[:70]}", flush=True)
        json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    hist = _load_history()
    json.dump(hist + [q for q in qs if q not in hist], open(HISTORY, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _valid_answer(a):
    return bool(a) and a.lstrip().startswith(">>") and "## 1." in a and not re.search(r"\bChi\b", a) and "<br" not in a


BANK_CAP = 400          # trần số câu trả lời sẵn
MAX_AGE_DAYS = 180      # câu nạp tự động quá hạn này sẽ bị loại khi kho đầy
SIMILAR = 0.7           # giống từ ngưỡng này thì sửa câu cũ, không thêm câu mới


def cmd_apply(path):
    """Quy tắc: chỉ nạp câu sửa lại (fix) và câu đúng có giá trị cao (value=high); câu giống câu đã có thì thay đáp án câu đó; kho có trần và hạn dùng."""
    verdicts = json.load(open(path, encoding="utf-8"))
    bank = json.load(open(BANK, encoding="utf-8"))
    backup = BANK.with_suffix(f".bak-{datetime.now():%Y%m%d%H%M}.json")
    shutil.copy(BANK, backup)
    today = datetime.now().strftime("%Y-%m-%d")
    by_q = {x["question"].strip(): x for x in bank}
    toks = lambda q: set(re.findall(r"\w+", q.lower()))
    removed_q = []
    added = fixed = dropped = skipped = low = merged = pruned = full = 0
    for v in verdicts:
        q, kind, ans = v.get("question", "").strip(), v.get("verdict"), (v.get("answer") or "").strip()
        if kind == "drop":
            if q in by_q:
                bank.remove(by_q.pop(q)); removed_q.append(q); dropped += 1
            continue
        if kind not in ("ok", "fix"):
            continue
        if not _valid_answer(ans):
            skipped += 1; continue
        # Cổng kiểm tra bắt buộc: kết luận về diện thẩm định thiết kế không được trái Phụ lục III NĐ 105/2025 (sửa đổi NĐ 347/2026)
        sys.path.insert(0, str(ROOT))
        from utils.tham_dinh import check_reply
        gate = check_reply(q, ans)
        if not gate["ok"]:
            print("BỊ CHẶN (sai diện thẩm định):", q[:80], "|", gate["problem"][:120])
            skipped += 1; continue
        if q in by_q:
            if by_q[q]["answer"] != ans:
                by_q[q]["answer"] = ans; fixed += 1
            continue
        if kind == "ok" and v.get("value") != "high":
            low += 1; continue                      # câu đúng nhưng ít giá trị: chỉ ghi báo cáo
        t = toks(q)
        near = next((x for x in bank if t and toks(x["question"]) and len(t & toks(x["question"])) / len(t | toks(x["question"])) >= SIMILAR), None)
        if near is not None:
            near["answer"] = ans; merged += 1       # giống câu đã có: sửa câu đó, không thêm mới
            continue
        if len(bank) >= BANK_CAP:                   # kho đầy: loại câu nạp tự động đã quá hạn
            old = [x for x in bank if x.get("added") and (datetime.now() - datetime.strptime(x["added"], "%Y-%m-%d")).days > MAX_AGE_DAYS]
            if old:
                bank.remove(old[0]); by_q.pop(old[0]["question"].strip(), None); removed_q.append(old[0]["question"]); pruned += 1
            else:
                full += 1; continue
        item = {"question": q, "answer": ans, "added": today}
        bank.append(item); by_q[q] = item; added += 1
    json.dump(bank, open(BANK, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # Đồng bộ vào bảng kb_questions và xóa các câu đã loại
    sys.path.insert(0, str(ROOT))
    from database import SessionLocal
    from models import KbQuestion
    from utils.faq_auditor import seed_200_faqs
    db = SessionLocal()
    for q in removed_q:
        db.query(KbQuestion).filter(KbQuestion.question == q).delete(synchronize_session=False)
    db.commit()
    seed_200_faqs(db, force_update=True)
    print(json.dumps({"added": added, "fixed": fixed, "merged_into_similar": merged, "dropped": dropped, "pruned_old": pruned,
                      "skipped_low_value": low, "skipped_invalid": skipped, "skipped_bank_full": full, "bank_size": len(bank), "backup": backup.name}, ensure_ascii=False))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["suggestions"]:
        cmd_suggestions()
    elif a[:1] == ["filter"] and len(a) == 2:
        cmd_filter(a[1])
    elif a[:1] == ["ask"] and len(a) == 3:
        cmd_ask(a[1], a[2])
    elif a[:1] == ["apply"] and len(a) == 2:
        cmd_apply(a[1])
    else:
        print(__doc__)
