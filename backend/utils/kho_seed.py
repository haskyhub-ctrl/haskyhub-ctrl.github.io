"""Nạp sẵn bộ tài liệu pháp lý và hướng dẫn (thư mục kho_seed, nằm trong git) vào kho của Trợ lý Chi.

Mỗi tài liệu trong kho_seed/manifest.json có tầng, trạng thái hiệu lực, ngày hiệu lực và ghi chú.
Khi hệ thống khởi động, tài liệu nào chưa có trong kho thì được chép vào data/kho_tai_lieu.
Tài liệu đã bị quản trị viên chỉnh sửa hoặc xóa trên trang Kho tài liệu AI thì không bị ghi đè lại.
Muốn cập nhật nội dung hoặc trạng thái từ bộ nạp sẵn, tăng seed_rev của tài liệu đó trong manifest.
"""
import json
import os
import shutil
from datetime import datetime

from utils import local_rag

SEED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kho_seed")
SEED_MANIFEST = os.path.join(SEED_DIR, "manifest.json")
DELETED_PATH = os.path.join(local_rag.KHO_DIR, "seed_deleted.json")


def _deleted() -> set:
    try:
        with open(DELETED_PATH, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def mark_deleted(stored: str) -> None:
    d = _deleted()
    d.add(stored)
    os.makedirs(local_rag.KHO_DIR, exist_ok=True)
    with open(DELETED_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(d), f, ensure_ascii=False)


def sync_seed() -> dict:
    """Chép các tài liệu nạp sẵn vào kho. Trả {added, updated, total}."""
    try:
        with open(SEED_MANIFEST, "r", encoding="utf-8") as f:
            seed = json.load(f)
    except Exception:
        return {"added": 0, "updated": 0, "total": 0}
    man = local_rag.load_manifest()
    deleted = _deleted()
    os.makedirs(local_rag.KHO_DIR, exist_ok=True)
    added = updated = 0
    # Tài liệu đã thay bằng bản mới: gỡ khỏi kho (kể cả bản đã chép vào máy chủ) và không nạp lại
    try:
        with open(os.path.join(SEED_DIR, "retired.json"), "r", encoding="utf-8") as f:
            retired = json.load(f)
    except Exception:
        retired = []
    removed = False
    for sid in retired:
        stored = f"seed_{sid}.txt"
        deleted.add(stored)
        mark_deleted(stored)
        if stored in man:
            man.pop(stored, None)
            removed = True
        try:
            os.remove(os.path.join(local_rag.KHO_DIR, stored))
        except OSError:
            pass
    if removed:
        local_rag.save_manifest(man)
    for sid, meta in seed.items():
        stored = f"seed_{sid}.txt"
        src = os.path.join(SEED_DIR, f"{sid}.txt")
        if stored in deleted or not os.path.isfile(src):
            continue
        cur = man.get(stored)
        rev = int(meta.get("seed_rev", 1))
        if cur and (cur.get("admin_edited") or int(cur.get("seed_rev", 0)) >= rev):
            continue
        shutil.copyfile(src, os.path.join(local_rag.KHO_DIR, stored))
        with open(src, "r", encoding="utf-8") as f:
            text = f.read()
        entry = dict(meta)
        entry.update({
            "original_name": meta.get("source") or stored,
            "uploaded_at": datetime.utcnow().isoformat(),
            "from_seed": True, "seed_rev": rev,
            "chars": len(text), "chunks": local_rag.count_chunks(text),
            "needs_ocr": False,
        })
        man[stored] = entry
        if cur:
            updated += 1
        else:
            added += 1
    if added or updated:
        local_rag.save_manifest(man)
    return {"added": added, "updated": updated, "total": len(seed)}


FAQ_PATH = os.path.join(SEED_DIR, "faq.json")


def sync_faq(db) -> int:
    """Đồng bộ ngân hàng câu trả lời sẵn với kho_seed/faq_bank_2026.json (nguồn chuẩn, đã rà soát).
    Câu có trong tệp thì cập nhật đáp án; câu cũ nạp từ trước (nguồn seed, faq_bank_2026) không còn trong tệp thì xóa.
    Câu do cán bộ duyệt tay hoặc từ hàng chờ (nguồn khác) không bị đụng tới."""
    from models import KbQuestion
    from utils.kb_qa import question_key
    from utils.faq_auditor import seed_200_faqs
    stats = seed_200_faqs(db, force_update=True)
    bank_path = os.path.join(SEED_DIR, "faq_bank_2026.json")
    try:
        with open(bank_path, "r", encoding="utf-8") as f:
            keys = {question_key(it["question"]) for it in json.load(f) if it.get("question")}
    except Exception:
        return stats.get("added", 0)
    removed = 0
    for row in db.query(KbQuestion).filter(KbQuestion.source.in_(["seed", "faq_bank_2026"])).all():
        if row.question_key not in keys:
            db.delete(row)
            removed += 1
    if removed:
        db.commit()
    return stats.get("added", 0) + stats.get("updated", 0) + removed
