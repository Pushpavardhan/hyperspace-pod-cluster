@echo off
title Hyperspace Pod - WORKER NODE
echo ============================================
echo    Joining Hyperspace Pod as WORKER
echo ============================================
set MASTER_IP=192.168.1.50
echo Connecting to %MASTER_IP%:6379 ...
ray stop
ray start --address=%MASTER_IP%:6379
echo SUCCESS! This laptop is now a Worker Node.
echo Dashboard: http://%MASTER_IP%:8265
pause
