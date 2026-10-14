@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo   NAP DU LIEU LUAT PCCC VAO RAG (AI CHI)
echo ==========================================
echo.

cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment: venv
) else (
    echo [LOI] Khong tim thay virtual environment!
    pause
    exit /b 1
)

echo [DANG XU LY] Dang tao Vector Embedding ChromaDB. Vui long doi...
python utils\rag_ingest.py

echo.
echo [HOAN THANH] Da ket thuc tien trinh Nap Du Lieu.
pause
