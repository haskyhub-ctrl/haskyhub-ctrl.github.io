@echo off
chcp 65001 >nul
title FRAS - He thong Danh gia Nguy co Chay No

echo.
echo  ================================================
echo    FRAS - He thong Danh gia Nguy co Chay No
echo    Phong Canh sat PCCC ^& CNCH - Bac Ninh
echo  ================================================
echo.

REM ── Xac dinh thu muc goc va chuyen vao backend ───────
set "PROJECT_ROOT=%~dp0"
if exist "%PROJECT_ROOT%backend\main.py" (
    cd /d "%PROJECT_ROOT%backend"
) else if exist "main.py" (
    REM Dang o san trong backend
) else if exist "backend\main.py" (
    cd backend
) else (
    echo [LOI] Khong tim thay thu muc backend hoac file main.py.
    echo Vui long chac chan ban dat file bat nay cung cho voi thu muc backend.
    pause
    exit /b 1
)

echo [OK] Thu muc hien tai: %CD%

REM ── Kiem tra Python ────────────────────────────────
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Khong tim thay Python!
    echo.
    echo Vui long tai va cai dat Python tai:
    echo   https://www.python.org/downloads/
    echo.
    echo Nho tick chon "Add Python to PATH" khi cai dat.
    pause
    exit /b 1
)

REM ── Tao virtual environment neu chua co ──────────────
if not exist "venv\Scripts\activate.bat" (
    echo [>>>] Tao virtual environment lan dau...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [LOI] Khong tao duoc venv!
        pause
        exit /b 1
    )
    echo [OK] Da tao virtual environment
    echo.
)

REM ── Kich hoat venv ───────────────────────────────────
call venv\Scripts\activate.bat
echo [OK] Da kich hoat virtual environment

REM ── Cai dat / cap nhat thu vien ──────────────────────
echo [>>>] Kiem tra va cai dat thu vien (co the mat vai phut lan dau)...
pip install -r requirements.txt -q --disable-pip-version-check
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Cai dat thu vien that bai!
    pause
    exit /b 1
)
echo [OK] Thu vien da san sang

REM ── Chay server ──────────────────────────────────────
echo.
echo [>>>] Dang khoi dong server...
echo.
echo  --^> Trang web  : http://localhost:8000
echo  --^> Dang nhap  : admin@fras.vn / admin123
echo  --^> API docs   : http://localhost:8000/docs
echo.
echo  Nhan Ctrl+C de dung server
echo  ================================================
echo.

REM Mo trinh duyet tu dong sang ben
start "" cmd /c "ping -n 3 127.0.0.1 >nul && start http://localhost:8000"

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo  ================================================
echo   Server da dung.
echo  ================================================
pause
