"""Bộ nhớ đệm câu trả lời: câu hỏi giống nhau được trả lời tức thì thay vì gọi AI lại (mất 20 đến 60 giây).

Chỉ lưu câu hỏi không gắn với hồ sơ cá nhân và không có lịch sử hội thoại. Tự hết hạn sau CACHE_TTL giây, và bị xóa khi
kho tài liệu thay đổi (đổi tài liệu, tầng, trạng thái) hoặc khi có người báo câu trả lời chưa tốt.
"""
import hashlib
import threading
import time

from utils.kb_qa import question_key

CACHE_TTL = 12 * 3600
MAX_ENTRIES = 400
_lock = threading.Lock()
_store = {}          # key -> (thời điểm lưu, chữ ký kho, kết quả)


def _kho_signature() -> str:
    from utils import local_rag
    return hashlib.sha1(repr(local_rag._signature()).encode("utf-8", "replace")).hexdigest()[:16]


def _key(message: str) -> str:
    return question_key(message)


def get(message: str):
    k = _key(message)
    if not k:
        return None
    with _lock:
        item = _store.get(k)
    if not item:
        return None
    ts, sig, result = item
    if time.time() - ts > CACHE_TTL or sig != _kho_signature():
        with _lock:
            _store.pop(k, None)
        return None
    return dict(result)


def put(message: str, result: dict) -> None:
    k = _key(message)
    if not k or not isinstance(result, dict) or not result.get("reply"):
        return
    with _lock:
        if len(_store) >= MAX_ENTRIES:
            oldest = min(_store, key=lambda x: _store[x][0])
            _store.pop(oldest, None)
        _store[k] = (time.time(), _kho_signature(), dict(result))


def drop(message: str) -> None:
    with _lock:
        _store.pop(_key(message), None)
