@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title 4. KHOI PHUC BAN CU

echo ==========================================
echo     [4] CỖ MÁY THỜI GIAN (ROLLBACK)
echo ==========================================
echo.
echo Lich su 7 lan luu CODE gan nhat cua ban:
echo ------------------------------------------
git log -n 7 --pretty=format:"%%h - %%s (%%cr)"
echo.
echo ------------------------------------------
echo.
echo LUA CHON:
echo - De DAO NGUOC nhanh loi cua ban luu gan nhat (Lui ve 1 buoc): Bam ENTER luon khong can nhap gi.
echo - Hoac nhap 7 ky tu ID dung dau tien o danh sach tren neu muon xoa bo loi cua phien ban do.
echo.
set /p "TARGET_ID=>> Nhap ID hoac Bam Enter: "

if "!TARGET_ID!"=="" (
    set TARGET_ID=HEAD
    echo.
    echo [Đang xử lý] Dang dao nguoc thay doi cua ban luu gan nhat...
) else (
    echo.
    echo [Đang xử lý] Dang dao nguoc thay doi cua ID: !TARGET_ID! 
)

REM Thuc hien revert an toan khong hien thi trinh edit van ban cua git
git revert !TARGET_ID! --no-edit

if !ERRORLEVEL! equ 0 (
    echo.
    echo ==========================================
    echo [OK] DA KHOI PHUC THANH CONG!
    echo Code loi do da duoc loai bo khoi thu muc cua ban ma khong lam mat cac file khac!
    echo.
    echo 📌 [QUAN TRONG] De Server va Github nhan ra ban da sua sai, 
    echo VUI LONG CHAY TIEP FILE:
    echo 1. 2_UP_CODE_GITHUB.bat
    echo 2. 3_UP_LEN_ORACLE_FRAS_AI.bat
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo [ERROR] BI XUNG DOT KHI KHOI PHUC.
    echo Do ban luu cu do khac biet qua da so voi hien tai. Neu gap loi nay hay nho AI xu ly xung dot Git.
    echo ==========================================
)
echo.
pause
