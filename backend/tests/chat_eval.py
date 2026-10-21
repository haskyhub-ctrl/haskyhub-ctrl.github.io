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

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")

# (câu hỏi, [phải có một trong từng nhóm], [không được có], loại: "ok" hoặc "scope")
CASES = [
    ("Nghiệm thu PCCC hiện nay chủ đầu tư có phải nộp hồ sơ cho Công an không?", [["bãi bỏ", "không phải nộp"], ["tự tổ chức", "tự nghiệm thu"]], ["05 ngày làm việc"], "ok"),
    ("Giờ tôi cần phục hồi hoạt động thì bắt đầu từ đâu, quy trình thế nào?", [["bãi bỏ"]], ["05 ngày làm việc", "đơn đề nghị phục hồi"], "ok"),
    ("Cơ sở nguy cơ cao bao lâu thì bị kiểm tra định kỳ một lần?", [["01 năm", "1 năm"]], [], "ok"),
    ("Cháy thì gọi số điện thoại nào?", [["114"]], [], "ok"),
    ("Luật PCCC năm 2013 còn hiệu lực không?", [["55/2024"], ["hết hiệu lực", "thay thế", "không còn"]], [], "ok"),
    ("Nghị định 136/2020 còn dùng được không?", [["hết hiệu lực", "không còn", "thay thế"]], [], "ok"),
    ("Nghị định 347/2026 sửa đổi những gì?", [["105/2025"]], [], "ok"),
    ("Nhà trọ của tôi có phải làm thủ tục thẩm duyệt thiết kế PCCC không?", [["thẩm"], ["căn cứ", "quy mô", "diện tích", "Phụ lục"]], [], "ok"),
    ("Ổ cắm điện bị nóng thì phải làm gì?", [["ngắt", "tắt", "rút"]], [], "ok"),
    ("Cơ sở của tôi có phải lập phương án chữa cháy và thoát nạn không?", [["phương án"]], [], "ok"),
    ("Giá vàng hôm nay bao nhiêu?", [["ngoài lĩnh vực"]], [], "scope"),
    ("Cách nấu phở bò ngon", [["ngoài lĩnh vực"]], [], "scope"),
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
        persona_bad += tôi
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
