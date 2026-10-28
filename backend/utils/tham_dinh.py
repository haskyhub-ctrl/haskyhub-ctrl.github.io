"""Đối chiếu tự động công trình có thuộc diện thẩm định thiết kế về PCCC hay không, theo Phụ lục III Nghị định 105/2025/NĐ-CP
(sửa đổi, bổ sung bởi Nghị định 347/2026/NĐ-CP). Bảng ngưỡng dưới đây chép nguyên từ Phụ lục III trong kho (kho_seed/a2c5fea83664.txt).

Mục đích: kết luận về diện thẩm định phải chính xác tuyệt đối nên KHÔNG để AI tự suy ra. Hàm evaluate() cho kết luận chắc chắn
từ loại hình, số tầng, tổng diện tích sàn nêu trong câu hỏi; câu trả lời của AI được kiểm tra lại bằng check_reply().
"""
import re

# Mỗi mục: id, nhãn, regex nhận diện loại hình, các điều kiện (HOẶC): tầng tối thiểu, diện tích sàn tối thiểu, khối tích tối thiểu, chỗ ngồi/cháu tối thiểu
RULES = [
    {"id": "9a", "label": "Cửa hàng xăng dầu, trạm cấp xăng dầu nội bộ, kho xăng dầu, kho/trạm chiết khí hóa lỏng, trạm phân phối khí", "always": True,
     "text": "Mục 9 điểm a Phụ lục III: cửa hàng xăng dầu, trạm cấp xăng dầu nội bộ có từ 01 cột bơm trở lên; kho chứa dầu mỏ, kho chứa khí hóa lỏng, trạm chiết khí hóa lỏng, trạm phân phối khí... đều thuộc diện thẩm định, không phân biệt quy mô",
     "re": r"(cửa hàng xăng dầu|trạm xăng|cây xăng|trạm cấp xăng dầu|kho xăng|kho dầu|kho chứa dầu|kho chứa khí|kho gas|trạm chiết (khí|gas)|trạm phân phối khí)"},
    {"id": "9c", "label": "Nhà máy, kho vật liệu nổ, tiền chất thuốc nổ, vũ khí", "always": True,
     "text": "Mục 9 điểm c Phụ lục III: nhà máy sản xuất, kho cố định chứa vật liệu nổ, tiền chất thuốc nổ công nghiệp, vũ khí, công cụ hỗ trợ thuộc diện thẩm định",
     "re": r"(vật liệu nổ|tiền chất thuốc nổ|kho (chứa )?(thuốc nổ|vũ khí))"},
    {"id": "1", "label": "Nhà chung cư, nhà ở tập thể", "floors": 7, "area": 3000,
     "text": "Mục 1 Phụ lục III: nhà chung cư, nhà ở tập thể cao từ 7 tầng trở lên hoặc có tổng diện tích sàn từ 3.000 m2 trở lên",
     "re": r"(chung cư|nhà ở tập thể|ký túc|khu tập thể)"},
    {"id": "2a", "label": "Nhà trẻ, trường mầm non, trường mẫu giáo", "area": 2000, "people": 150, "people_unit": "cháu",
     "text": "Mục 2 Phụ lục III: nhà trẻ, trường mầm non, trường mẫu giáo có từ 150 cháu trở lên hoặc có tổng diện tích sàn từ 2.000 m2 trở lên",
     "re": r"(nhà trẻ|mầm non|mẫu giáo|nhóm trẻ|lớp mẫu giáo)"},
    {"id": "2b", "label": "Trường học các cấp, trường đại học, cao đẳng, trung tâm đào tạo, cơ sở nghiên cứu", "floors": 5, "area": 3000,
     "text": "Mục 2 Phụ lục III: trường tiểu học, THCS, THPT, đại học, cao đẳng, trường dạy nghề, trung tâm đào tạo khác, cơ sở nghiên cứu cao từ 5 tầng trở lên hoặc có tổng diện tích sàn từ 3.000 m2 trở lên",
     "re": r"(trường (tiểu học|trung học|thcs|thpt|phổ thông|đại học|cao đẳng|dạy nghề|học)|trung tâm đào tạo|trung tâm dạy|cơ sở nghiên cứu|trường học)"},
    {"id": "3", "label": "Công trình y tế (bệnh viện, phòng khám, trạm y tế, nhà hộ sinh, dưỡng lão...)", "floors": 5, "area": 2000,
     "text": "Mục 3 Phụ lục III: bệnh viện, phòng khám, trạm y tế, nhà hộ sinh, cơ sở điều dưỡng, phục hồi chức năng, dưỡng lão... cao từ 5 tầng trở lên hoặc có tổng diện tích sàn từ 2.000 m2 trở lên",
     "re": r"(bệnh viện|phòng khám|trạm y tế|nhà hộ sinh|dưỡng lão|điều dưỡng|phục hồi chức năng|cơ sở y tế|nhà thuốc|bệnh xá)"},
    {"id": "4", "label": "Công trình thể thao", "area": 5000, "people": 5000, "people_unit": "chỗ ngồi",
     "text": "Mục 4 Phụ lục III: sân vận động có khán đài từ 5.000 chỗ ngồi trở lên; nhà thi đấu, nhà tập luyện thể thao có khán đài từ 5.000 chỗ ngồi trở lên hoặc tổng diện tích sàn từ 5.000 m2 trở lên",
     "re": r"(sân vận động|nhà thi đấu|nhà tập luyện|phòng tập gym|trung tâm thể thao|công trình thể thao|sân thể thao)"},
    {"id": "5c", "label": "Công trình vui chơi, giải trí, vũ trường, karaoke và công trình văn hóa khác", "floors": 4, "area": 1000,
     "text": "Mục 5 Phụ lục III: công trình vui chơi, giải trí, vũ trường, karaoke, các công trình văn hóa khác cao từ 4 tầng trở lên hoặc có tổng diện tích sàn từ 1.000 m2 trở lên",
     "re": r"(karaoke|vũ trường|quán bar|bar |club|vui chơi|giải trí|khu trò chơi|massage|xông hơi|spa)"},
    {"id": "5a", "label": "Nhà hát, rạp chiếu phim, rạp xiếc", "people": 300, "people_unit": "chỗ ngồi",
     "text": "Mục 5 Phụ lục III: nhà hát, rạp chiếu phim, rạp xiếc có từ 300 chỗ ngồi trở lên",
     "re": r"(nhà hát|rạp chiếu phim|rạp xiếc|rạp phim)"},
    {"id": "5b", "label": "Trung tâm hội nghị, nhà văn hóa, bảo tàng, thư viện, nhà triển lãm, nhà trưng bày", "floors": 5, "area": 3000,
     "text": "Mục 5 Phụ lục III: trung tâm hội nghị, nhà văn hóa, bảo tàng, thư viện, nhà triển lãm, nhà trưng bày cao từ 5 tầng trở lên hoặc có tổng diện tích sàn từ 3.000 m2 trở lên",
     "re": r"(hội nghị|nhà văn hóa|bảo tàng|thư viện|nhà triển lãm|nhà trưng bày|hội trường)"},
    {"id": "6a", "label": "Trung tâm thương mại, siêu thị, chợ, cửa hàng kinh doanh hàng hóa dễ cháy", "area": 2000,
     "text": "Mục 6 Phụ lục III: trung tâm thương mại, siêu thị, chợ, cửa hàng kinh doanh hàng hóa dễ cháy có tổng diện tích sàn từ 2.000 m2 trở lên",
     "re": r"(trung tâm thương mại|siêu thị|chợ|cửa hàng (kinh doanh )?hàng (hóa )?dễ cháy|tttm)"},
    {"id": "6b", "label": "Nhà hàng, cửa hàng ăn uống", "area": 3000,
     "text": "Mục 6 Phụ lục III: nhà hàng, cửa hàng ăn uống có tổng diện tích sàn từ 3.000 m2 trở lên",
     "re": r"(nhà hàng|quán ăn|cửa hàng ăn uống|quán cà phê|quán cafe|quán cơm|tiệm ăn|quán nhậu|trung tâm tiệc cưới)"},
    {"id": "7a", "label": "Khách sạn, nhà khách, nhà nghỉ, cơ sở dịch vụ lưu trú khác (kể cả nhà trọ kinh doanh lưu trú)", "floors": 7, "area": 3000,
     "text": "Mục 7 điểm a Phụ lục III: công trình cao từ 7 tầng trở lên hoặc có tổng diện tích sàn từ 3.000 m2 trở lên gồm khách sạn, nhà khách, nhà nghỉ và các cơ sở dịch vụ lưu trú khác",
     "re": r"(khách sạn|nhà khách|nhà nghỉ|nhà trọ|phòng trọ|homestay|lưu trú|resort|căn hộ dịch vụ|motel)"},
    {"id": "7b", "label": "Bưu điện, bưu cục, cơ sở bưu chính, viễn thông", "floors": 7, "area": 3000,
     "text": "Mục 7 điểm b Phụ lục III: công trình cao từ 7 tầng trở lên hoặc có tổng diện tích sàn từ 3.000 m2 trở lên gồm bưu điện, bưu cục, cơ sở cung cấp dịch vụ bưu chính, viễn thông khác",
     "re": r"(bưu điện|bưu cục|bưu chính|viễn thông)"},
    {"id": "7c", "label": "Tòa nhà làm trụ sở, nhà làm việc (văn phòng, ngân hàng, công sở...)", "floors": 7, "area": 3000,
     "text": "Mục 7 điểm c Phụ lục III: công trình cao từ 7 tầng trở lên hoặc có tổng diện tích sàn từ 3.000 m2 trở lên gồm tòa nhà sử dụng làm trụ sở, nhà làm việc",
     "re": r"(ngân hàng|trụ sở|nhà làm việc|văn phòng|tòa nhà văn phòng|công sở|cao ốc văn phòng|chi nhánh|phòng giao dịch|công ty|ủy ban)"},
    {"id": "10", "label": "Nhà kho chứa hàng hóa hạng A, B, C", "area": 2000, "volume": 15000, "needs_hang": True,
     "text": "Mục 10 Phụ lục III: nhà kho chứa hàng hóa có hạng nguy hiểm cháy và cháy nổ A, B, C có khối tích từ 15.000 m3 trở lên hoặc tổng diện tích sàn từ 2.000 m2 trở lên (kho hạng D, E không thuộc diện này)",
     "re": r"(nhà kho|kho hàng|kho chứa|kho bãi|kho lạnh|kho vật tư)"},
    {"id": "9d", "label": "Công trình sản xuất công nghiệp (nhà xưởng, nhà máy)", "needs_hang": True,
     "text": "Mục 9 điểm d Phụ lục III: nhà phục vụ sản xuất hạng A, B có khối tích từ 7.000 m3 trở lên hoặc tổng diện tích sàn từ 1.000 m2 trở lên; hạng C từ 15.000 m3 hoặc 2.000 m2; hạng D, E từ 30.000 m3 hoặc 10.000 m2",
     "re": r"(nhà xưởng|xưởng|nhà máy|công trình sản xuất|cơ sở sản xuất|dây chuyền sản xuất|khu công nghiệp)",
     "hang_rules": {"AB": {"area": 1000, "volume": 7000}, "C": {"area": 2000, "volume": 15000}, "DE": {"area": 10000, "volume": 30000}}},
    {"id": "12", "label": "Nhà để xe ô tô, xe máy, nhà trưng bày ô tô, xe máy dạng kín", "area": 2000,
     "text": "Mục 12 Phụ lục III: nhà để xe ô tô, xe máy, nhà trưng bày ô tô, xe máy dạng kín có tổng diện tích sàn từ 2.000 m2 trở lên",
     "re": r"(nhà để xe|bãi đỗ xe|gara|ga ra|nhà trưng bày (ô tô|xe)|showroom|hầm để xe)"},
    {"id": "13", "label": "Công trình giao thông (nhà ga, bến xe, trạm dừng nghỉ, nhà sửa chữa phương tiện...)", "area": 3000,
     "text": "Mục 13 Phụ lục III: bến xe khách, trung tâm đăng kiểm, trạm dừng nghỉ, nhà sửa chữa, bảo dưỡng phương tiện giao thông cơ giới... có tổng diện tích sàn từ 3.000 m2 trở lên; nhà ga hành khách, nhà ga hàng hóa... từ 3.000 m2",
     "re": r"(bến xe|nhà ga|trung tâm đăng kiểm|trạm dừng nghỉ|xưởng sửa chữa (ô tô|xe)|garage sửa)"},
]

_NUM = r"(\d{1,3}(?:[.,]\d{3})+|\d+(?:[.,]\d+)?)"


def _to_num(s: str) -> float:
    s = s.strip()
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        return float(re.sub(r"[.,]", "", s))
    return float(s.replace(",", "."))


def extract_facts(q: str) -> dict:
    """Lấy số tầng, tổng diện tích sàn, khối tích, hạng nguy hiểm cháy nổ, số chỗ ngồi/số cháu từ câu hỏi."""
    t = q.lower()
    f = {"floors": None, "area": None, "volume": None, "hang": None, "people": None}
    floors = [int(m.group(1)) for m in re.finditer(r"(\d{1,2})\s*(?:tầng|lầu)(?!\s*hầm)", t)]
    if not floors:
        w = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, "mười": 10}
        m = re.search(r"\b(một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s+tầng", t)
        if m:
            floors = [w[m.group(1)]]
    if floors:
        f["floors"] = max(floors)
    m_total = re.search(r"tổng\s+(?:diện tích\s+)?(?:sàn|xây dựng|diện tích)\s*(?:là|khoảng|:)?\s*" + _NUM + r"\s*(?:m2|m²|mét vuông|m vuông)", t)
    m_each = re.search(r"(?:mỗi|một|/)\s*(?:tầng|sàn)\s*(?:có\s*)?(?:diện tích\s*)?(?:sàn\s*)?(?:khoảng|là|:)?\s*" + _NUM + r"\s*(?:m2|m²|mét vuông|m vuông)", t) or \
        re.search(r"(?:diện tích\s*)?(?:mỗi|từng)\s*(?:tầng|sàn)\s*(?:khoảng|là|:)?\s*" + _NUM + r"\s*(?:m2|m²|mét vuông|m vuông)", t)
    m_any = re.search(_NUM + r"\s*(?:m2|m²|mét vuông|m vuông)", t)
    if m_total:
        f["area"] = _to_num(m_total.group(1))
    elif m_each and f["floors"]:
        f["area"] = _to_num(m_each.group(1)) * f["floors"]
    elif m_any:
        v = _to_num(m_any.group(1))
        f["area"] = v   # diện tích nêu chung được coi là tổng diện tích sàn
        f["area_ambiguous"] = bool(f["floors"] and re.search(r"(diện tích|sàn)\s*(?:mỗi|1)?\s*tầng", t))
    m_vol = re.search(_NUM + r"\s*(?:m3|m³|mét khối)", t)
    if m_vol:
        f["volume"] = _to_num(m_vol.group(1))
    m_h = re.search(r"hạng\s*(?:nguy hiểm cháy[^a-z0-9]{0,15})?([abcde])(?![a-zà-ỹ])", t)
    if m_h:
        f["hang"] = m_h.group(1).upper()
    m_p = re.search(_NUM + r"\s*(?:cháu|chỗ ngồi|chỗ|học sinh|ghế)", t)
    if m_p:
        f["people"] = _to_num(m_p.group(1))
    return f


def _match_rule(q: str):
    t = q.lower()
    hits = [r for r in RULES if re.search(r["re"], t)]
    if not hits:
        return None, []
    # Ưu tiên theo thứ tự trong RULES (mục đặc thù như xăng dầu, karaoke trước mục chung như trụ sở)
    return hits[0], hits


def evaluate(question: str):
    """Trả None nếu không nhận diện được loại công trình. Ngược lại trả dict: verdict thuoc | khong_thuoc | can_them_thong_tin."""
    rule, hits = _match_rule(question)
    if not rule:
        return None
    f = extract_facts(question)
    t = question.lower()
    mixed = len({h["id"][0] for h in hits}) > 1 or bool(re.search(r"(kết hợp|hỗn hợp|đa năng|vừa ở vừa|tầng 1[^.]{0,30}kinh doanh|ở từ tầng)", t))
    res = {"rule_id": rule["id"], "label": rule["label"], "rule_text": rule["text"], "facts": f, "mixed": mixed, "other_rules": [h["id"] for h in hits[1:]]}
    if rule.get("always"):
        res.update(verdict="thuoc", why="Loại công trình này thuộc diện thẩm định thiết kế không phụ thuộc quy mô.")
        return res
    thr = dict(rule)
    if rule["id"] == "9d" or rule["id"] == "10":
        hang = f["hang"]
        if rule["id"] == "10":
            if hang in ("D", "E"):
                res.update(verdict="khong_thuoc", why="Nhà kho hạng D, E không thuộc mục 10 Phụ lục III.")
                return res
            if hang is None:
                res.update(verdict="can_them_thong_tin", missing=["hạng nguy hiểm cháy nổ của hàng hóa trong kho (A, B, C hay D, E)", "tổng diện tích sàn hoặc khối tích"],
                           why="Kho chỉ thuộc diện thẩm định khi chứa hàng hạng A, B, C và đạt ngưỡng từ 2.000 m2 sàn hoặc 15.000 m3.")
                return res
        else:
            if hang is None:
                res.update(verdict="can_them_thong_tin", missing=["hạng nguy hiểm cháy nổ của nhà sản xuất (A, B, C, D hay E)", "tổng diện tích sàn hoặc khối tích"],
                           why="Ngưỡng thẩm định phụ thuộc hạng: A, B từ 1.000 m2 hoặc 7.000 m3; C từ 2.000 m2 hoặc 15.000 m3; D, E từ 10.000 m2 hoặc 30.000 m3.")
                return res
            key = "AB" if hang in ("A", "B") else ("C" if hang == "C" else "DE")
            thr.update(rule["hang_rules"][key])
    reasons, ok_known = [], True
    passed = False
    if thr.get("floors"):
        if f["floors"] is None:
            ok_known = False
        elif f["floors"] >= thr["floors"]:
            passed = True; reasons.append(f"cao {int(f['floors'])} tầng, đạt ngưỡng từ {thr['floors']} tầng")
        else:
            reasons.append(f"cao {int(f['floors'])} tầng, dưới ngưỡng {thr['floors']} tầng")
    if thr.get("area"):
        if f["area"] is None:
            ok_known = False
        elif f["area"] >= thr["area"]:
            passed = True; reasons.append(f"tổng diện tích sàn khoảng {f['area']:,.0f} m2, đạt ngưỡng từ {thr['area']:,} m2".replace(",", "."))
        else:
            reasons.append(f"tổng diện tích sàn khoảng {f['area']:,.0f} m2, dưới ngưỡng {thr['area']:,} m2".replace(",", "."))
    if thr.get("volume") and f["volume"] is not None:
        if f["volume"] >= thr["volume"]:
            passed = True; reasons.append(f"khối tích {f['volume']:,.0f} m3, đạt ngưỡng từ {thr['volume']:,} m3".replace(",", "."))
        else:
            reasons.append(f"khối tích {f['volume']:,.0f} m3, dưới ngưỡng {thr['volume']:,} m3".replace(",", "."))
    if thr.get("people") and f["people"] is not None:
        if f["people"] >= thr["people"]:
            passed = True; reasons.append(f"{f['people']:,.0f} {thr.get('people_unit', 'người')}, đạt ngưỡng từ {thr['people']:,}".replace(",", "."))
        else:
            reasons.append(f"{f['people']:,.0f} {thr.get('people_unit', 'người')}, dưới ngưỡng {thr['people']:,}".replace(",", "."))
    if passed:
        res.update(verdict="thuoc", why="; ".join(reasons))
    elif ok_known:
        res.update(verdict="khong_thuoc", why="; ".join(reasons) + ". Các điều kiện trong mục này là HOẶC nên chỉ cần đạt một điều kiện là thuộc diện, hiện chưa điều kiện nào đạt.")
    else:
        miss = []
        if thr.get("floors") and f["floors"] is None:
            miss.append("số tầng")
        if thr.get("area") and f["area"] is None:
            miss.append("tổng diện tích sàn")
        res.update(verdict="can_them_thong_tin", missing=miss, why="; ".join(reasons) if reasons else "Chưa đủ số liệu quy mô để kết luận.")
    if mixed and res["verdict"] == "khong_thuoc":
        res["note"] = "Công trình có nhiều công năng: phải xét thêm từng công năng (mục 8 Phụ lục III); nhà ở riêng lẻ có kết hợp sản xuất, kinh doanh không bị coi là công trình hỗn hợp theo mục 8."
    if f.get("area_ambiguous"):
        res["note"] = (res.get("note", "") + " Diện tích nêu có thể là diện tích mỗi tầng; cần nhân với số tầng để ra tổng diện tích sàn.").strip()
    return res


def facts_block(question: str) -> str:
    """Đoạn chèn vào câu lệnh cho AI: kết quả đối chiếu bắt buộc tuân thủ. Trả '' nếu không áp dụng."""
    r = evaluate(question)
    if not r:
        return ""
    v = {"thuoc": "THUỘC diện thẩm định thiết kế về PCCC", "khong_thuoc": "KHÔNG thuộc diện thẩm định thiết kế về PCCC",
         "can_them_thong_tin": "CHƯA ĐỦ SỐ LIỆU để kết luận (phải trả lời theo từng trường hợp và hỏi lại bằng khối '?? ')"}[r["verdict"]]
    lines = [
        "KẾT QUẢ ĐỐI CHIẾU TỰ ĐỘNG VỚI PHỤ LỤC III NGHỊ ĐỊNH 105/2025/NĐ-CP (sửa đổi bởi NĐ 347/2026/NĐ-CP), ĐÃ KIỂM CHỨNG, BẮT BUỘC TUÂN THỦ, TUYỆT ĐỐI KHÔNG ĐƯỢC TRÁI:",
        f"- Loại hình nhận diện: {r['label']}",
        f"- Quy định: {r['rule_text']}",
        f"- Kết luận: {v}.",
        f"- Lý do: {r['why']}",
    ]
    if r.get("missing"):
        lines.append("- Cần hỏi lại: " + "; ".join(r["missing"]))
    if r.get("note"):
        lines.append("- Lưu ý: " + r["note"])
    if r.get("other_rules"):
        lines.append("- Câu hỏi còn có thể liên quan các mục khác của Phụ lục III: " + ", ".join(r["other_rules"]) + " (xét riêng từng công năng).")
    lines.append("- Dòng kết luận đầu tiên (>>) phải nêu đúng kết luận trên. Không dùng ngưỡng cũ (khối tích 5.000 m3, 5 tầng cho nhà nghỉ...). Thẩm định thiết kế là thủ tục khi thiết kế, cải tạo, thay đổi công năng; khác với việc cơ sở thuộc diện quản lý về PCCC (Phụ lục I) hay cơ sở nguy hiểm cháy nổ nhóm 1, nhóm 2 (Phụ lục II).")
    return "\n".join(lines)


_POS = re.compile(r"(phải|bắt buộc|thuộc diện|cần)[^.\n]{0,50}thẩm\s*(định|duyệt)", re.I)
_NEG = re.compile(r"(không|chưa|miễn)[^.\n]{0,40}(phải|thuộc diện|bắt buộc|cần)?[^.\n]{0,30}thẩm\s*(định|duyệt)|thẩm\s*(định|duyệt)[^.\n]{0,30}(không (phải|bắt buộc|thuộc)|chưa (phải|thuộc))", re.I)
_OLD = re.compile(r"((?<![\d.])5\.000\s*m3|(?<![\d.])5\.000\s*m³|(?<![\d.])1\.500\s*m3|khối tích từ 1\.500)", re.I)


def check_reply(question: str, reply: str) -> dict:
    """Kiểm tra câu trả lời có mâu thuẫn với kết quả đối chiếu Phụ lục III không. Trả {'ok': bool, 'problem': str}."""
    r = evaluate(question)
    if not r or r["verdict"] == "can_them_thong_tin":
        return {"ok": True, "problem": ""}
    head = reply[:700]
    first = re.sub(r"\s+", " ", head)
    pos, neg = bool(_POS.search(first)), bool(_NEG.search(first))
    if r["verdict"] == "khong_thuoc" and pos and not neg:
        return {"ok": False, "problem": "Câu trả lời khẳng định phải thẩm định nhưng đối chiếu Phụ lục III cho thấy KHÔNG thuộc diện: " + r["why"]}
    if r["verdict"] == "thuoc" and neg and not pos:
        return {"ok": False, "problem": "Câu trả lời khẳng định không phải thẩm định nhưng đối chiếu Phụ lục III cho thấy THUỘC diện: " + r["why"]}
    if _OLD.search(reply) and re.search(r"thẩm\s*(định|duyệt)", reply):
        return {"ok": False, "problem": "Câu trả lời dùng ngưỡng cũ (khối tích 5.000 m3 hoặc 1.500 m3) không còn trong Phụ lục III hiện hành."}
    return {"ok": True, "problem": ""}
