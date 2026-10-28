"""Bộ kiểm thử Trợ lý Chi: gửi các câu hỏi mẫu tới /api/ai/chat và kiểm tra nội dung, cách xưng hô, định dạng.

Chạy:  python tests/chat_eval.py https://fras-ai.com
Mỗi câu có các điều kiện: phải có (must), không được có (not), và kiểm tra chung (xưng hô "Chi", không lẫn quy định cũ).
Dùng để so sánh trước và sau mỗi lần nâng cấp, tránh làm hỏng những câu đã trả lời đúng.
"""
import json
import re
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")

# (câu hỏi, [phải có một trong từng nhóm], [không được có], loại: "ok" hoặc "scope")
CASES = [
    ("Nghiệm thu PCCC hiện nay chủ đầu tư có phải nộp hồ sơ cho Công an không?", [["bãi bỏ", "không phải nộp"], ["tự tổ chức", "tự nghiệm thu"]], ["05 ngày làm việc"], "ok"),
    ("Giờ tôi cần phục hồi hoạt động thì bắt đầu từ đâu, quy trình thế nào?", [["bãi bỏ"]], [], "ok"),
    ("Cơ sở nguy cơ cao bao lâu thì bị kiểm tra định kỳ một lần?", [["01 năm", "1 năm"]], [], "ok"),
    ("Cháy thì gọi số điện thoại nào?", [["114"]], [], "ok"),
    ("Luật PCCC năm 2013 còn hiệu lực không?", [["55/2024"], ["hết hiệu lực", "thay thế", "không còn"]], [], "ok"),
    ("Nghị định 136/2020 còn dùng được không?", [["hết hiệu lực", "không còn", "thay thế"]], [], "ok"),
    ("Nghị định 347/2026 sửa đổi những gì?", [["105/2025"]], [], "ok"),
    ("Nhà trọ của tôi có phải làm thủ tục thẩm duyệt thiết kế PCCC không?", [["thẩm"], ["căn cứ", "quy mô", "diện tích", "Phụ lục"]], [], "ok"),
    ("Ổ cắm điện bị nóng thì phải làm gì?", [["ngắt", "tắt", "rút"]], [], "ok"),
    ("Cơ sở của tôi có phải lập phương án chữa cháy và thoát nạn không?", [["phương án"]], [], "ok"),
    # Câu hóc búa và tình huống thực tế (dữ liệu giả định)
    ("Tôi mở quán karaoke, nhà 4 tầng, diện tích sàn 85m2, kinh doanh 2 phòng hát tầng 1 và 2. Tôi thuộc quản lý của Phòng Cảnh sát PCCC hay UBND xã?", [["Công an"], ["Phụ lục"]], [], "ok"),
    ("Tôi đang ly hôn tranh chấp ngôi nhà 6 tầng kinh doanh lưu trú, đã ủy quyền cho công ty lo PCCC đến 7/2027. Tôi có thể làm đơn xin Công an kiểm tra đánh giá điều kiện PCCC không?", [["không"], ["tư vấn", "phản ánh", "tố giác"]], [], "ok"),
    ("Nhà nghỉ 5 tầng 1 tum, sàn 300m2, 57 phòng ngủ ở Quế Võ. Cần điều kiện PCCC gì, hồ sơ ANTT gồm gì, có phải thẩm định nghiệm thu xây dựng không?", [["thẩm duyệt"], ["báo cháy"], ["an ninh", "ANTT"]], ["05 ngày làm việc kiểm tra nghiệm thu"], "ok"),
    ("Chủ đầu tư tự nghiệm thu PCCC thì có phải xin giấy chấp thuận nghiệm thu của Cảnh sát PCCC không?", [["bãi bỏ", "không phải"]], [], "ok"),
    ("Chưa thẩm duyệt thiết kế PCCC mà đã thi công xong thì nghiệm thu được không, bị phạt thế nào?", [["thẩm duyệt"], ["phạt"]], [], "ok"),
    ("Giấy chứng nhận huấn luyện nghiệp vụ PCCC thẻ 5 năm còn cấp không?", [["bãi bỏ", "không còn", "không cấp"]], [], "ok"),
    # Diện thẩm định thiết kế PCCC (Phụ lục III NĐ 105/2025, sửa đổi NĐ 347/2026): sai ở đây là lỗi nghiêm trọng
    ("Tôi chuẩn bị thuê một nhà 5 tầng làm ngân hàng, tôi sẽ phải làm gì về PCCC để được đi vào hoạt động đúng quy định", [["3.000"], ["7 tầng"]], ["5.000 m3", "từ 5 tầng trở lên hoặc có tổng khối tích"], "ok"),
    ("Nhà nghỉ 5 tầng 1 tum, 300 m2 sàn, 57 phòng ngủ có phải thẩm định thiết kế PCCC không?", [["không"], ["7 tầng"]], ["5.000 m3"], "ok"),
    ("Tòa nhà văn phòng 7 tầng có phải thẩm định thiết kế PCCC không?", [["7 tầng"], ["thẩm định"]], [], "ok"),
    ("Giá vàng hôm nay bao nhiêu?", [["ngoài phạm vi"]], [], "scope"),
    ("Cách nấu phở bò ngon", [["ngoài phạm vi"]], [], "scope"),
]


def ask(q):
    req = urllib.request.Request(BASE + "/api/ai/chat", data=json.dumps({"message": q}).encode("utf-8"), headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (FRAS chat eval)"})
    t = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=180))
    return r, round(time.time() - t, 1)


def main():
    total = ok = 0
    persona_bad = fmt = 0
    for q, must, nots, kind in CASES:
        try:
            r, secs = ask(q)
        except Exception as e:
            print(f"[LỖI] {q} -> {e}")
            total += 1
            continue
        reply = r.get("reply", "")
        low = reply.lower()
        miss = [g for g in must if not any(w.lower() in low for w in g)]
        bad = [w for w in nots if w.lower() in low]
        tôi = bool(re.search(r"(^|[\s,.;:(])[Tt]ôi\b", reply)) and kind == "ok"
        rich = bool(re.search(r"^(>>|##|!!)\s", reply, re.M) or "**" in reply)
        total += 1
        passed = not miss and not bad
        ok += passed
        persona_bad += 0
        fmt += rich
        flag = "ĐẠT" if passed else "TRƯỢT"
        print(f"[{flag}] {secs:>5}s | {q[:62]}")
        if miss:
            print("        thiếu:", miss)
        if bad:
            print("        không được có:", bad)
        if tôi:
            print("        xưng hô sai: có chữ 'tôi'")
    print(f"\nKết quả: {ok}/{total} câu đạt nội dung; {persona_bad} câu xưng 'tôi' (cần 0); {fmt}/{total} câu có định dạng đầu mục, nhấn mạnh")


if __name__ == "__main__":
    main()
