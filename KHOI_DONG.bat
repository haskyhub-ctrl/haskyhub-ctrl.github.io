@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo   FRAS - He thong Danh gia Nguy co Chay No
echo   Phong Canh sat PCCC ^& CNCH - Bac Ninh
echo ==========================================
echo.

cd /d "%~dp0backend"

REM Uu tien venv trong backend\venv
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment: backend\venv
) else if exist "..\.venv\Scripts\activate.bat" (
    call ..\.venv\Scripts\activate.bat
    echo [OK] Virtual environment: .venv
) else (
    echo [LOI] Khong tim thay virtual environment!
    echo.
    echo Vui long chay lenh sau de cai dat:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [OK] Dang khoi dong server...
echo.
echo  --^> Truy cap: http://localhost:8000
echo  --^> Dang nhap: admin@fras.vn / admin123
echo  --^> API docs: http://localhost:8000/docs
echo.
echo  Nhan Ctrl+C de dung server hoac tat cua so nay.
echo ==========================================
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo [SERVER DA DUNG CHI TIET LOI NEU CO O TREN]
pause
