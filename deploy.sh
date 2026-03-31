#!/bin/bash
set -e

echo "1. Stop backend service..."
sudo systemctl stop fras

echo "2. Disconnect existing users to prevent 'database is being accessed' error..."
sudo -u postgres psql -c "REVOKE CONNECT ON DATABASE fras FROM PUBLIC;" || true
sudo -u postgres psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'fras';" || true

echo "3. Drop old database & create new..."
sudo -u postgres psql -c "DROP DATABASE fras;"
sudo -u postgres psql -c "CREATE DATABASE fras OWNER frasuser;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE fras TO frasuser;"

echo "4. Pull newest code..."
cd /home/ubuntu/fras
git fetch origin main
git reset --hard origin/main

echo "5. Install new dependencies if any..."
cd backend
source venv/bin/activate
pip install -r requirements.txt || true

echo "6. Start backend service..."
sudo systemctl start fras
sleep 5

echo "7. Status check..."
sudo systemctl status fras --no-pager
