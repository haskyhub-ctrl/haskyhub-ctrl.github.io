@echo off
chcp 65001 >nul
title 1. LUU CODE LOCAL

echo ==========================================
echo       [1/3] LƯU CODE CỤC BỘ VÀO MÁY
echo ==========================================
echo.
echo [Đang tải...] Kiem tra va luu cac thay doi moi nhat vao Git Local...
git add .
git commit -m "Auto save %date% %time:~0,5%"
echo.
echo [OK] DA LUU CODE TREN MAY TAI CHANG GIT LOCAL THANH CONG!
echo.
timeout /t 3
