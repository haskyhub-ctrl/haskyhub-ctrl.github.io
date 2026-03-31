#!/bin/bash
set -e

echo "1. Stop backend service..."
sudo systemctl stop fras

echo "2. Pull newest code..."
cd /home/ubuntu/fras
git fetch origin main
git reset --hard origin/main

echo "3. Install new dependencies if any..."
cd backend
source venv/bin/activate
pip install -r requirements.txt || true

echo "4. Start backend service..."
sudo systemctl start fras
sleep 5

echo "5. Status check..."
sudo systemctl status fras --no-pager
