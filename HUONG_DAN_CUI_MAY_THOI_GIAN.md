# 🕒 Cỗ Máy Thời Gian - Hướng Dẫn Khôi Phục Phiên Bản Cũ

## 1. Cơ chế hoạt động của "Khôi phục phiên bản" (Git Revert)
Khi bạn chạy file `4_KHOI_PHUC_BAN_CU.bat`, hệ thống sẽ **KHÔNG TỰ ĐỘNG XÓA** lịch sử lưu của bạn (điều này giúp tránh mọi rủi ro mất mát dữ liệu).
Thay vào đó, nó tạo ra một **bảo lưu hoàn toàn mới**, tên gọi là thao tác *"Revert"*. Thao tác này sẽ dọn dẹp và mang mọi tệp tin về đúng hình dáng của nó vào thời điểm trước khi phiên bản lỗi xảy ra.

> **Ví dụ điển hình:**
> 1h chiều: Bạn tạo ra Tính năng A (Chạy Tốt).
> 2h chiều: Bạn sửa lỗi Tính năng B, nhưng lỡ tay làm hỏng luôn Tính năng A. Giao diện sập (Lỗi ở bản lúc 2h).
> 3h chiều: Bạn chạy File Số 4. Hệ thống sẽ đem Tính năng A trở lại sống khỏe y như lúc 1h chiều.

## 2. Cách Sử Dụng File Số 4 (`4_KHOI_PHUC_BAN_CU.bat`)

**Bước 1:** Click đúp chạy file số 4.
**Bước 2:** Một màn hình Terminal hiện ra danh sách các lần lưu mã code (Commit) của bạn. Nó trông thế này:
```text
3fa9b2r - Auto save 12/04/2026 10:00 (5 minutes ago)
b78g9aa - Auto save 12/04/2026 09:00 (65 minutes ago)
c61p7q2 - Auto save 11/04/2026 23:00 (12 hours ago)
```
**Bước 3: Đưa ra quyết định**
* TH1: Nếu bạn chỉ vừa mới làm hư code ở ngay lần click `File lưu số 1` gần nhất, **hãy để trống terminal và nhấn ENTER luôn**. Hệ thống lập tức lùi về 1 bước trước đó.
* TH2: Nếu bạn làm hư code ở lúc *09:00* buổi sáng, nhưng mãi 11h trưa bạn mới phát hiện ra, hãy copy đúng dãy 7 chữ cái đứng ở đầu dòng bị lỗi ví dụ: `b78g9aa`. Nhập nó vào terminal và ấn Enter.

**Bước 4: Đồng bộ sự sửa sai lên hệ thống mây**
Sau khi Bước 3 báo **[OK] Thành.Công**. Thì cơ sở mã nguồn tại Đáy Máy Tính của bạn đã được dọn sạch rác để quay về trạng thái tốt. 
Để đẩy sự trong sạch này lên Github và Máy chủ 24/7 Oracle, bạn chỉ cần bấm chạy 2 file như mọi khi:
- `2_UP_CODE_GITHUB.bat` (Để Github nhận bản khôi phục) 
- `3_UP_LEN_ORACLE_FRAS_AI.bat` (Để máy chủ Oracle tải bản được khôi phục về chạy)

## 3. Các Lỗi Khác Có Thể Gặp
**Lỗi "[ERROR] BI XUNG DOT KHI KHOI PHUC"**
Điều này xảy ra khi bạn dùng Cỗ Máy Thời Gian muốn quay về một mốc đã... quá cổ đại (ví dụ lùi tới 50 bước về trước). Mã Cũ và Mã Mới đâm sầm vào nhau vì thay đổi quá lớn. 
-> Đừng hoảng sợ, khi bị xung đột lỗi này, bạn có thể copy đoạn báo lỗi hoặc hỏi tôi (AI) ở phần mềm Chat để tôi gộp xung đột vào chung với nhau cho bạn. File không bị biến mất!
