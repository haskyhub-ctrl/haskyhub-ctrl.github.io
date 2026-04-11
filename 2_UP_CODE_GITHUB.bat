@echo off
title 2. UP CODE LEN GITHUB

echo ==========================================
echo       [2/3] DAY CODE LEN GITHUB
echo ==========================================
echo.
echo [Dang tai...] Day code len kho luu tru Github...
git push origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo [OK] DA UP CODE LEN GITHUB THANH CONG!
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo [ERROR] BI LOI KHI PUSH LEN GITHUB. Kiem tra mang ngay!
    echo ==========================================
)
echo.
pause
