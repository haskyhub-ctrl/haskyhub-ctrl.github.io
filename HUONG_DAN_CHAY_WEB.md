# 🔥 HƯỚNG DẪN CHẠY WEB FRAS - Từ A đến Z

## 📋 BẠN ĐÃ CÓ GÌ?

| Thành phần | Trạng thái | Giải thích |
|------------|-----------|------------|
| ✅ **Backend (FastAPI)** | Đã có | File `backend/main.py` - server xử lý logic |
| ✅ **Frontend (HTML/JS/CSS)** | Đã có | Thư mục `frontend/` - giao diện web |
| ✅ **PostgreSQL** | Đã cài | Phần mềm database trên máy bạn |
| ✅ **Cấu hình kết nối DB** | Đã có | File `backend/.env` |
| ⚠️ **Database "fras"** | Chưa tạo | Cần tạo database tên "fras" trong PostgreSQL |
| ⚠️ **Python packages** | Chưa cài | Cần chạy `pip install` |
| ⚠️ **Tunnel** | Chưa cài | Cần cài ngrok hoặc cloudflared |

---

## 🧠 HIỂU ĐƠN GIẢN: WEB CẦN GÌ ĐỂ CHẠY?

Một trang web cần **3 thứ** chạy cùng lúc:

```
1. DATABASE (PostgreSQL)     → Kho lưu trữ dữ liệu (câu hỏi, user, kết quả...)
2. BACKEND (FastAPI/Python)  → Bộ não xử lý (đăng nhập, tính điểm, lưu dữ liệu...)
3. FRONTEND (HTML/JS)        → Giao diện người dùng nhìn thấy

Khi người dùng mở web:
   Người dùng → [Tunnel] → Frontend → Backend → Database
```

### Tunnel là gì?
- Tunnel = "đường hầm" kết nối máy bạn ra internet
- Không cần tunnel → chỉ bạn truy cập được (localhost)
- Có tunnel → ai cũng truy cập được qua link công khai

### Có cần hosting không?
- **KHÔNG CẦN** nếu dùng tunnel
- Hosting = thuê máy chủ chạy 24/7 trên internet
- Tunnel = dùng chính máy bạn làm server (miễn phí, nhưng máy phải bật)

---

## 🚀 HƯỚNG DẪN TỪNG BƯỚC

### BƯỚC 1: Tạo database PostgreSQL

Mở **Command Prompt** (cmd) hoặc **pgAdmin**, chạy:

```cmd
psql -U postgres
```

Nhập password PostgreSQL của bạn (password: `Unikitaoo1` theo file .env).

Sau khi vào được PostgreSQL, chạy:

```sql
CREATE DATABASE fras;
```

Nếu thành công sẽ thấy: `CREATE DATABASE`

Gõ `\q` để thoát.

> **Nếu lỗi "psql không nhận":** Cần thêm PostgreSQL vào PATH.
> Mở cmd chạy: `set PATH=%PATH%;C:\Program Files\PostgreSQL\16\bin` (thay 16 bằng version bạn cài)
> Hoặc dùng **pgAdmin** (giao diện đồ họa) để tạo database.

---

### BƯỚC 2: Cài đặt Python packages

Mở **cmd** tại thư mục project, chạy:

```cmd
cd backend
pip install -r requirements.txt
```

Đợi cài xong (khoảng 1-2 phút).

---

### BƯỚC 3: Chạy Backend Server

Vẫn trong thư mục `backend`, chạy:

```cmd
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Nếu thành công, bạn sẽ thấy:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
🔥 Seeding database with initial data...
✅ Seeded xxx questions...
✅ Admin account: admin@fras.vn / admin123
```

> **Lúc này web đã chạy!** Mở trình duyệt vào `http://localhost:8000` để xem.

---

### BƯỚC 4: Tạo Tunnel (để người khác truy cập)

#### Cách 1: Dùng ngrok (đơn giản nhất)

1. Tải ngrok: https://ngrok.com/download
2. Đăng ký tài khoản miễn phí tại https://ngrok.com
3. Lấy authtoken từ dashboard
4. Mở **cmd mới** (giữ cmd backend đang chạy), chạy:

```cmd
ngrok config add-authtoken YOUR_TOKEN_HERE
ngrok http 8000
```

5. Bạn sẽ nhận được URL như: `https://abc123.ngrok-free.app`
6. Gửi URL này cho người khác → họ truy cập được web của bạn!

#### Cách 2: Dùng Cloudflare Tunnel (ổn định hơn, miễn phí)

1. Tải cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
2. Mở **cmd mới**, chạy:

```cmd
cloudflared tunnel --url http://localhost:8000
```

3. Bạn sẽ nhận được URL như: `https://xxx.trycloudflare.com`

---

## 📊 TÓM TẮT: CẦN MỞ BAO NHIÊU CỬA SỔ CMD?

```
CMD 1: PostgreSQL (tự chạy nền, không cần mở)
CMD 2: uvicorn main:app --host 0.0.0.0 --port 8000 --reload  (Backend)
CMD 3: ngrok http 8000  (Tunnel - nếu muốn người khác truy cập)
```

---

## ❓ CÂU HỎI THƯỜNG GẶP

### Q: Máy tắt thì web có chạy không?
**A:** Không. Khi máy tắt, web ngừng hoạt động. Muốn web chạy 24/7 thì cần hosting.

### Q: URL ngrok thay đổi mỗi lần restart?
**A:** Đúng (bản miễn phí). Bản trả phí ($8/tháng) có URL cố định.

### Q: Cloudflare tunnel có URL cố định không?
**A:** Bản quick tunnel (lệnh trên) thì URL thay đổi. Muốn cố định cần cấu hình thêm (miễn phí nhưng phức tạp hơn).

### Q: Tôi có cần biết PostgreSQL không?
**A:** Không cần. Backend tự tạo bảng và seed dữ liệu khi khởi động. Bạn chỉ cần tạo database trống tên "fras".

### Q: Nếu muốn dùng hosting thay vì tunnel?
**A:** Project đã có file `render.yaml` để deploy lên Render.com (miễn phí). Nhưng cần tạo tài khoản và cấu hình thêm.

---

## 🔧 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "psql: command not found"
→ PostgreSQL chưa được thêm vào PATH. Dùng pgAdmin hoặc thêm PATH thủ công.

### Lỗi: "FATAL: password authentication failed"
→ Sai password PostgreSQL. Kiểm tra lại password trong file `backend/.env`.

### Lỗi: "database 'fras' does not exist"
→ Chưa tạo database. Quay lại Bước 1.

### Lỗi: "ModuleNotFoundError: No module named 'xxx'"
→ Chưa cài packages. Quay lại Bước 2.

### Lỗi: "Address already in use"
→ Port 8000 đang bị dùng. Đổi port: `uvicorn main:app --host 0.0.0.0 --port 8001`

---

## 🎯 CHECKLIST NHANH

- [ ] PostgreSQL đang chạy (kiểm tra trong Services)
- [ ] Database "fras" đã được tạo
- [ ] `pip install -r requirements.txt` đã chạy xong
- [ ] `uvicorn main:app --host 0.0.0.0 --port 8000` đang chạy
- [ ] Mở `http://localhost:8000` thấy trang web
- [ ] (Tùy chọn) ngrok/cloudflared đang chạy để chia sẻ link
