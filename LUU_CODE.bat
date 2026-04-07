@echo off
chcp 65001 >nul
title Luu thay doi Code - FRAS

echo ==========================================
echo       LUU THAY DOI VAO GIT (COMMIT)
echo ==========================================
echo.

REM Hien thi cac file da thay doi
git status -s
echo.

REM Yeu cau nhap loi nhan commit
set /p msg="Nhap noi dung thay doi (bam Enter de dung loi nhan mac dinh): "

REM Neu khong nhap gi, dung gio hien tai lam mac dinh
if "%msg%"=="" (
    set msg=Cap nhat code ngay %date% luc %time:~0,5%
)

echo.
echo [>>>] Dang luu code...
git add .
git commit -m "%msg%"

echo.
echo ==========================================
echo [OK] DA LUU CODE THANH CONG!
echo ==========================================
echo.
echo De day len tren mang (Github/Server), ban co the chay them:
echo  git push
echo.
pause
