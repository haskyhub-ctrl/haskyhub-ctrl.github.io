# 📚 NotebookLM MCP CLI — Hướng dẫn sử dụng

> Công cụ tích hợp Google NotebookLM vào môi trường local & AI tools (Claude, Cursor, v.v.)  
> GitHub: https://github.com/jacob-bd/notebooklm-mcp-cli  
> Tài khoản: `moonshinemylove@gmail.com`

---

## ⚙️ Cài đặt

```powershell
# Cài qua pipx
pipx install notebooklm-mcp-cli

# Nâng cấp (đóng mọi terminal đang chạy nlm trước)
pipx upgrade notebooklm-mcp-cli
```

---

## 🔑 Xác thực

```powershell
# Đăng nhập (mở Chrome để xác thực Google)
nlm login

# Xem thông tin profile hiện tại
nlm login show

# Đổi profile
nlm login --profile ten_profile
```

**Lưu ý:** Nếu lỗi `FileExistsError` khi login:
1. Xóa các file (không phải thư mục) trong `C:\Users\Hasky\.notebooklm-mcp-cli\`  
   - `chrome-profiles` (nếu là file)  
   - `cache` (nếu là file)  
2. Chạy lại `nlm login`

---

## 📓 Quản lý Notebooks

### Danh sách các notebooks hiện có

| ID | Tên | Sources |
|----|-----|---------|
| `7b3226d6-...` | Bac Ninh Fire Alarm Transmission and Database Implementation Guide | 12 |
| `8cfa2cc0-...` | *(không tên)* | 0 |
| `3dde892e-...` | Weekly Fire Safety Briefing and Work Plan January 2026 | 2 |

```powershell
# Liệt kê tất cả notebooks
nlm notebook list

# Xem chi tiết 1 notebook
nlm notebook get <notebook_id>

# Tạo notebook mới
nlm notebook create --title "Tên notebook"

# Xóa notebook
nlm notebook delete <notebook_id>
```

---

## 📎 Quản lý Sources

```powershell
# Xem sources trong notebook
nlm source list <notebook_id>

# Thêm source (file, URL, text)
nlm add source <notebook_id> --url https://example.com
nlm add source <notebook_id> --file duong/dan/file.pdf

# Xóa source
nlm source delete <notebook_id> <source_id>
```

---

## 💬 Chat / Query

```powershell
# Chat với nội dung notebook
nlm query notebook <notebook_id> "Câu hỏi của bạn"

# Ví dụ
nlm query notebook 7b3226d6-fbab-41c8-b3aa-5f278a901256 "Hệ thống báo cháy cần kết nối gì?"
```

---

## 📝 Notes

```powershell
# Xem notes
nlm note list <notebook_id>

# Tạo note
nlm note create <notebook_id> --content "Nội dung note"
```

---

## 🤖 Tích hợp MCP với AI Tools (Cursor / Claude)

```powershell
# Cài đặt MCP server cho AI tool
nlm setup

# Kiểm tra cấu hình
nlm doctor
```

File config MCP thường ở:  
`C:\Users\Hasky\.notebooklm-mcp-cli\profiles\default`

---

## 🎨 Studio / Audio / Quiz / Mindmap

```powershell
# Tạo audio overview
nlm audio create <notebook_id>

# Tạo quiz
nlm quiz create <notebook_id>

# Tạo mindmap
nlm mindmap create <notebook_id>

# Tạo flashcards
nlm flashcards create <notebook_id>

# Tạo slides
nlm slides create <notebook_id>
```

---

## 🔧 Tiện ích

```powershell
# Xem tất cả lệnh
nlm --help
nlm <command> --help

# Kiểm tra version
nlm --version

# Chẩn đoán cài đặt
nlm doctor

# Đặt alias cho notebook ID
nlm alias set fras 7b3226d6-fbab-41c8-b3aa-5f278a901256

# Sau đó dùng alias thay ID
nlm query notebook fras "câu hỏi"
```

---

## 📂 Thư mục dữ liệu

| Đường dẫn | Nội dung |
|-----------|---------|
| `C:\Users\Hasky\.notebooklm-mcp-cli\profiles\` | Cookie & thông tin xác thực |
| `C:\Users\Hasky\.notebooklm-mcp-cli\chrome-profiles\` | Chrome profile tạm |
| `C:\Users\Hasky\.notebooklm-mcp-cli\cache\` | Cache version check |

---

*Cập nhật lần cuối: 2026-04-11*
