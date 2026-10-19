"""Dựng kho tri thức phân tích dự phòng (data_docs/analysis_library_seed.json) bằng AI.

Với mỗi cặp (câu hỏi, đáp án mức cao hoặc rất cao) trong CSDL, nhờ AI viết sẵn: tình trạng ghi nhận và khuyến nghị
(theo đúng quy tắc trong utils/ai_rules.py). Khi AI không hoạt động, hệ thống soạn bản phân tích từ kho này.

Cách chạy (từ thư mục backend, có kết nối tới dịch vụ AI):
    python build_analysis_library.py            # dựng các mục còn thiếu (chạy lại được, tự bỏ qua mục đã có)
    python build_analysis_library.py --index    # chỉ lập chỉ mục kho vào ChromaDB (cần GEMINI_API_KEY)

Chạy lại mỗi khi thêm hoặc sửa nhiều câu hỏi. Mục AI học thêm khi chạy thật nằm ở file riêng, không bị ghi đè.
"""
import asyncio
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Question, QuestionOption
from routers.ai_analysis import call_gemini
from utils.ai_prompt import CURRENT_LEGAL_REFERENCES, FACILITY_TYPE_LABELS
from utils.ai_rules import rules_as_prompt, sanitize_analysis
from utils.analysis_library import SEED_PATH, entry_key, normalize_deadline, index_chroma

BATCH = 8
PARALLEL = 4
LEVEL = {3: "RẤT CAO", 2: "CAO"}


def collect_items():
    db = SessionLocal()
    try:
        items = []
        for q in db.query(Question).filter(Question.is_active == True).all():
            for o in q.options:
                if o.score >= 2:
                    ft = q.facility_type if q.facility_type and q.facility_type != "all" else ""
                    items.append({
                        "key": entry_key(q.question_text, o.option_text),
                        "question": q.question_text,
                        "option_text": o.option_text,
                        "score": o.score,
                        "category": q.category.name if q.category else "",
                        "ftype": ft,
                    })
        return items
    finally:
        db.close()


def build_prompt(batch):
    legal = "\n".join(f"  - {r}" for r in CURRENT_LEGAL_REFERENCES)
    lines = []
    for i, it in enumerate(batch, 1):
        lines.append(f"[{i}] Nhóm: {it['category']} | Mức {LEVEL.get(it['score'], 'CAO')}\n    Câu hỏi: {it['question']}\n    Cơ sở trả lời: {it['option_text']}")
    return f"""Bạn là chuyên gia tư vấn an toàn phòng cháy chữa cháy và cứu nạn cứu hộ, hỗ trợ Phòng Cảnh sát PCCC và CNCH, Công an thành phố Bắc Ninh.
Hệ thống FRAS giúp người dân và cơ sở TỰ KIỂM TRA, nhận hướng dẫn an toàn miễn phí; kết quả không dùng để xử phạt.
Dưới đây là {len(batch)} câu trả lời có nguy cơ. Với MỖI mục, hãy viết một mục kho tri thức gồm:
- issue: một câu mô tả tình trạng ghi nhận, bám đúng câu trả lời, giọng trung lập.
- title: tiêu đề khuyến nghị bắt đầu bằng động từ, tối đa 14 từ.
- description: 2-4 câu các bước làm cụ thể, vật tư phổ thông, làm được tại nhà hoặc cơ sở nhỏ.
- priority: urgent | high | medium (urgent cho nguy cơ trực tiếp gây cháy: điện, nguồn nhiệt, rò gas, mức RẤT CAO).
- deadline: chỉ dùng một trong các nhãn: Làm ngay (trong 24-48 giờ); Trong 7 ngày; Trong 15 ngày; Trong 30 ngày; Trong 60 ngày.
- responsible_party: người thực hiện (ví dụ: Chủ cơ sở, Thợ điện có chuyên môn).
- legal_basis: tên văn bản trong danh mục dưới đây, hoặc chuỗi rỗng nếu không chắc; không ghi số Điều/Khoản nếu không chắc.

DANH MỤC VĂN BẢN ĐƯỢC PHÉP VIỆN DẪN:
{legal}

QUY TẮC BẮT BUỘC:
{rules_as_prompt()}

CÁC MỤC CẦN VIẾT:
{chr(10).join(lines)}

Trả về đúng một khối JSON: {{"entries": [{{"id": 1, "issue": "...", "title": "...", "description": "...", "priority": "...", "deadline": "...", "responsible_party": "...", "legal_basis": "..."}}]}}
"""


async def run_batch(batch, sem, out, lock, n_done, total):
    async with sem:
        for attempt in range(3):
            try:
                res = await call_gemini(build_prompt(batch), temperature=0.3, timeout=150.0)
                ents = res.get("entries") if isinstance(res, dict) else None
                if not ents:
                    raise ValueError("AI không trả về entries")
                got = 0
                for e in ents:
                    i = e.get("id")
                    if not isinstance(i, int) or not (1 <= i <= len(batch)):
                        continue
                    it = batch[i - 1]
                    if not (e.get("title") and e.get("description")):
                        continue
                    prio = e.get("priority") if e.get("priority") in ("urgent", "high", "medium", "low") else "high"
                    entry = {
                        "question": it["question"], "option_text": it["option_text"], "score": it["score"],
                        "category": it["category"], "facility_type": it["ftype"],
                        "issue": e.get("issue") or "",
                        "rec": {
                            "title": e["title"], "description": e["description"], "priority": prio,
                            "deadline": normalize_deadline(e.get("deadline"), prio),
                            "responsible_party": e.get("responsible_party") or "Chủ cơ sở",
                            "legal_basis": e.get("legal_basis") or "",
                        },
                        "source": "ai", "updated": datetime.utcnow().isoformat(timespec="seconds"),
                    }
                    async with lock:
                        out[it["key"]] = sanitize_analysis(entry)
                    got += 1
                n_done[0] += 1
                print(f"[{n_done[0]}/{total}] +{got}/{len(batch)} mục", flush=True)
                return
            except Exception as ex:
                print(f"  lỗi lô (lần {attempt + 1}): {ex}", flush=True)
                await asyncio.sleep(3)


def save(out):
    os.makedirs(os.path.dirname(SEED_PATH), exist_ok=True)
    tmp = SEED_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.utcnow().isoformat(timespec="seconds"), "entries": out}, f, ensure_ascii=False, indent=1)
    os.replace(tmp, SEED_PATH)


async def main():
    existing = {}
    if os.path.exists(SEED_PATH):
        existing = json.load(open(SEED_PATH, encoding="utf-8")).get("entries", {})
    items = [it for it in collect_items() if it["key"] not in existing]
    print(f"Cần dựng {len(items)} mục (đã có {len(existing)}).", flush=True)
    batches = [items[i:i + BATCH] for i in range(0, len(items), BATCH)]
    sem, lock, n_done = asyncio.Semaphore(PARALLEL), asyncio.Lock(), [0]
    out = dict(existing)

    async def saver():
        while n_done[0] < len(batches):
            await asyncio.sleep(20)
            async with lock:
                save(out)

    task = asyncio.create_task(saver()) if batches else None
    await asyncio.gather(*(run_batch(b, sem, out, lock, n_done, len(batches)) for b in batches))
    if task:
        task.cancel()
    save(out)
    print(f"Xong. Kho có {len(out)} mục.", flush=True)


if __name__ == "__main__":
    if "--index" in sys.argv:
        data = json.load(open(SEED_PATH, encoding="utf-8")).get("entries", {})
        print("Đã lập chỉ mục ChromaDB" if index_chroma(data) else "Chưa lập chỉ mục (thiếu thư viện hoặc GEMINI_API_KEY)")
    else:
        asyncio.run(main())
