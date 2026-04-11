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

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo [OK] DA LUU CODE TREN MAY TAI CHANG GIT LOCAL THANH CONG!
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo [WARNING] KHONG CO THAO TAC NAO MOI HOAC CHUA CO SU THAY DOI CODE NAO DE LUU!
    echo ==========================================
)
echo.
pause
