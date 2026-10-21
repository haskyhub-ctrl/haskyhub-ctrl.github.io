"""Ngân hàng câu hỏi khó: ghi nhận câu hỏi bot chưa đủ căn cứ, và trả đáp án đã được cán bộ duyệt."""
from datetime import datetime

from sqlalchemy.orm import Session

from models import KbQuestion
from utils.local_rag import _tokens

MATCH_THRESHOLD = 0.6      # độ giống tối thiểu (Jaccard theo từ) để dùng đáp án đã duyệt
MIN_TOKENS = 3


def question_key(text: str) -> str:
    toks = sorted(set(_tokens(text)))
    return " ".join(toks)[:490]


def find_approved(db: Session, message: str):
    """Tìm đáp án đã duyệt cho câu hỏi giống nhất. Trả KbQuestion hoặc None."""
    q = set(_tokens(message))
    if len(q) < MIN_TOKENS:
        return None
    best, best_score = None, 0.0
    for row in db.query(KbQuestion).filter(KbQuestion.status == "approved", KbQuestion.answer.isnot(None)).all():
        t = set((row.question_key or "").split())
        if not t:
            continue
        score = len(q & t) / len(q | t)
        if score > best_score:
            best, best_score = row, score
    return best if best is not None and best_score >= MATCH_THRESHOLD else None


def log_unanswered(db: Session, message: str, source: str = "chat") -> None:
    """Ghi câu hỏi mà bot chưa có căn cứ trong kho (gộp các câu giống nhau, tăng số lần hỏi)."""
    key = question_key(message)
    if len(key.split()) < MIN_TOKENS:
        return
    row = db.query(KbQuestion).filter(KbQuestion.question_key == key).first()
    now = datetime.utcnow()
    if row:
        row.times_asked = (row.times_asked or 0) + 1
        row.last_asked_at = now
    else:
        db.add(KbQuestion(question=message.strip()[:1500], question_key=key, status="pending", source=source, last_asked_at=now))
    db.commit()
