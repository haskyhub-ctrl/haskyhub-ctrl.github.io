@echo off
setlocal EnableDelayedExpansion
title DAY TRUC TIEP LEN SERVER (KHONG QUA GITHUB)

echo ==========================================
echo    CAP NHAT CODE TRUC TIEP LEN SERVER
echo ==========================================
echo.

if not exist server_ip_config.txt (
    echo Lan dau tien chay, vui long thiet lap thong so Server.
    set /p SERVER_IP="Nhap IP cua Server Oracle dang [129.xxx.xxx.xxx]: "
    echo !SERVER_IP!> server_ip_config.txt
) else (
    set /p SERVER_IP=<server_ip_config.txt
)

set SERVER_IP=%SERVER_IP: =%

echo 1. Dang dong goi code hien tai (an toan, bo qua database va log)...
git archive -o deploy.tar HEAD

if not exist deploy.tar (
    echo [Loi] Khong the tao file, co the do loi Git.
    pause
    exit /b
)

echo 2. Dang gui file len Server !SERVER_IP!...
scp -o StrictHostKeyChecking=no -i "%USERPROFILE%\.ssh\oracle_key" deploy.tar ubuntu@!SERVER_IP!:/home/ubuntu/deploy.tar

if !ERRORLEVEL! neq 0 (
    echo.
    echo [Loi] Day file xuong server that bai. Xem lai ket noi SSH.
    del deploy.tar
    pause
    exit /b
)

echo 3. Giai nen va khoi dong lai backend tren Server...
ssh -o StrictHostKeyChecking=no -i "%USERPROFILE%\.ssh\oracle_key" ubuntu@!SERVER_IP! "cd /home/ubuntu/fras && tar -xf ../deploy.tar && sudo systemctl restart fras && rm ../deploy.tar"

echo.
del deploy.tar
echo ==========================================
echo [OK] DA DAY CODE VA KHOI DONG LAI SERVER XONG!
echo (Server hien dang phuc vu phien ban ban vua day len)
echo ==========================================
echo.
pause
