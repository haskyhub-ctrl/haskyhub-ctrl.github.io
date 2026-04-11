@echo off
chcp 65001 >nul
title 2. UP CODE LEN GITHUB

echo ==========================================
echo       [2/3] ĐẨY CODE LÊN GITHUB
echo ==========================================
echo.
echo [Đang tải...] Day thay doi len kho luu tru Github...
git push origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo [OK] DA UP CODE LEN GITHUB THANH CONG!
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo [ERROR] BI LOI KHI PUSH LEN GITHUB (Kiem tra mang hoac Log do tren man hinh)!
    echo ==========================================
)
echo.
pause
