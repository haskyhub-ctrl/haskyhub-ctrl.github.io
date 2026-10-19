"""Mã theo dõi hồ sơ khảo sát cho người dân, hộ gia đình (không có tài khoản).

Người khảo sát không tài khoản chỉ có một phiên tạm, mất khi hết hạn hoặc đổi thiết bị. Mã theo dõi cho
họ quay lại bảng theo dõi tiến độ khắc phục (cập nhật Realtime cho cơ quan quản lý) bất cứ lúc nào, trên
bất kỳ thiết bị nào, mà không cần đăng ký tài khoản.

Mã gồm 10 ký tự (bảng chữ cái bỏ các ký tự dễ nhầm như 0/O, 1/I), hiển thị dạng ABCD-EFGH-JK:
khoảng 50 bit ngẫu nhiên nên không đoán được; nhập sai nhiều lần từ một địa chỉ sẽ bị tạm khóa.
"""
import secrets
import time
from collections import defaultdict, deque

ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
CODE_LENGTH = 10

_MAX_FAILS = 8          # số lần nhập sai tối đa
_WINDOW_SECONDS = 600   # trong 10 phút
_fails = defaultdict(deque)


def normalize_code(code: str) -> str:
    return "".join(ch for ch in (code or "").upper() if ch.isalnum())


def format_code(code: str) -> str:
    c = normalize_code(code)
    return f"{c[:4]}-{c[4:8]}-{c[8:]}" if len(c) == CODE_LENGTH else c


def new_code(db, model) -> str:
    """Sinh mã chưa trùng trong bảng (model.tracking_code)."""
    for _ in range(20):
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if not db.query(model).filter(model.tracking_code == code).first():
            return code
    raise RuntimeError("Không sinh được mã theo dõi")


def is_blocked(client_id: str) -> bool:
    q = _fails[client_id]
    now = time.time()
    while q and now - q[0] > _WINDOW_SECONDS:
        q.popleft()
    return len(q) >= _MAX_FAILS


def record_failure(client_id: str):
    _fails[client_id].append(time.time())


def clear_failures(client_id: str):
    _fails.pop(client_id, None)
