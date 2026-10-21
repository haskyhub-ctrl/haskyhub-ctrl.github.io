"""Quản lý kho tài liệu của Trợ lý Chi và hàng chờ câu hỏi khó (chỉ dành cho quản trị).

Tài liệu tải lên được lưu ngoài git (backend/data/kho_tai_lieu), mỗi tài liệu có tầng và trạng thái hiệu lực.
Câu hỏi khó là những câu bot chưa có căn cứ trong kho; cán bộ nhập đáp án chuẩn, đáp án đã duyệt được ưu tiên trả lời.
"""
import os
import re
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth_middleware import get_current_user
from middleware.rbac import require_role
from models import KbQuestion, LawCandidate, User
from utils import local_rag
from utils.kb_qa import question_key

router = APIRouter(prefix="/api/admin/kho", tags=["Admin Kho"])

ALLOWED_EXTS = (".pdf", ".docx", ".txt")
MAX_BYTES = 80 * 1024 * 1024
MIN_READABLE_CHARS = 200          # ít hơn thế coi là bản quét, chưa đọc được chữ


def _admin(user: User):
    require_role("admin", "superadmin")(user)


def _doc_view(stored: str, meta: dict) -> dict:
    p = os.path.join(local_rag.KHO_DIR, stored)
    return {
        "id": stored,
        "title": meta.get("title") or meta.get("original_name") or stored,
        "original_name": meta.get("original_name"),
        "tier": meta.get("tier", local_rag.DEFAULT_TIER),
        "tier_label": local_rag.TIER_LABEL.get(meta.get("tier", local_rag.DEFAULT_TIER), ""),
        "status": meta.get("status", "inactive"),
        "effective_date": meta.get("effective_date") or "",
        "note": meta.get("note") or "",
        "uploaded_at": meta.get("uploaded_at"),
        "chars": meta.get("chars", 0),
        "chunks": meta.get("chunks", 0),
        "needs_ocr": bool(meta.get("needs_ocr")),
        "from_seed": bool(meta.get("from_seed")),
        "group": meta.get("group") or "",
        "size": os.path.getsize(p) if os.path.isfile(p) else 0,
    }


# ------------------------------------------------------------------ tài liệu
@router.get("/docs")
def list_docs(current_user: User = Depends(get_current_user)):
    _admin(current_user)
    man = local_rag.load_manifest()
    docs = [_doc_view(k, v) for k, v in man.items()]
    docs.sort(key=lambda d: (d["tier"], d["title"].lower()))
    builtin = []
    if os.path.isdir(local_rag.DOCS_DIR):
        builtin = sorted(f for f in os.listdir(local_rag.DOCS_DIR) if f.lower().endswith(local_rag._EXTS) and not f.startswith(("~$", ".")))
    return {"docs": docs, "builtin": builtin, "tiers": {str(k): v for k, v in local_rag.TIER_LABEL.items()}}


@router.post("/docs")
async def upload_doc(
    file: UploadFile = File(...),
    title: str = Form(""),
    tier: int = Form(2),
    status: str = Form("active"),
    effective_date: str = Form(""),
    note: str = Form(""),
    current_user: User = Depends(get_current_user),
):
    """Tải một tài liệu lên kho. PDF bản quét (không có chữ) được lưu nhưng để trạng thái chưa dùng, kèm cảnh báo."""
    _admin(current_user)
    name = file.filename or "tai_lieu"
    ext = os.path.splitext(name)[1].lower()
    if ext == ".doc":
        raise HTTPException(status_code=400, detail="Chưa đọc được định dạng .doc cũ. Vui lòng mở bằng Word, lưu lại thành .docx rồi tải lên.")
    if ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail="Chỉ nhận tệp PDF, DOCX hoặc TXT.")
    if tier not in local_rag.TIER_WEIGHT:
        raise HTTPException(status_code=400, detail="Tầng phải là 1, 2 hoặc 3.")
    if status not in ("active", "inactive"):
        raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ.")

    os.makedirs(local_rag.KHO_DIR, exist_ok=True)
    stored = uuid.uuid4().hex + ext
    path = os.path.join(local_rag.KHO_DIR, stored)
    size = 0
    with open(path, "wb") as out:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_BYTES:
                out.close()
                os.remove(path)
                raise HTTPException(status_code=413, detail="Tệp quá lớn (tối đa 80 MB).")
            out.write(chunk)

    text = local_rag.read_text(path)
    chars = len(text.strip())
    needs_ocr = ext == ".pdf" and chars < MIN_READABLE_CHARS
    meta = {
        "title": title.strip() or os.path.splitext(name)[0],
        "original_name": name,
        "tier": tier,
        "status": "inactive" if needs_ocr else status,
        "effective_date": effective_date.strip(),
        "note": note.strip(),
        "uploaded_at": datetime.utcnow().isoformat(),
        "uploaded_by": current_user.id,
        "chars": chars,
        "chunks": local_rag.count_chunks(text),
        "needs_ocr": needs_ocr,
    }
    if needs_ocr:
        meta["note"] = (meta["note"] + " " if meta["note"] else "") + "Tệp là bản quét, chưa đọc được chữ. Cần bản có chữ (hoặc nhận dạng chữ OCR) mới dùng được."
    man = local_rag.load_manifest()
    man[stored] = meta
    local_rag.save_manifest(man)
    info = local_rag.reindex()
    return {"doc": _doc_view(stored, meta), "index": info, "warning": "Tệp chưa đọc được chữ nên chưa được dùng để trả lời." if needs_ocr else None}


class DocUpdate(BaseModel):
    title: Optional[str] = None
    tier: Optional[int] = None
    status: Optional[str] = None
    effective_date: Optional[str] = None
    note: Optional[str] = None


@router.patch("/docs/{doc_id}")
def update_doc(doc_id: str, body: DocUpdate, current_user: User = Depends(get_current_user)):
    _admin(current_user)
    man = local_rag.load_manifest()
    meta = man.get(doc_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    if body.tier is not None:
        if body.tier not in local_rag.TIER_WEIGHT:
            raise HTTPException(status_code=400, detail="Tầng phải là 1, 2 hoặc 3.")
        meta["tier"] = body.tier
    if body.status is not None:
        if body.status not in ("active", "inactive"):
            raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ.")
        if body.status == "active" and meta.get("needs_ocr"):
            raise HTTPException(status_code=400, detail="Tệp này chưa đọc được chữ nên chưa thể đưa vào sử dụng.")
        meta["status"] = body.status
    for f in ("title", "effective_date", "note"):
        v = getattr(body, f)
        if v is not None:
            meta[f] = v.strip()
    meta["admin_edited"] = True     # bộ nạp sẵn không ghi đè các chỉnh sửa của quản trị viên
    local_rag.save_manifest(man)
    local_rag.reindex()
    return _doc_view(doc_id, meta)


@router.delete("/docs/{doc_id}")
def delete_doc(doc_id: str, current_user: User = Depends(get_current_user)):
    _admin(current_user)
    man = local_rag.load_manifest()
    if doc_id not in man:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    man.pop(doc_id)
    local_rag.save_manifest(man)
    if doc_id.startswith("seed_"):
        from utils.kho_seed import mark_deleted
        mark_deleted(doc_id)        # không để bộ nạp sẵn chép lại tài liệu đã xóa
    p = os.path.join(local_rag.KHO_DIR, os.path.basename(doc_id))
    if os.path.isfile(p):
        os.remove(p)
    local_rag.reindex()
    return {"deleted": True}


@router.post("/reindex")
def reindex(current_user: User = Depends(get_current_user)):
    _admin(current_user)
    return local_rag.reindex()


@router.get("/test-search")
def test_search(q: str = Query(..., min_length=2), current_user: User = Depends(get_current_user)):
    """Thử tìm trong kho: xem Trợ lý Chi sẽ lấy những đoạn nào làm căn cứ cho một câu hỏi."""
    _admin(current_user)
    hits = local_rag.search(q, k=5)
    return [{"source": s, "tier": local_rag.TIER_LABEL.get(t, ""), "score": sc, "text": txt[:500]} for s, txt, sc, t in hits]


# ------------------------------------------------------------------ câu hỏi khó
class QuestionIn(BaseModel):
    question: str
    answer: Optional[str] = None


class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    status: Optional[str] = None


def _q_view(r: KbQuestion) -> dict:
    return {
        "id": r.id, "question": r.question, "answer": r.answer or "", "status": r.status,
        "times_asked": r.times_asked or 1, "source": r.source,
        "last_asked_at": r.last_asked_at.isoformat() if r.last_asked_at else None,
        "answered_at": r.answered_at.isoformat() if r.answered_at else None,
    }


@router.get("/questions")
def list_questions(
    status: str = Query("pending", pattern="^(pending|approved|rejected|all)$"),
    q: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _admin(current_user)
    qry = db.query(KbQuestion)
    if status != "all":
        qry = qry.filter(KbQuestion.status == status)
    if q:
        qry = qry.filter(KbQuestion.question.ilike(f"%{q.strip()}%"))
    rows = qry.order_by(KbQuestion.times_asked.desc(), KbQuestion.last_asked_at.desc()).limit(300).all()
    counts = {s: db.query(KbQuestion).filter(KbQuestion.status == s).count() for s in ("pending", "approved", "rejected")}
    return {"items": [_q_view(r) for r in rows], "counts": counts}


@router.post("/questions")
def add_question(body: QuestionIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Cán bộ tự thêm một câu hỏi và đáp án chuẩn (có đáp án thì duyệt luôn)."""
    _admin(current_user)
    text = body.question.strip()
    if len(text) < 6:
        raise HTTPException(status_code=400, detail="Câu hỏi quá ngắn.")
    ans = (body.answer or "").strip()
    now = datetime.utcnow()
    row = KbQuestion(question=text[:1500], question_key=question_key(text), answer=ans or None,
                     status="approved" if ans else "pending", source="admin", times_asked=0,
                     answered_at=now if ans else None, answered_by=current_user.id if ans else None)
    db.add(row)
    db.commit()
    return _q_view(row)


@router.put("/questions/{qid}")
def update_question(qid: str, body: QuestionUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _admin(current_user)
    row = db.get(KbQuestion, qid)
    if not row:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")
    if body.question is not None and body.question.strip():
        row.question = body.question.strip()[:1500]
        row.question_key = question_key(row.question)
    if body.answer is not None:
        row.answer = body.answer.strip() or None
        row.answered_at = datetime.utcnow()
        row.answered_by = current_user.id
    if body.status is not None:
        if body.status not in ("pending", "approved", "rejected"):
            raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ.")
        if body.status == "approved" and not (row.answer or "").strip():
            raise HTTPException(status_code=400, detail="Cần nhập đáp án trước khi duyệt.")
        row.status = body.status
    db.commit()
    return _q_view(row)


@router.delete("/questions/{qid}")
def delete_question(qid: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _admin(current_user)
    row = db.get(KbQuestion, qid)
    if not row:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")
    db.delete(row)
    db.commit()
    return {"deleted": True}


# ------------------------------------------------------------------ văn bản mới theo dõi hằng tuần
def _lc_view(r: LawCandidate) -> dict:
    return {
        "id": r.id, "url": r.url, "title": r.title, "snippet": r.snippet or "", "source": r.source or "", "published": r.published or "",
        "found_at": r.found_at.isoformat() if r.found_at else None, "status": r.status, "kind": r.kind or "",
        "summary": r.summary or "", "hint": r.hint or "", "kho_doc_id": r.kho_doc_id,
    }


@router.get("/watch")
def watch_list(status: str = Query("new", pattern="^(new|ingested|ignored|all)$"), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _admin(current_user)
    from utils import law_watch
    qry = db.query(LawCandidate)
    if status == "all":
        qry = qry.filter(LawCandidate.relevant.is_(True))
    else:
        qry = qry.filter(LawCandidate.status == status)
        if status == "new":
            qry = qry.filter(LawCandidate.relevant.is_(True))
    rows = qry.order_by(LawCandidate.found_at.desc()).limit(200).all()
    counts = {s: db.query(LawCandidate).filter(LawCandidate.status == s, LawCandidate.relevant.is_(True)).count() for s in ("new", "ingested", "ignored")}
    return {"items": [_lc_view(r) for r in rows], "counts": counts, "last_run": law_watch.last_run()}


_watch_running = {"on": False}


@router.post("/watch/run")
def watch_run(current_user: User = Depends(get_current_user)):
    """Chạy ngay một lượt tìm văn bản mới (chạy nền, vài phút)."""
    _admin(current_user)
    import threading
    if _watch_running["on"]:
        return {"started": False, "message": "Đang chạy, vui lòng chờ."}
    from database import SessionLocal
    from utils import law_watch

    def job():
        _watch_running["on"] = True
        db = SessionLocal()
        try:
            law_watch.run(db)
        except Exception as e:
            print(f"[law_watch] Lỗi chạy tay: {e}")
        finally:
            db.close()
            _watch_running["on"] = False

    threading.Thread(target=job, daemon=True).start()
    return {"started": True, "message": "Đã bắt đầu tìm văn bản mới, vài phút nữa bấm làm mới để xem kết quả."}


@router.get("/watch/status")
def watch_status(current_user: User = Depends(get_current_user)):
    _admin(current_user)
    from utils import law_watch
    return {"running": _watch_running["on"], "last_run": law_watch.last_run()}


@router.post("/watch/{cid}/ignore")
def watch_ignore(cid: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _admin(current_user)
    r = db.get(LawCandidate, cid)
    if not r:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục")
    r.status, r.reviewed_at = "ignored", datetime.utcnow()
    db.commit()
    return _lc_view(r)


@router.post("/watch/{cid}/ingest")
def watch_ingest(cid: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Tải nội dung về kho ở dạng nháp (chưa dùng để trả lời, cán bộ rà soát rồi bật ở mục Tài liệu)."""
    _admin(current_user)
    r = db.get(LawCandidate, cid)
    if not r:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục")
    from utils import law_watch
    try:
        res = law_watch.ingest_url(r.url, r.title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Không nạp được: {e}")
    r.status, r.kho_doc_id, r.reviewed_at = "ingested", res["id"], datetime.utcnow()
    db.commit()
    return {"item": _lc_view(r), "chars": res["chars"]}


# ------------------------------------------------------------------ xem, sửa nội dung tài liệu
class DocText(BaseModel):
    text: str


def _doc_path(doc_id: str) -> str:
    return os.path.join(local_rag.KHO_DIR, os.path.basename(doc_id))


@router.get("/docs/{doc_id}/text")
def doc_text(doc_id: str, current_user: User = Depends(get_current_user)):
    _admin(current_user)
    man = local_rag.load_manifest()
    if doc_id not in man or not os.path.isfile(_doc_path(doc_id)):
        raise HTTPException(status_code=404, detail="Không tìm thấy nội dung tài liệu")
    with open(_doc_path(doc_id), "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return {"id": doc_id, "title": man[doc_id].get("title"), "status": man[doc_id].get("status"), "text": text[:400000], "truncated": len(text) > 400000}


@router.put("/docs/{doc_id}/text")
def doc_text_save(doc_id: str, body: DocText, current_user: User = Depends(get_current_user)):
    """Sửa nội dung tài liệu dạng văn bản (trang wiki, tài liệu từ bộ nạp sẵn hoặc từ web)."""
    _admin(current_user)
    man = local_rag.load_manifest()
    meta = man.get(doc_id)
    if not meta or not doc_id.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Chỉ sửa được tài liệu dạng văn bản (.txt)")
    text = body.text.strip()
    if len(text) < 50:
        raise HTTPException(status_code=400, detail="Nội dung quá ngắn")
    with open(_doc_path(doc_id), "w", encoding="utf-8") as f:
        f.write(text)
    meta["chars"] = len(text)
    meta["chunks"] = local_rag.count_chunks(text)
    meta["admin_edited"] = True
    local_rag.save_manifest(man)
    local_rag.reindex()
    return _doc_view(doc_id, meta)


# ------------------------------------------------------------------ wiki tri thức
_wiki_job = {"running": False, "done": 0, "total": 0, "current": "", "errors": []}


@router.get("/wiki")
def wiki_list(current_user: User = Depends(get_current_user)):
    _admin(current_user)
    from utils import wiki
    return {"topics": wiki.status(), "job": dict(_wiki_job)}


class WikiGen(BaseModel):
    slugs: Optional[list] = None      # bỏ trống: biên soạn các chủ đề chưa có trang


@router.post("/wiki/generate")
def wiki_generate(body: WikiGen, current_user: User = Depends(get_current_user)):
    """Biên soạn trang wiki bằng AI (chạy nền, mỗi trang khoảng nửa phút). Trang mới ở dạng nháp."""
    _admin(current_user)
    import threading
    from utils import wiki
    if _wiki_job["running"]:
        return {"started": False, "message": "Đang biên soạn, vui lòng chờ."}
    slugs = body.slugs or [t["slug"] for t in wiki.status() if t["state"] == "none"]
    slugs = [s for s in slugs if s in wiki.TOPIC_BY_SLUG]
    if not slugs:
        return {"started": False, "message": "Không có chủ đề nào cần biên soạn."}

    def job():
        _wiki_job.update({"running": True, "done": 0, "total": len(slugs), "current": "", "errors": []})
        for sl in slugs:
            _wiki_job["current"] = wiki.TOPIC_BY_SLUG[sl][1]
            try:
                wiki.generate(sl)
            except Exception as e:
                _wiki_job["errors"].append(f"{wiki.TOPIC_BY_SLUG[sl][1]}: {str(e)[:120]}")
            _wiki_job["done"] += 1
        _wiki_job.update({"running": False, "current": ""})

    threading.Thread(target=job, daemon=True).start()
    return {"started": True, "message": f"Đã bắt đầu biên soạn {len(slugs)} trang, mỗi trang khoảng nửa phút."}
