"""
Cấu hình model dùng qua cổng 9router.

Các tài khoản Antigravity (model "ag/...") đã bị khóa, nên mặc định chuyển sang
model miễn phí NVIDIA Nemotron qua cổng OpenRouter trên 9router.
Đổi model không cần sửa mã: đặt ROUTER_MODEL (và tùy chọn ROUTER_FALLBACK_MODELS,
danh sách cách nhau bằng dấu phẩy) trong backend/.env.
"""
import os

DEFAULT_ROUTER_MODEL = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"


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
    for m in (os.getenv("ROUTER_FALLBACK_MODELS") or "").split(","):
        m = m.strip()
        if m and not _is_locked(m) and m not in models:
            models.append(m)
    return models
