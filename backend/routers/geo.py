"""Tra cứu địa bàn từ tọa độ GPS (dùng khi người dân, cơ sở bấm "Lấy vị trí hiện tại" lúc khảo sát)."""
from fastapi import APIRouter, Query

from utils import geo_wards

router = APIRouter(prefix="/api/geo", tags=["Geo"])


@router.get("/locate")
def locate(lat: float = Query(..., ge=-90, le=90), lng: float = Query(..., ge=-180, le=180)):
    """Cho tọa độ, trả về xã phường của tỉnh Bắc Ninh chứa điểm đó. Ngoài địa giới tỉnh thì found = false."""
    r = geo_wards.locate(lat, lng)
    if not r:
        return {"found": False}
    return {"found": True, **r}
