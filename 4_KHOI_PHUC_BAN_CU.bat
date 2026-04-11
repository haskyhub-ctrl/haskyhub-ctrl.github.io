@echo off
setlocal EnableDelayedExpansion
title 4. KHOI PHUC BAN CU

echo ==========================================
echo     [4] CO MAY THOI GIAN - ROLLBACK
echo ==========================================
echo.
echo Lich su 7 lan luu CODE gan nhat cua ban:
echo ------------------------------------------
git log -n 7 --pretty=format:"%%h - %%s"
echo.
echo ------------------------------------------
echo.
echo LUA CHON:
echo - Bam ENTER luon neu muon DAO NGUOC ban vua xay ra loi gan nhat - Lui 1 buoc.
echo - Hoac nhap 7 chu cai ID o dong tren neu muon dao nguoc phien ban xac dinh.
echo.
set /p TARGET_ID=">> Nhap ID hoac Bam Enter: "

if "!TARGET_ID!"=="" (
    set TARGET_ID=HEAD
    echo.
    echo [Dang xu ly] Dang lui ve trang thai luu khoe manh gan nhat...
) else (
    echo.
    echo [Dang xu ly] Dang xoa thay doi loi cua ID: !TARGET_ID! 
)

git revert !TARGET_ID! --no-edit

if !ERRORLEVEL! equ 0 (
    echo.
    echo ==========================================
    echo [OK] DA KHOI PHUC THANH CONG!
    echo Code bi loi da duoc dao nguoc ma khong lam hong form file khac!
    echo.
    echo De Server va Github sua lại thanh ban sạch, hay chay tiep File:
    echo 1. 2_UP_CODE_GITHUB.bat
    echo 2. 3_UP_LEN_ORACLE_FRAS_AI.bat
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo [ERROR] BI XUNG DOT GIUA CODE CU VA MOI KHI KHOI PHUC.
    echo Neu gap loi nay hay nho AI xu ly xung dot Git tren Chatboard!
    echo ==========================================
)
echo.
pause
