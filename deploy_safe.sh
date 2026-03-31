#!/bin/bash
# deploy_safe.sh — Deploy code mới mà KHÔNG xóa database
# Dùng script này cho mọi lần update thông thường (sửa bug, thêm feature)
# Chỉ dùng deploy.sh (reset DB) khi cần reset toàn bộ dữ liệu & câu hỏi

set -e

echo "1. Pull newest code from GitHub..."
cd /home/ubuntu/fras
git fetch origin main
git reset --hard origin/main

echo "2. Install new dependencies if any..."
cd backend
source venv/bin/activate
pip install -r requirements.txt --quiet || true

echo "3. Restart backend service (DB stays intact)..."
sudo systemctl restart fras
sleep 3

echo "4. Status check..."
sudo systemctl status fras --no-pager

echo ""
echo "✅ Deploy xong! Database và dữ liệu vẫn còn nguyên."
echo "   Backend tự động chạy migrate_db() khi khởi động nếu có schema mới."
