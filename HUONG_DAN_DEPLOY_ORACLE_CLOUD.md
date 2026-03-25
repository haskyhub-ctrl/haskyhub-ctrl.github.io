# ☁️ HƯỚNG DẪN DEPLOY FRAS LÊN ORACLE CLOUD - Chi Tiết Từ A đến Z

## 📋 TỔNG QUAN

Thay vì chạy web trên máy tính cá nhân (phải bật máy 24/7), bạn sẽ đưa toàn bộ lên **Oracle Cloud Free Tier** - một máy chủ ảo (VPS) miễn phí chạy 24/7 trên internet.

### Trước và Sau khi deploy:

```
❌ TRƯỚC (chạy trên máy cá nhân):
   Người dùng → Cloudflare Tunnel → Máy tính bạn (phải bật 24/7)
   → Tắt máy = web chết

✅ SAU (chạy trên Oracle Cloud):
   Người dùng → Tên miền → Oracle Cloud VPS (chạy 24/7 miễn phí)
   → Không cần bật máy cá nhân
```

### Oracle Cloud Free Tier cho bạn gì?

| Tài nguyên | Miễn phí |
|------------|----------|
| **VM Instance** | 1-2 máy ảo ARM (4 CPU, 24GB RAM) hoặc 2 AMD (1 CPU, 1GB RAM) |
| **Storage** | 200GB ổ cứng |
| **Bandwidth** | 10TB/tháng |
| **Thời hạn** | Vĩnh viễn (Always Free) |

> ⚡ Với dự án FRAS, bạn chỉ cần **1 VM AMD** (1 CPU, 1GB RAM) là đủ.

---

## 🚀 CÁC BƯỚC THỰC HIỆN

---

### BƯỚC 1: Tạo VM Instance trên Oracle Cloud

1. Đăng nhập vào [Oracle Cloud Console](https://cloud.oracle.com)
2. Ở trang chủ, nhấn **"Create a VM instance"** (hoặc vào menu ☰ → Compute → Instances → Create Instance)
3. Cấu hình như sau:

| Mục | Giá trị |
|-----|---------|
| **Name** | `fras-server` |
| **Image** | Ubuntu 22.04 (hoặc 24.04) - **Canonical Ubuntu** |
| **Shape** | `VM.Standard.E2.1.Micro` (Always Free - 1 OCPU, 1GB RAM) |
| **Networking** | Để mặc định (tự tạo VCN mới) |
| **SSH Key** | ⭐ Quan trọng - xem bên dưới |

#### Tạo SSH Key (để kết nối vào máy chủ):

**Trên Windows**, mở **PowerShell** và chạy:
```powershell
ssh-keygen -t rsa -b 4096 -f $env:USERPROFILE\.ssh\oracle_key
```
- Nhấn Enter 2 lần (không cần đặt password)
- File key sẽ được tạo tại: `C:\Users\Hasky\.ssh\oracle_key` (private) và `oracle_key.pub` (public)

**Quay lại Oracle Cloud:**
- Chọn **"Upload public key files"**
- Upload file `C:\Users\Hasky\.ssh\oracle_key.pub`
- Nhấn **"Create"** để tạo VM

⏳ Đợi 2-3 phút cho VM khởi động. Sau khi trạng thái chuyển sang **RUNNING**, ghi lại **Public IP Address** (ví dụ: `129.154.xxx.xxx`)

---

### BƯỚC 2: Mở Port trên Oracle Cloud (RẤT QUAN TRỌNG)

Oracle Cloud mặc định **chặn tất cả các port**. Bạn cần mở port 80 (HTTP) và 443 (HTTPS):

1. Vào **Oracle Cloud Console** → Menu ☰ → **Networking** → **Virtual Cloud Networks**
2. Nhấn vào VCN đã tạo (ví dụ: `vcn-xxxxxxxxx`)
3. Nhấn vào **Public Subnet** → nhấn vào **Security List** (Default Security List)
4. Nhấn **"Add Ingress Rules"** và thêm 2 rule:

**Rule 1 - HTTP (port 80):**
| Mục | Giá trị |
|-----|---------|
| Source Type | CIDR |
| Source CIDR | `0.0.0.0/0` |
| IP Protocol | TCP |
| Destination Port Range | `80` |

**Rule 2 - HTTPS (port 443):**
| Mục | Giá trị |
|-----|---------|
| Source Type | CIDR |
| Source CIDR | `0.0.0.0/0` |
| IP Protocol | TCP |
| Destination Port Range | `443` |

**Rule 3 - Backend (port 8000) - để test:**
| Mục | Giá trị |
|-----|---------|
| Source Type | CIDR |
| Source CIDR | `0.0.0.0/0` |
| IP Protocol | TCP |
| Destination Port Range | `8000` |

Nhấn **"Add Ingress Rules"** để lưu.

---

### BƯỚC 3: Kết nối SSH vào VM

Mở **PowerShell** trên máy bạn, chạy:

```powershell
ssh -i $env:USERPROFILE\.ssh\oracle_key ubuntu@<PUBLIC_IP>
```

Thay `<PUBLIC_IP>` bằng IP thật của VM (ví dụ: `129.154.50.100`).

Lần đầu kết nối sẽ hỏi `Are you sure...?` → gõ `yes` và Enter.

> ✅ Nếu thấy `ubuntu@fras-server:~$` là bạn đã vào được VM thành công!

---

### BƯỚC 4: Cài đặt phần mềm trên VM

Sau khi SSH vào VM, chạy **từng lệnh một** theo thứ tự:

```bash
# 1. Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# 2. Cài Python 3 và pip
sudo apt install -y python3 python3-pip python3-venv

# 3. Cài PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# 4. Cài Nginx (web server để chuyển tiếp request)
sudo apt install -y nginx

# 5. Cài Git
sudo apt install -y git

# 6. Mở firewall cho port 80, 443, 8000
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo netfilter-persistent save
```

---

### BƯỚC 5: Cấu hình PostgreSQL

```bash
# 1. Đăng nhập vào PostgreSQL
sudo -u postgres psql

# 2. Trong PostgreSQL, chạy các lệnh sau:
CREATE USER frasuser WITH PASSWORD 'FrasSecure2024!';
CREATE DATABASE fras OWNER frasuser;
GRANT ALL PRIVILEGES ON DATABASE fras TO frasuser;
\q
```

---

### BƯỚC 6: Clone code từ GitHub và cấu hình

```bash
# 1. Clone dự án từ GitHub
cd /home/ubuntu
git clone https://github.com/haskyhub-ctrl/FRAR.git fras

# 2. Vào thư mục backend
cd fras/backend

# 3. Tạo môi trường ảo Python
python3 -m venv venv
source venv/bin/activate

# 4. Cài đặt các package
pip install -r requirements.txt
pip install gunicorn
```

#### Tạo file `.env` trên server:

```bash
nano .env
```

Dán nội dung sau vào (nhấn Ctrl+Shift+V để dán):

```
# Backend Environment Variables
GEMINI_API_KEY="AIzaSyBdf88j0uRkjX00ov5YsCqu5NQ2PY82_bI"
SECRET_KEY="fras-production-secret-key-oracle-2024"
DATABASE_URL="postgresql://frasuser:FrasSecure2024!@localhost:5432/fras"
```

Nhấn `Ctrl + O` → Enter để lưu, `Ctrl + X` để thoát.

---

### BƯỚC 7: Test thử Backend

```bash
# Đảm bảo đang trong thư mục backend và venv đã kích hoạt
cd /home/ubuntu/fras/backend
source venv/bin/activate

# Chạy thử
uvicorn main:app --host 0.0.0.0 --port 8000
```

Mở trình duyệt trên máy tính bạn, truy cập: `http://<PUBLIC_IP>:8000`

Nếu thấy trang web FRAS → **thành công!** Nhấn `Ctrl + C` để dừng server (chúng ta sẽ thiết lập chạy tự động ở bước tiếp theo).

---

### BƯỚC 8: Thiết lập chạy tự động (Systemd Service)

Tạo file service để backend tự chạy khi khởi động:

```bash
sudo nano /etc/systemd/system/fras.service
```

Dán nội dung sau:

```ini
[Unit]
Description=FRAS Backend Server
After=network.target postgresql.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/fras/backend
Environment="PATH=/home/ubuntu/fras/backend/venv/bin:/usr/bin"
EnvironmentFile=/home/ubuntu/fras/backend/.env
ExecStart=/home/ubuntu/fras/backend/venv/bin/gunicorn -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Lưu và thoát (`Ctrl+O`, Enter, `Ctrl+X`), sau đó chạy:

```bash
# Kích hoạt service
sudo systemctl daemon-reload
sudo systemctl enable fras
sudo systemctl start fras

# Kiểm tra trạng thái
sudo systemctl status fras
```

Nếu thấy **`active (running)`** → Backend đã chạy tự động, dù restart VM cũng tự bật lại!

---

### BƯỚC 9: Cấu hình Nginx (Reverse Proxy)

Nginx sẽ đóng vai trò chuyển tiếp request từ port 80 (HTTP) vào port 8000 (Backend):

```bash
sudo nano /etc/nginx/sites-available/fras
```

Dán nội dung:

```nginx
server {
    listen 80;
    server_name _;

    # Tăng giới hạn upload file (cho tính năng đánh giá ảnh)
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

Lưu, thoát, rồi kích hoạt:

```bash
# Xóa config mặc định, kích hoạt config FRAS
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/fras /etc/nginx/sites-enabled/

# Kiểm tra cú pháp
sudo nginx -t

# Khởi động lại Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

✅ Giờ bạn có thể truy cập web bằng: `http://<PUBLIC_IP>` (không cần gõ port 8000 nữa!)

---

### BƯỚC 10: Gán tên miền (Nếu có)

Nếu bạn đã có tên miền `fras-ai.com` trên Cloudflare:

1. Vào **Cloudflare Dashboard** → chọn domain `fras-ai.com`
2. Vào tab **DNS**
3. Thêm record:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | `@` | `<PUBLIC_IP của Oracle>` | Proxied ☁️ |
| A | `www` | `<PUBLIC_IP của Oracle>` | Proxied ☁️ |
| A | `api` | `<PUBLIC_IP của Oracle>` | Proxied ☁️ |

4. Sau đó cập nhật lại file Nginx:

```bash
sudo nano /etc/nginx/sites-available/fras
```

Đổi dòng `server_name _;` thành:
```nginx
server_name fras-ai.com www.fras-ai.com api.fras-ai.com;
```

Restart nginx:
```bash
sudo systemctl restart nginx
```

> ✅ Giờ mọi người truy cập `http://fras-ai.com` là vào được web FRAS!

---

### BƯỚC 11 (Tùy chọn): Cài SSL (HTTPS) miễn phí

```bash
# Cài Certbot
sudo apt install -y certbot python3-certbot-nginx

# Tạo chứng chỉ SSL (thay bằng domain thật của bạn)
sudo certbot --nginx -d fras-ai.com -d www.fras-ai.com

# Tự động gia hạn
sudo systemctl enable certbot.timer
```

> ✅ Giờ web có `https://fras-ai.com` với ổ khóa xanh!

---

## 📊 TÓM TẮT KIẾN TRÚC SAU KHI DEPLOY

```
🌍 Người dùng gõ: fras-ai.com
        │
        ▼
☁️ Cloudflare DNS (chuyển hướng đến IP Oracle)
        │
        ▼
🖥️ Oracle Cloud VM (chạy 24/7 miễn phí)
   ┌────────────────────────────────┐
   │  Nginx (port 80/443)          │
   │     │                         │
   │     ▼                         │
   │  Gunicorn + FastAPI (port 8000) │
   │     │                         │
   │     ▼                         │
   │  PostgreSQL (port 5432)       │
   │  📂 Database: fras            │
   └────────────────────────────────┘
```

---

## 🔧 CÁC LỆNH HỮU ÍCH SAU KHI DEPLOY

| Mục đích | Lệnh |
|----------|-------|
| **Xem log backend** | `sudo journalctl -u fras -f` |
| **Restart backend** | `sudo systemctl restart fras` |
| **Dừng backend** | `sudo systemctl stop fras` |
| **Xem trạng thái** | `sudo systemctl status fras` |
| **Cập nhật code mới** | `cd /home/ubuntu/fras && git pull && sudo systemctl restart fras` |
| **Xem log Nginx** | `sudo tail -f /var/log/nginx/access.log` |
| **Restart Nginx** | `sudo systemctl restart nginx` |
| **Backup database** | `pg_dump -U frasuser fras > backup_$(date +%Y%m%d).sql` |

---

## ❓ CÂU HỎI THƯỜNG GẶP

### Q: Tắt máy tính cá nhân thì web còn chạy không?
**A:** CÓ! Web chạy trên Oracle Cloud, không liên quan đến máy bạn. Bạn tắt máy thoải mái.

### Q: Cập nhật code như thế nào?
**A:** SSH vào server, chạy:
```bash
cd /home/ubuntu/fras
git pull
sudo systemctl restart fras
```

### Q: Oracle Cloud có thật sự miễn phí không?
**A:** Có. "Always Free" tier không bao giờ hết hạn. Chỉ cần bạn không tự upgrade lên tài khoản trả phí.

### Q: Nếu quên password PostgreSQL?
**A:** Xem lại file `/home/ubuntu/fras/backend/.env` trên server.

### Q: Web bị chậm thì sao?
**A:** VM miễn phí chỉ có 1 CPU + 1GB RAM. Nếu quá chậm, có thể upgrade lên ARM VM (4 CPU, 24GB RAM) - vẫn miễn phí.

---

## 🎯 CHECKLIST TỔNG HỢP

- [ ] Tạo VM Instance trên Oracle Cloud
- [ ] Lấy được Public IP
- [ ] Mở port 80, 443, 8000 trên Security List
- [ ] SSH vào VM thành công
- [ ] Cài Python, PostgreSQL, Nginx, Git
- [ ] Tạo database `fras` và user `frasuser`
- [ ] Clone code từ GitHub
- [ ] Tạo venv + cài packages
- [ ] Tạo file `.env`
- [ ] Test thử `uvicorn` thành công
- [ ] Tạo systemd service (tự động chạy)
- [ ] Cấu hình Nginx reverse proxy
- [ ] Truy cập được `http://<PUBLIC_IP>`
- [ ] (Tùy chọn) Gán tên miền
- [ ] (Tùy chọn) Cài SSL HTTPS
