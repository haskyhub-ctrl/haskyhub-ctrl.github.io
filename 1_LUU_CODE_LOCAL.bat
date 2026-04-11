@echo off
title 1. LUU CODE LOCAL

echo ==========================================
echo       [1/3] LUU CODE CUC BO VAO MAY
echo ==========================================
echo.
echo [Dang tai...] Kiem tra va luu cac thay doi vao Git Local...
git add .
git commit -m "Auto save %date% %time:~0,5%"

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo [OK] DA LUU CODE TREN MAY THANH CONG!
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo [WARNING] KHONG CO THAO TAC NAO MOI DE LUU!
    echo ==========================================
)
echo.
pause
