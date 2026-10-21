"""Nạp các cơ sở còn thiếu từ danh_sach_co_so_latest.csv (chạy mỗi lần deploy, không đụng tới tài khoản đã có).

Thực chất gọi reimport_facilities.py ở chế độ mặc định (chỉ thêm cơ sở chưa có). Muốn thay toàn bộ danh sách,
dùng: python reimport_facilities.py --wipe --yes
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reimport_facilities import main  # noqa: E402

if __name__ == "__main__":
    sys.argv = [sys.argv[0]]
    main()
