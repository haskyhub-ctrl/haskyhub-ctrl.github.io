@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title 3. DEPLOY LEN SERVER ORACLE

echo ==========================================
echo    [3/3] CẬP NHẬT CODE LÊN FRAS-AI.COM
echo ==========================================
echo.

if not exist "server_ip_config.txt" (
    echo Lan dau tien chay, vui long thiet lap thong so Server.
    set /p "SERVER_IP=Nhap IP cua Server Oracle (Dang: 129.xxx.xxx.xxx): "
    echo !SERVER_IP!> server_ip_config.txt
) else (
    set /p SERVER_IP=<server_ip_config.txt
)

set SERVER_IP=%SERVER_IP: =%

echo [Đang tải...] Dang ket noi toi Server !SERVER_IP! de cap nhat fras-ai.com...
echo Server se tu dong Pull code moi nhat ve va chay lai Backend...
echo Vui long doi khoang 15-30 giay...
echo.

ssh -o StrictHostKeyChecking=no -i "%USERPROFILE%\.ssh\oracle_key" ubuntu@!SERVER_IP! "bash -c 'cd /home/ubuntu/fras && ./deploy_safe.sh'"

if !ERRORLEVEL! equ 0 (
    echo.
    echo ==========================================
    echo [OK] DA DEPLOY PHIEN BAN MOI NHAT LEN FRAS-AI.COM THANH CONG!
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo [ERROR] TIM THAY LOI KHI KET NOI SERVER HOAC SERVER BAO LOI DEPLOY!
    echo ==========================================
)
echo.
pause
