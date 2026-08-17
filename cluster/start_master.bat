@echo off
title Hyperspace Pod - MASTER NODE
echo ============================================
echo    MASTER NODE Starting on Laptop 1
echo ============================================
echo Your IP address:
ipconfig | findstr /i IPv4
echo.
echo Dashboard: http://localhost:8265
echo.
ray stop
ray start --head --port=6379 --dashboard-host=0.0.0.0 --dashboard-port=8265
echo MASTER IS RUNNING! Open http://localhost:8265
pause
