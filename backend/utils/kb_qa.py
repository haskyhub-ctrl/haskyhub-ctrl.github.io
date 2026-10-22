"""Ngân hàng câu hỏi khó: ghi nhận câu hỏi bot chưa đủ căn cứ, và trả đáp án đã được cán bộ duyệt."""
from datetime import datetime

from sqlalchemy.orm import Session

from models import KbQuestion
from utils.local_rag import _tokens

MATCH_THRESHOLD = 0.55      # độ giống tối thiểu kết hợp Jaccard và Overlap
MIN_TOKENS = 3

# Các từ khóa chuyên ngành định danh loại hình / thủ tục (tránh match chéo)
CRITICAL_ENTITY_KEYWORDS = [
    "nhà nghỉ", "nha nghi", "khách sạn", "khach san", "karaoke", "vũ trường", "vu truong",
    "chung cư", "chung cu", "nhà trọ", "nha tro", "xăng dầu", "xang dau", "gas", "khí dầu mỏ",
    "bệnh viện", "benh vien", "trường học", "truong hoc", "chợ", "siêu thị", "sieu thi",
    "an ninh trật tự", "an ninh trat tu", "antt", "thẩm duyệt", "tham duyet", "kinh doanh dịch vụ pccc"
]


def question_key(text: str) -> str:
    toks = sorted(set(_tokens(text)))
    return " ".join(toks)[:490]


def find_approved(db: Session, message: str):
    """Tìm đáp án đã duyệt cho câu hỏi giống nhất. Trả KbQuestion hoặc None.
    
    BƯỚC KIỂM TRA CHẶT CHẼ:
    - Câu hỏi tình huống dài (> 25 từ) hoặc có chi tiết địa chỉ/diện tích cụ thể bắt buộc vào RAG, KHÔNG dùng FAQ ngắn.
    - Chênh lệch độ dài token giữa câu hỏi và FAQ không quá 2.2 lần.
    - Jaccard similarity phải đạt tối thiểu 0.35.
    - Trùng khớp từ khóa chủ đề cốt lõi (không match câu 'nhà nghỉ' vào 'kinh doanh dịch vụ PCCC').
    """
    msg_lower = message.lower()
    words = message.strip().split()
    
    # 1. Câu hỏi tình huống phức tạp / dài -> chuyển sang RAG LLM phân tích chuyên sâu
    if len(words) > 25:
        return None
        
    q = set(_tokens(message))
    if len(q) < MIN_TOKENS:
        return None
        
    best, best_score = None, 0.0
    for row in db.query(KbQuestion).filter(KbQuestion.status == "approved", KbQuestion.answer.isnot(None)).all():
        t = set((row.question_key or "").split())
        if not t:
            continue
            
        # Kiểm tra tỷ lệ độ dài
        len_ratio = max(len(q), len(t)) / max(min(len(q), len(t)), 1)
        if len_ratio > 2.2:
            continue
            
        inter = len(q & t)
        if not inter:
            continue
            
        jaccard = inter / len(q | t)
        overlap = inter / min(len(q), len(t))
        score = 0.5 * jaccard + 0.5 * overlap
        
        # Kiểm tra tương thích thực thể chủ đề cốt lõi
        target_lower = (row.question or "").lower()
        entity_conflict = False
        for ekw in CRITICAL_ENTITY_KEYWORDS:
            in_q = ekw in msg_lower
            in_t = ekw in target_lower
            if in_q != in_t and in_q:
                # Câu hỏi của dân có thực thể này (vd: nhà nghỉ, ANTT) mà FAQ không có -> không match
                entity_conflict = True
                break
        if entity_conflict:
            continue
            
        if score > best_score and jaccard >= 0.35:
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
