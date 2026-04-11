@echo off
echo [1/3] Xoa venv cu...
rd /s /q "C:\Users\Hasky\pipx\venvs\notebooklm-mcp-cli" 2>nul
del /f /q "C:\Users\Hasky\.local\bin\nlm.exe" 2>nul
del /f /q "C:\Users\Hasky\.local\bin\notebooklm-mcp.exe" 2>nul

echo [2/3] Cai lai notebooklm-mcp-cli...
pipx install notebooklm-mcp-cli

echo [3/3] Kiem tra...
nlm --version

echo.
echo Hoan thanh! Thu chay: nlm notebook list
pause
