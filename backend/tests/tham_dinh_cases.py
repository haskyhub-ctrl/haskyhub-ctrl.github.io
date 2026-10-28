"""Bộ kiểm thử bắt buộc cho phần đối chiếu diện thẩm định thiết kế về PCCC (Phụ lục III NĐ 105/2025, sửa đổi NĐ 347/2026).
Chạy: python tests/tham_dinh_cases.py   (phải đạt 100%, mỗi lần sửa bảng ngưỡng hoặc nạp văn bản mới đều chạy lại)
Mỗi ca: (câu hỏi, kết luận đúng, mục Phụ lục III). Kết luận: thuoc | khong_thuoc | can_them_thong_tin.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from utils.tham_dinh import evaluate  # noqa: E402

CASES = [
    # mục 7: khách sạn, nhà nghỉ, bưu điện, trụ sở, nhà làm việc (ngân hàng): 7 tầng hoặc 3.000 m2
    ("Tôi chuẩn bị thuê một nhà 5 tầng làm ngân hàng, tôi sẽ phải làm gì về PCCC để được đi vào hoạt động đúng quy định", "can_them_thong_tin", "7c"),  # 5 tầng chưa đạt 7 tầng; còn phụ thuộc tổng diện tích sàn (từ 3.000 m2)
    ("Nhà 5 tầng tổng diện tích sàn 2.000 m2 làm trụ sở ngân hàng có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "7c"),
    ("Tòa nhà văn phòng 7 tầng có phải thẩm định thiết kế PCCC không?", "thuoc", "7c"),
    ("Tòa nhà làm việc 4 tầng, tổng diện tích sàn 3.200 m2 có phải thẩm định PCCC không?", "thuoc", "7c"),
    ("Nhà nghỉ 5 tầng 1 tum, 300 m2 sàn, 57 phòng ngủ có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "7a"),
    ("Khách sạn 6 tầng tổng diện tích sàn 2.900 m2 có phải thẩm định thiết kế không?", "khong_thuoc", "7a"),
    ("Khách sạn 8 tầng có phải thẩm định thiết kế PCCC không?", "thuoc", "7a"),
    ("Nhà nghỉ 3 tầng diện tích 90 m2 mỗi tầng có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "7a"),
    ("Nhà trọ 4 tầng, tổng diện tích sàn 800 m2, 20 phòng có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "7a"),
    ("Khách sạn có phải thẩm định thiết kế PCCC không?", "can_them_thong_tin", "7a"),
    ("Chi nhánh bưu điện 3 tầng 600 m2 sàn có phải thẩm định PCCC không?", "khong_thuoc", "7b"),
    # mục 1: chung cư
    ("Chung cư mini 6 tầng, tổng diện tích sàn 1.800 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "1"),
    ("Nhà chung cư 7 tầng có phải thẩm định thiết kế PCCC không?", "thuoc", "1"),
    ("Chung cư 5 tầng tổng sàn 3.500 m2 có phải thẩm định thiết kế PCCC không?", "thuoc", "1"),
    # mục 2: giáo dục
    ("Trường mầm non 120 cháu, 2 tầng, tổng diện tích sàn 900 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "2a"),
    ("Trường mầm non 200 cháu có phải thẩm định thiết kế PCCC không?", "thuoc", "2a"),
    ("Trường mầm non 3 tầng diện tích sàn 2.400 m2 có phải thẩm định thiết kế PCCC không?", "thuoc", "2a"),
    ("Trường tiểu học 4 tầng, tổng diện tích sàn 2.500 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "2b"),
    ("Trường THPT 5 tầng có phải thẩm định thiết kế PCCC không?", "thuoc", "2b"),
    # mục 3: y tế
    ("Phòng khám đa khoa 4 tầng, tổng diện tích sàn 1.200 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "3"),
    ("Bệnh viện 5 tầng có phải thẩm định thiết kế PCCC không?", "thuoc", "3"),
    ("Phòng khám tư nhân tổng diện tích sàn 2.100 m2 có phải thẩm định PCCC không?", "thuoc", "3"),
    # mục 5: karaoke, văn hóa
    ("Quán karaoke 3 tầng, mỗi tầng 120 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "5c"),
    ("Karaoke 4 tầng có phải thẩm định thiết kế PCCC không?", "thuoc", "5c"),
    ("Quán karaoke 2 tầng tổng diện tích sàn 1.100 m2 có phải thẩm định thiết kế PCCC không?", "thuoc", "5c"),
    ("Rạp chiếu phim 250 chỗ ngồi có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "5a"),
    ("Rạp chiếu phim 300 chỗ ngồi có phải thẩm định thiết kế PCCC không?", "thuoc", "5a"),
    ("Nhà văn hóa 4 tầng, tổng diện tích sàn 2.000 m2 có phải thẩm định PCCC không?", "khong_thuoc", "5b"),
    # mục 6: thương mại
    ("Siêu thị tổng diện tích sàn 1.800 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "6a"),
    ("Chợ dân sinh 2.500 m2 sàn có phải thẩm định thiết kế PCCC không?", "thuoc", "6a"),
    ("Nhà hàng tiệc cưới 2.500 m2 sàn có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "6b"),
    ("Nhà hàng 3.000 m2 sàn có phải thẩm định thiết kế PCCC không?", "thuoc", "6b"),
    # mục 9, 10: xăng dầu, kho, xưởng
    ("Cửa hàng xăng dầu có 2 cột bơm có phải thẩm định thiết kế PCCC không?", "thuoc", "9a"),
    ("Trạm xăng nhỏ 1 cột bơm có phải thẩm định thiết kế PCCC không?", "thuoc", "9a"),
    ("Nhà kho hàng hạng C diện tích sàn 1.500 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "10"),
    ("Nhà kho hàng hạng C diện tích sàn 2.000 m2 có phải thẩm định thiết kế PCCC không?", "thuoc", "10"),
    ("Nhà kho hàng hạng D diện tích sàn 5.000 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "10"),
    ("Nhà xưởng sản xuất hạng C diện tích sàn 1.200 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "9d"),
    ("Xưởng gỗ hạng C diện tích sàn 2.200 m2 có phải thẩm định thiết kế PCCC không?", "thuoc", "9d"),
    ("Nhà xưởng hạng A sàn 1.000 m2 có phải thẩm định thiết kế PCCC không?", "thuoc", "9d"),
    ("Nhà xưởng hạng D, sàn 9.000 m2 có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "9d"),
    ("Kho chứa hàng hóa có phải thẩm định thiết kế PCCC không?", "can_them_thong_tin", "10"),
    # mục 12, 13
    ("Nhà để xe ô tô kín 1.500 m2 sàn có phải thẩm định thiết kế PCCC không?", "khong_thuoc", "12"),
    ("Nhà để xe kín 2.000 m2 sàn có phải thẩm định thiết kế PCCC không?", "thuoc", "12"),
    ("Bến xe khách tổng diện tích sàn 3.500 m2 có phải thẩm định PCCC không?", "thuoc", "13"),
]


def main():
    bad = 0
    for q, want, rid in CASES:
        r = evaluate(q)
        got = r["verdict"] if r else "khong_nhan_dien"
        gid = r["rule_id"] if r else "-"
        ok = got == want and gid == rid
        bad += not ok
        print(("ĐẠT  " if ok else "SAI  ") + f"{got:<19} mục {gid:<3} (đúng: {want}, mục {rid}) | {q[:80]}")
        if not ok and r:
            print("      facts:", r["facts"], "| why:", r["why"][:120])
    print(f"\n{len(CASES) - bad}/{len(CASES)} ca đạt")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
