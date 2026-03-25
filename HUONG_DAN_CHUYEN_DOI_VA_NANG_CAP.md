# 🔄 HƯỚNG DẪN: Gỡ Tunnel → Dùng VPS Oracle → Quy Trình Nâng Cấp Web

---

## 📑 MỤC LỤC

1. [PHẦN 1: Gỡ bỏ Cloudflare Tunnel](#phần-1-gỡ-bỏ-cloudflare-tunnel)
2. [PHẦN 2: Sử dụng VPS Oracle Cloud](#phần-2-sử-dụng-vps-oracle-cloud)
3. [PHẦN 3: Trỏ tên miền Hostinger về Oracle Cloud](#phần-3-trỏ-tên-miền-hostinger-về-oracle-cloud)
4. [PHẦN 4: Quy trình nâng cấp web](#phần-4-quy-trình-nâng-cấp-web)

---

## PHẦN 1: Gỡ bỏ Cloudflare Tunnel

### 🧠 Hiểu vấn đề

Hiện tại kiến trúc của bạn đang là:

```
❌ KIẾN TRÚC CŨ (Tunnel):
   Người dùng → Tên miền (Hostinger) → Cloudflare Tunnel → Máy tính cá nhân (port 8000)
   → Phải bật máy 24/7, tunnel có thể đứt bất cứ lúc nào
```

Sau khi chuyển sang Oracle Cloud:

```
✅ KIẾN TRÚC MỚI (VPS):
   Người dùng → Tên miền (Hostinger DNS) → Oracle Cloud VPS (Nginx → FastAPI)
   → Chạy 24/7 miễn phí, ổn định, không cần bật máy cá nhân
```

### 📋 Các bước gỡ Tunnel

#### Bước 1.1: Tắt Cloudflare Tunnel trên máy cá nhân

Nếu bạn đang chạy `cloudflared` trên máy tính:

```cmd
:: Kiểm tra cloudflared có đang chạy không
tasklist | findstr cloudflared

:: Tắt process cloudflared
taskkill /IM cloudflared.exe /F
```

Nếu bạn đã cài cloudflared như Windows Service:

```cmd
:: Gỡ service cloudflared
cloudflared service uninstall

:: Hoặc dừng service
sc stop cloudflared
sc delete cloudflared
```

#### Bước 1.2: Xóa Tunnel trên Cloudflare Dashboard (nếu dùng Cloudflare)

> ⚠️ **Chỉ làm bước này nếu bạn đang dùng Cloudflare làm DNS proxy cho tên miền Hostinger.**

1. Đăng nhập [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Vào **Networks** → **Tunnels**
3. Tìm tunnel đang dùng → nhấn **⋮** (3 chấm) → **Delete**
4. Xác nhận xóa

#### Bước 1.3: Xóa DNS records liên quan đến Tunnel

Nếu bạn đã thêm DNS records trỏ về tunnel trên Cloudflare:

1. Vào **Cloudflare Dashboard** → chọn domain
2. Tab **DNS** → tìm các record có type `CNAME` trỏ đến `*.cfargotunnel.com`
3. **Xóa** tất cả các record đó

#### Bước 1.4: Gỡ cloudflared khỏi máy (tùy chọn)

```cmd
:: Nếu cài bằng winget
winget uninstall cloudflared

:: Hoặc xóa thủ công file cloudflared.exe
del "C:\Program Files (x86)\cloudflared\cloudflared.exe"
```

> ✅ **Kết quả:** Tunnel đã được gỡ hoàn toàn. Máy tính cá nhân không còn liên quan đến việc chạy web.

---

## PHẦN 2: Sử dụng VPS Oracle Cloud

### 🔑 Kết nối SSH vào VPS

Mở **PowerShell** hoặc **cmd** trên máy tính:

```powershell
ssh -i C:\Users\Hasky\.ssh\oracle_key ubuntu@<IP_VPS_CUA_BAN>
```

> Thay `<IP_VPS_CUA_BAN>` bằng Public IP thật (ví dụ: `129.154.50.100`)

### 📂 Cấu trúc thư mục trên VPS

```
/home/ubuntu/fras/              ← Thư mục gốc project
├── backend/
│   ├── main.py                 ← FastAPI server chính
│   ├── .env                    ← Biến môi trường (API keys, DB URL)
│   ├── database.py             ← Kết nối database
│   ├── models.py               ← Định nghĩa bảng dữ liệu
│   ├── schemas.py              ← Định nghĩa request/response
│   ├── routers/                ← Các API endpoints
│   │   ├── auth.py             ← Đăng nhập/đăng ký
│   │   ├── survey.py           ← Khảo sát
│   │   ├── admin.py            ← Quản trị
│   │   ├── ai_analysis.py      ← Phân tích AI
│   │   ├── image_analysis.py   ← Phân tích ảnh
│   │   └── ...
│   ├── utils/                  ← Hàm tiện ích
│   ├── middleware/              ← Xác thực, phân quyền
│   ├── venv/                   ← Môi trường Python ảo
│   └── requirements.txt        ← Danh sách packages
├── frontend/
│   ├── index.html              ← Trang chủ
│   ├── login.html              ← Trang đăng nhập
│   ├── dashboard.html          ← Bảng điều khiển
│   ├── survey.html             ← Trang khảo sát
│   ├── css/                    ← Styles
│   ├── js/                     ← JavaScript
│   │   ├── api.js              ← Gọi API từ frontend
│   │   ├── auth.js             ← Xử lý đăng nhập
│   │   ├── survey.js           ← Logic khảo sát
│   │   └── ...
│   └── admin/                  ← Trang quản trị
└── docker-compose.yml
```

### 🛠️ Các lệnh quản lý VPS thường dùng

#### Quản lý Backend Service (FRAS)

| Mục đích | Lệnh |
|----------|-------|
| **Xem trạng thái** | `sudo systemctl status fras` |
| **Khởi động lại** | `sudo systemctl restart fras` |
| **Dừng backend** | `sudo systemctl stop fras` |
| **Bật backend** | `sudo systemctl start fras` |
| **Xem log realtime** | `sudo journalctl -u fras -f` |
| **Xem 50 dòng log cuối** | `sudo journalctl -u fras -n 50` |
| **Xem log lỗi** | `sudo journalctl -u fras -p err` |

#### Quản lý Nginx (Web Server)

| Mục đích | Lệnh |
|----------|-------|
| **Xem trạng thái** | `sudo systemctl status nginx` |
| **Khởi động lại** | `sudo systemctl restart nginx` |
| **Kiểm tra cấu hình** | `sudo nginx -t` |
| **Xem log truy cập** | `sudo tail -f /var/log/nginx/access.log` |
| **Xem log lỗi** | `sudo tail -f /var/log/nginx/error.log` |
| **Sửa cấu hình Nginx** | `sudo nano /etc/nginx/sites-available/fras` |

#### Quản lý PostgreSQL (Database)

| Mục đích | Lệnh |
|----------|-------|
| **Vào PostgreSQL** | `sudo -u postgres psql` |
| **Vào database fras** | `sudo -u postgres psql -d fras` |
| **Xem các bảng** | `\dt` (trong psql) |
| **Xem dữ liệu users** | `SELECT id, email, role FROM users;` (trong psql) |
| **Backup database** | `pg_dump -U frasuser fras > ~/backup_$(date +%Y%m%d).sql` |
| **Restore database** | `psql -U frasuser fras < ~/backup_20260320.sql` |
| **Thoát psql** | `\q` |

#### Quản lý hệ thống VPS

| Mục đích | Lệnh |
|----------|-------|
| **Xem dung lượng ổ cứng** | `df -h` |
| **Xem RAM đang dùng** | `free -h` |
| **Xem CPU đang dùng** | `top` (nhấn `q` để thoát) |
| **Cập nhật hệ thống** | `sudo apt update && sudo apt upgrade -y` |
| **Xem IP public** | `curl ifconfig.me` |
| **Restart VPS** | `sudo reboot` |

### 🔄 Quy trình cập nhật code lên VPS

Khi bạn đã sửa code trên máy tính và push lên GitHub:

```bash
# SSH vào VPS
ssh -i C:\Users\Hasky\.ssh\oracle_key ubuntu@<IP_VPS>

# Trên VPS, chạy:
cd /home/ubuntu/fras

# Pull code mới từ GitHub
git pull origin main

# Nếu có thay đổi requirements.txt (thêm package mới):
cd backend
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Restart backend để áp dụng code mới
sudo systemctl restart fras

# Kiểm tra xem có lỗi không
sudo systemctl status fras
sudo journalctl -u fras -n 20
```

### ⚠️ Xử lý sự cố thường gặp trên VPS

#### Web không truy cập được

```bash
# 1. Kiểm tra backend có chạy không
sudo systemctl status fras

# 2. Kiểm tra nginx có chạy không
sudo systemctl status nginx

# 3. Kiểm tra port có mở không
sudo iptables -L -n | grep 80
sudo iptables -L -n | grep 443

# 4. Kiểm tra log lỗi
sudo journalctl -u fras -n 50
sudo tail -20 /var/log/nginx/error.log
```

#### Backend bị crash liên tục

```bash
# Xem log chi tiết
sudo journalctl -u fras -n 100 --no-pager

# Thử chạy thủ công để xem lỗi
cd /home/ubuntu/fras/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
# Xem lỗi hiện ra → sửa → Ctrl+C → restart service
```

#### Database bị lỗi

```bash
# Kiểm tra PostgreSQL
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Kiểm tra kết nối
sudo -u postgres psql -c "SELECT 1;"
```

---

## PHẦN 3: Trỏ tên miền Hostinger về Oracle Cloud

### 🌐 Cách 1: Dùng DNS của Hostinger trực tiếp (Đơn giản nhất)

Nếu bạn **KHÔNG dùng Cloudflare** làm DNS proxy:

1. Đăng nhập [Hostinger hPanel](https://hpanel.hostinger.com/)
2. Chọn domain của bạn → **DNS / Nameservers** → **DNS Records**
3. **Xóa** tất cả record cũ liên quan đến tunnel (CNAME trỏ về cloudflare tunnel)
4. **Thêm** các record mới:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| **A** | `@` | `<IP_VPS_ORACLE>` | 3600 |
| **A** | `www` | `<IP_VPS_ORACLE>` | 3600 |

> Thay `<IP_VPS_ORACLE>` bằng Public IP thật của VPS Oracle.

5. Đợi 5-30 phút để DNS cập nhật (có thể lên đến 24h trong một số trường hợp)

### 🌐 Cách 2: Dùng Cloudflare làm DNS proxy (Khuyến nghị - Bảo mật hơn)

Nếu bạn muốn dùng Cloudflare để ẩn IP thật và có thêm bảo vệ DDoS:

1. **Trên Hostinger:** Đổi Nameservers sang Cloudflare
   - Vào hPanel → Domain → **DNS / Nameservers** → **Change Nameservers**
   - Nhập nameservers của Cloudflare (ví dụ: `ada.ns.cloudflare.com`, `bob.ns.cloudflare.com`)

2. **Trên Cloudflare Dashboard:**
   - Thêm domain → tab **DNS**
   - Thêm records:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| **A** | `@` | `<IP_VPS_ORACLE>` | Proxied ☁️ |
| **A** | `www` | `<IP_VPS_ORACLE>` | Proxied ☁️ |

3. **Trên VPS Oracle**, cập nhật Nginx config:

```bash
sudo nano /etc/nginx/sites-available/fras
```

Đổi `server_name` thành tên miền thật:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo nginx -t
sudo systemctl restart nginx
```

### 🔒 Cài SSL (HTTPS) trên VPS

#### Nếu dùng Cloudflare Proxy (Cách 2):
- Cloudflare tự cấp SSL → bạn chỉ cần bật **SSL/TLS** → **Full** trên Cloudflare Dashboard
- Không cần cài Certbot trên VPS

#### Nếu dùng DNS Hostinger trực tiếp (Cách 1):
```bash
# Cài Certbot trên VPS
sudo apt install -y certbot python3-certbot-nginx

# Tạo chứng chỉ SSL (thay bằng domain thật)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Tự động gia hạn
sudo systemctl enable certbot.timer
```

### ✅ Kiểm tra kết quả

```bash
# Trên máy tính, kiểm tra DNS đã trỏ đúng chưa
nslookup yourdomain.com

# Hoặc dùng trình duyệt truy cập
# http://yourdomain.com → phải thấy trang FRAS
```

---

## PHẦN 4: Quy trình nâng cấp web

### 🏗️ Tổng quan kiến trúc hiện tại

```
FRAS - Hệ thống Đánh giá Nguy cơ Cháy Nổ
├── Backend: FastAPI (Python) - Port 8000
│   ├── Auth (JWT) - Đăng nhập/đăng ký
│   ├── Survey - Khảo sát đánh giá
│   ├── AI Analysis - Phân tích AI (Gemini)
│   ├── Image Analysis - Phân tích ảnh
│   ├── Admin - Quản trị hệ thống
│   ├── Export - Xuất báo cáo
│   ├── Notifications - Thông báo
│   └── Improvement - Kế hoạch cải thiện
├── Frontend: HTML/CSS/JS (Vanilla)
│   ├── Trang chủ, Đăng nhập, Đăng ký
│   ├── Dashboard, Khảo sát, Kết quả
│   ├── Lịch sử, So sánh, Bản đồ
│   └── Admin Panel
└── Database: PostgreSQL
```

### 📝 Quy trình nâng cấp từ A đến Z

#### Bước 4.1: Lên kế hoạch (Trên máy tính cá nhân)

Trước khi code, hãy xác định rõ:

```
1. Chức năng mới là gì? (Mô tả chi tiết)
2. Cần thay đổi gì ở Backend? (API mới, sửa API cũ?)
3. Cần thay đổi gì ở Frontend? (Trang mới, sửa trang cũ?)
4. Cần thay đổi gì ở Database? (Bảng mới, cột mới?)
5. Có cần cài thêm package Python không?
```

#### Bước 4.2: Phát triển trên máy cá nhân

##### a) Chạy project trên máy cá nhân để test

```cmd
:: Mở cmd tại thư mục project
cd c:\Users\Hasky\.gemini\antigravity\scratch\fras\backend

:: Cài packages (nếu chưa)
pip install -r requirements.txt

:: Chạy server local
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> `--reload` sẽ tự restart server mỗi khi bạn sửa code → tiện cho phát triển.

##### b) Thêm chức năng Backend mới

**Nếu cần tạo API endpoint mới:**

1. Tạo file router mới trong [`backend/routers/`](backend/routers/):

```python
# backend/routers/ten_chuc_nang.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/ten-chuc-nang", tags=["Ten Chuc Nang"])

@router.get("/")
def get_data(db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Logic xử lý ở đây
    return {"message": "OK"}

@router.post("/")
def create_data(data: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Logic tạo mới ở đây
    return {"message": "Created"}
```

2. Đăng ký router trong [`backend/main.py`](backend/main.py:188):

```python
# Thêm import
from routers import ten_chuc_nang

# Thêm dòng này vào phần Register routers
app.include_router(ten_chuc_nang.router)
```

**Nếu cần thêm bảng/cột database mới:**

1. Thêm model trong [`backend/models.py`](backend/models.py):

```python
class TenBangMoi(Base):
    __tablename__ = "ten_bang_moi"
    
    id = Column(Integer, primary_key=True, index=True)
    ten = Column(String(200), nullable=False)
    mo_ta = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
```

2. Nếu thêm cột vào bảng đã có, thêm migration trong [`backend/database.py`](backend/database.py:24):

```python
def migrate_db():
    # ... code hiện tại ...
    migrations = {
        # ... migrations hiện tại ...
        "ten_bang": {
            "cot_moi": "VARCHAR(200)",
        },
    }
```

**Nếu cần thêm schema (validate dữ liệu):**

Thêm trong [`backend/schemas.py`](backend/schemas.py):

```python
class TenChucNangCreate(BaseModel):
    ten: str
    mo_ta: Optional[str] = None

class TenChucNangResponse(BaseModel):
    id: int
    ten: str
    mo_ta: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
```

##### c) Thêm chức năng Frontend mới

**Nếu cần tạo trang mới:**

1. Tạo file HTML trong [`frontend/`](frontend/):

```html
<!-- frontend/ten_chuc_nang.html -->
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tên Chức Năng - FRAS</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand"><a href="/">🔥 FRAS</a></div>
        <ul class="nav-links"></ul>
        <div class="nav-user"></div>
    </nav>

    <main class="container">
        <h1>Tên Chức Năng</h1>
        <!-- Nội dung ở đây -->
    </main>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        onReady(() => {
            setupNavbar();
            if (!requireAuth()) return;
            // Logic JavaScript ở đây
            loadData();
        });

        async function loadData() {
            try {
                const data = await api.get('/ten-chuc-nang/');
                console.log(data);
                // Render data lên trang
            } catch (error) {
                showToast(error.message, 'error');
            }
        }
    </script>
</body>
</html>
```

2. Trang mới sẽ tự động được serve bởi FastAPI nhờ route trong [`backend/main.py`](backend/main.py:221):

```python
@app.get("/{page}.html")
async def serve_page(page: str):
    # Tự động serve bất kỳ file .html nào trong frontend/
```

**Nếu cần thêm JavaScript phức tạp:**

Tạo file JS riêng trong [`frontend/js/`](frontend/js/):

```javascript
// frontend/js/ten_chuc_nang.js
async function loadTenChucNang() {
    const data = await api.get('/ten-chuc-nang/');
    // Xử lý data
}
```

Rồi include trong HTML:
```html
<script src="/js/ten_chuc_nang.js"></script>
```

##### d) Thêm package Python mới

Nếu chức năng mới cần thư viện Python:

```cmd
:: Trên máy cá nhân
cd backend
pip install ten-package
pip freeze > requirements.txt
```

> ⚠️ **Lưu ý:** Sau khi thêm package, cần cài lại trên VPS (xem Bước 4.4).

#### Bước 4.3: Test trên máy cá nhân

```cmd
:: Chạy server local
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

:: Mở trình duyệt: http://localhost:8000
:: Test tất cả chức năng mới
:: Test cả chức năng cũ (đảm bảo không bị hỏng)
```

**Checklist test:**
- [ ] Chức năng mới hoạt động đúng
- [ ] Các chức năng cũ vẫn hoạt động
- [ ] Đăng nhập/đăng ký vẫn OK
- [ ] Trang admin vẫn OK
- [ ] Không có lỗi trong console trình duyệt (F12)
- [ ] Không có lỗi trong terminal backend

#### Bước 4.4: Push code lên GitHub

```cmd
:: Trên máy cá nhân
cd c:\Users\Hasky\.gemini\antigravity\scratch\fras

:: Xem các file đã thay đổi
git status

:: Thêm tất cả file thay đổi
git add .

:: Commit với mô tả rõ ràng
git commit -m "Thêm chức năng: [mô tả ngắn gọn]"

:: Push lên GitHub
git push origin main
```

#### Bước 4.5: Deploy lên VPS Oracle

```bash
# SSH vào VPS
ssh -i C:\Users\Hasky\.ssh\oracle_key ubuntu@<IP_VPS>

# Pull code mới
cd /home/ubuntu/fras
git pull origin main

# Nếu có thêm package Python mới:
cd backend
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Restart backend
sudo systemctl restart fras

# Kiểm tra
sudo systemctl status fras
sudo journalctl -u fras -n 30
```

#### Bước 4.6: Kiểm tra trên production

- Mở trình duyệt → truy cập domain thật
- Test chức năng mới
- Test chức năng cũ
- Kiểm tra trên điện thoại (responsive)

### 🔄 Tóm tắt quy trình nâng cấp (Quick Reference)

```
┌─────────────────────────────────────────────────────┐
│  QUY TRÌNH NÂNG CẤP WEB FRAS                       │
│                                                     │
│  1. 📝 Lên kế hoạch chức năng mới                   │
│         ↓                                           │
│  2. 💻 Code trên máy cá nhân                        │
│     • Sửa/thêm backend (routers, models, schemas)   │
│     • Sửa/thêm frontend (HTML, JS, CSS)             │
│         ↓                                           │
│  3. 🧪 Test local (http://localhost:8000)            │
│         ↓                                           │
│  4. 📤 Push lên GitHub                              │
│     git add . → git commit → git push               │
│         ↓                                           │
│  5. 🚀 Deploy lên VPS                               │
│     SSH → git pull → pip install → restart fras      │
│         ↓                                           │
│  6. ✅ Kiểm tra trên production                     │
│     Truy cập domain thật → test chức năng            │
└─────────────────────────────────────────────────────┘
```

### 💡 Gợi ý chức năng có thể nâng cấp

Dựa trên cấu trúc hiện tại của FRAS, đây là một số hướng nâng cấp:

| # | Chức năng | Mô tả | Độ khó |
|---|-----------|-------|--------|
| 1 | **Báo cáo PDF** | Xuất kết quả đánh giá ra file PDF đẹp | ⭐⭐ |
| 2 | **Dashboard thống kê** | Biểu đồ tổng hợp cho admin (theo thời gian, khu vực) | ⭐⭐ |
| 3 | **Đánh giá định kỳ** | Tự động nhắc đánh giá lại sau X tháng | ⭐⭐ |
| 4 | **Multi-language** | Hỗ trợ đầy đủ tiếng Anh (hiện mới có cơ bản) | ⭐⭐⭐ |
| 5 | **Push Notification** | Thông báo đẩy qua trình duyệt (đã có Service Worker) | ⭐⭐⭐ |
| 6 | **Quản lý file đính kèm** | Upload ảnh/tài liệu cho mỗi đánh giá | ⭐⭐ |
| 7 | **API rate limiting** | Giới hạn số request để bảo vệ server | ⭐ |
| 8 | **Audit log** | Ghi lại mọi thao tác của user/admin | ⭐⭐ |
| 9 | **Forgot password** | Quên mật khẩu → gửi email reset | ⭐⭐⭐ |
| 10 | **2FA** | Xác thực 2 bước (Google Authenticator) | ⭐⭐⭐⭐ |

### 📁 Tóm tắt: File nào cần sửa khi nâng cấp?

| Loại thay đổi | File cần sửa |
|---------------|-------------|
| **Thêm API mới** | `backend/routers/xxx.py` (tạo mới) + `backend/main.py` (đăng ký router) |
| **Thêm bảng DB** | `backend/models.py` |
| **Thêm cột DB** | `backend/models.py` + `backend/database.py` (migration) |
| **Thêm schema** | `backend/schemas.py` |
| **Thêm trang web** | `frontend/xxx.html` (tạo mới) |
| **Sửa giao diện** | `frontend/css/main.css` hoặc tạo CSS mới |
| **Thêm logic JS** | `frontend/js/xxx.js` (tạo mới hoặc sửa) |
| **Thêm package** | `backend/requirements.txt` |
| **Sửa logic AI** | `backend/utils/ai_prompt.py` |
| **Sửa tính điểm** | `backend/utils/scoring.py` |

---

## 🎯 CHECKLIST TỔNG HỢP

### Gỡ Tunnel
- [ ] Tắt cloudflared trên máy cá nhân
- [ ] Xóa tunnel trên Cloudflare Dashboard (nếu có)
- [ ] Xóa DNS records cũ liên quan tunnel

### Trỏ tên miền
- [ ] Thêm A record trỏ về IP Oracle VPS
- [ ] Cập nhật `server_name` trong Nginx config
- [ ] Cài SSL (Certbot hoặc Cloudflare)
- [ ] Truy cập domain thật → thấy web FRAS

### Quy trình nâng cấp
- [ ] Code trên máy cá nhân
- [ ] Test local thành công
- [ ] Push lên GitHub
- [ ] SSH vào VPS → git pull → restart
- [ ] Kiểm tra trên production
