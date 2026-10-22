"""Rà tự động các đáp án soạn lại (data/faq_regen/regen.json): form, lỗi cấm, văn bản hết hiệu lực, và khác biệt số liệu so với đáp án cũ."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
rows = json.load(open(ROOT / "data" / "faq_regen" / "regen.json", encoding="utf-8"))

STALE = r"(Luật (Phòng cháy, chữa cháy )?(số )?(27/2001|40/2013)|Nghị định (số )?(79/2014|136/2020|50/2024|83/2017|167/2013|28/2020)|Thông tư (số )?(149/2020|150/2020|66/2014))"
BAD = [
    ("thiếu cấu trúc", lambda a: not (a.lstrip().startswith(">>") and "## 1." in a and "## 2." in a and "## 3." in a and "## 4." in a)),
    ("có <br>", lambda a: "<br" in a),
    ("xưng Chi", lambda a: bool(re.search(r"(Chi (xin|sẽ|là|có thể|rất|hy vọng|gửi)|là Chi|Chào bạn, Chi)", a))),
    ("dẫn văn bản hết hiệu lực làm căn cứ", lambda a: bool(re.search(r"\{\{?[^}]*" + STALE, a))),
    ("kết luận cấp xã/cấp III cho cơ sở cụ thể", lambda a: bool(re.search(r"(thuộc thẩm quyền[^.\n]{0,60}UBND cấp xã|công trình cấp III trở xuống)", a))),
    ("còn 'tỉnh Bắc Ninh'", lambda a: bool(re.search(r"(?<!UBND )(?<!Công an )tỉnh Bắc Ninh", a))),
    ("xưng 'Tôi' sai/Chi", lambda a: False),
    ("lời chào/trả lời lạc đề", lambda a: a.lstrip().startswith(("Cảm ơn", "Chào")) or "Hãy đặt câu hỏi cụ thể hơn" in a),
]
nums = lambda t: set(re.findall(r"\d[\d.]*\s*(?:đồng|triệu|ngày|năm|tháng|m2|m²|tầng|%)", t))
flag = []
for r in rows:
    n = r.get("new") or ""
    issues = [name for name, f in BAD if f(n)] if n else ["không có đáp án mới"]
    if n and re.search(r"(khuyến khích[^.]{0,80}(không dây|đầu báo cháy khói độc lập|cảnh báo sớm))", n):
        issues.append("khuyến khích báo cháy không dây thay cho thiết bị truyền tin")
    if n and re.search(r"(trang bị|điều kiện|yêu cầu|hồ sơ quản lý|cần những gì)", r["question"], re.I) and re.search(r"(nhà trọ|khách sạn|nhà nghỉ|karaoke|chung cư|kho|xưởng|trạm|cửa hàng|nhà hàng|quán|trường|phòng khám|chợ|văn phòng|gara|cơ sở)", r["question"], re.I) and "truyền tin" not in n.lower() and not re.search(r"(lối thoát nạn|dịch vụ PCCC|mức phạt|tần suất|hồ sơ phương án)", r["question"], re.I):
        issues.append("thiếu thiết bị truyền tin báo sự cố")
    d_old, d_new = nums(r["old"]), nums(n)
    diff = sorted((d_old ^ d_new))[:12]
    r["issues"], r["num_diff"] = issues, diff
    if issues or (d_old and d_old - d_new):
        flag.append(r)
json.dump(flag, open(ROOT / "data" / "faq_regen" / "flagged.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(rows)} câu; {len(flag)} cần xem; lỗi cấm: {sum(1 for r in rows if r['issues'])}")
for r in rows:
    if r["issues"]:
        print("-", r["question"][:70], r["issues"])
