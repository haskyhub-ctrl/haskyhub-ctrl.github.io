"""
Cấu hình model dùng qua cổng 9router.

Các tài khoản Antigravity (model "ag/...") đã bị khóa và cổng OpenRouter không ổn định,
nên mặc định dùng cổng Codex ("cx/...") trên 9router, bản Luna (nhẹ, nhanh).
Đổi model không cần sửa mã: đặt ROUTER_MODEL (và tùy chọn ROUTER_FALLBACK_MODELS,
danh sách cách nhau bằng dấu phẩy) trong backend/.env.
"""
import os

DEFAULT_ROUTER_MODEL = "cx/gpt-6-luna"
# Dự phòng khi không đặt ROUTER_FALLBACK_MODELS
DEFAULT_FALLBACK_MODELS = ["cx/gpt-5.6-luna"]


def _is_locked(model: str) -> bool:
    # Model Antigravity ("ag/...") đều đi qua tài khoản đã bị khóa, bỏ qua để không tốn thời gian chờ lỗi.
    return model.startswith("ag/")


def get_router_model() -> str:
    model = (os.getenv("ROUTER_MODEL") or "").strip()
    if not model or _is_locked(model):
        return DEFAULT_ROUTER_MODEL
    return model


def get_router_models() -> list:
    """Danh sách model thử lần lượt: ROUTER_MODEL trước, sau đó ROUTER_FALLBACK_MODELS."""
    models = [get_router_model()]
    raw = os.getenv("ROUTER_FALLBACK_MODELS")
    fallbacks = raw.split(",") if raw is not None else DEFAULT_FALLBACK_MODELS
    for m in fallbacks:
        m = m.strip()
        if m and not _is_locked(m) and m not in models:
            models.append(m)
    return models
