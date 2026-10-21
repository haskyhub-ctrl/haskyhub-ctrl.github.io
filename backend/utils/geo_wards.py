"""Xác định xã, phường từ tọa độ GPS bằng ranh giới 99 xã phường của tỉnh Bắc Ninh (file bacninh_communes.geojson).

Chạy hoàn toàn trên máy chủ, không gọi dịch vụ bản đồ bên ngoài, không tốn phí.
Dùng thư viện shapely nếu có (nhanh, cho việc rà 44.000 tọa độ); nếu chưa cài thì dùng cách tự tính (đủ cho một điểm).
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.path.join(_HERE, "..", "..", "frontend", "data", "bacninh_communes.geojson"),
    os.path.join(os.getcwd(), "frontend", "data", "bacninh_communes.geojson"),
    os.path.join(os.getcwd(), "..", "frontend", "data", "bacninh_communes.geojson"),
]

try:
    from shapely.geometry import Point, shape
    from shapely.strtree import STRtree
    HAVE_SHAPELY = True
except Exception:  # pragma: no cover
    HAVE_SHAPELY = False

_state = {"wards": None, "tree": None}


def _ward_name(props: dict) -> str:
    kind = (props.get("loai") or "Xã").strip()
    return f"{kind} {props.get('ten_xa', '').strip()}".strip()


def _load():
    if _state["wards"] is not None:
        return _state["wards"]
    path = next((p for p in _CANDIDATES if os.path.exists(p)), None)
    wards = []
    if path:
        data = json.load(open(path, encoding="utf-8"))
        for f in data.get("features", []):
            p = f.get("properties", {})
            item = {"ward": _ward_name(p), "code": p.get("ma_xa"), "province": "Tỉnh " + (p.get("ten_tinh") or "Bắc Ninh"), "geom": f["geometry"]}
            if HAVE_SHAPELY:
                item["shape"] = shape(f["geometry"])
            else:
                item["bbox"] = _bbox(f["geometry"])
            wards.append(item)
    _state["wards"] = wards
    if HAVE_SHAPELY and wards:
        _state["tree"] = STRtree([w["shape"] for w in wards])
    return wards


def _polys(geom):
    return [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]


def _bbox(geom):
    xs, ys = [], []
    for poly in _polys(geom):
        for x, y in poly[0]:
            xs.append(x)
            ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def _in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


def _in_geom(x, y, geom):
    for poly in _polys(geom):
        if _in_ring(x, y, poly[0]) and not any(_in_ring(x, y, h) for h in poly[1:]):
            return True
    return False


def locate(lat, lng):
    """Trả {"ward": "Xã An Lạc", "code": "...", "province": "Tỉnh Bắc Ninh"} hoặc None nếu ngoài địa giới tỉnh."""
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        return None
    wards = _load()
    if not wards:
        return None
    if HAVE_SHAPELY:
        pt = Point(lng, lat)
        for i in _state["tree"].query(pt):
            w = wards[int(i)]
            if w["shape"].covers(pt):
                return {"ward": w["ward"], "code": w["code"], "province": w["province"]}
        return None
    for w in wards:
        x0, y0, x1, y1 = w["bbox"]
        if x0 <= lng <= x1 and y0 <= lat <= y1 and _in_geom(lng, lat, w["geom"]):
            return {"ward": w["ward"], "code": w["code"], "province": w["province"]}
    return None


def ward_key(name: str) -> str:
    """Khóa so sánh tên xã phường (bỏ tiền tố Xã, Phường, không phân biệt hoa thường)."""
    return re.sub(r"^(xã|phường|thị trấn)\s+", "", (name or "").strip().lower()).strip()


def ward_shapes():
    """Danh sách (tên xã phường, hình học shapely) để rà soát hàng loạt. Cần shapely."""
    return [(w["ward"], w["shape"]) for w in _load()] if HAVE_SHAPELY else []


def locate_many(points):
    """Xác định xã phường cho nhiều điểm cùng lúc. points: list (lat, lng). Trả list tên xã phường hoặc None. Cần shapely."""
    wards = _load()
    out = [None] * len(points)
    if not (HAVE_SHAPELY and wards and points):
        return out
    import numpy as np
    from shapely import points as make_points
    pts = make_points(np.array([[p[1], p[0]] for p in points], dtype=float))
    idx_in, idx_ward = _state["tree"].query(pts, predicate="within")
    for i, w in zip(idx_in.tolist(), idx_ward.tolist()):
        if out[i] is None:
            out[i] = wards[w]["ward"]
    return out
