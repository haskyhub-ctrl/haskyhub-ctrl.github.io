@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo   CAI DAT VA KHOI DONG HE THONG FRAS
echo ==========================================
echo.

cd /d "%~dp0backend"

if not exist "venv\Scripts\activate.bat" (
    echo [1/3] Dang tao moi Virtual Environment (venv)...
    python -m venv venv
    if errorlevel 1 (
        echo [LOI] Khong the tao venv. Vui long kiem tra lai Python da cai chua.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Da tim thay Virtual Environment.
)

echo.
echo [2/3] Dang tai va cai dat thu vien (Requirements)...
echo Qua trinh nay co the mat vai phut, vui long cho...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo [LOI] Co loi xay ra trong qua trinh cai dat thu vien!
    pause
    exit /b 1
)

echo.
echo [3/3] Dang khoi dong server...
echo.
echo  --^> Truy cap: http://localhost:8000
echo  --^> Dang nhap: admin@fras.vn / admin123
echo  --^> API docs: http://localhost:8000/docs
echo.
echo  Nhan Ctrl+C de dung server
echo ==========================================
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Server da dung.
pause
