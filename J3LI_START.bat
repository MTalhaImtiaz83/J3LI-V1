@echo off
title J3LI - Smart Launcher
echo ============================================================
echo    J3LI - Just Three Like It
echo    Starting Cloud-Ready Quranic Research System...
echo ============================================================
echo.

set "CDIR=%~dp0"
cd /d "%CDIR%"

echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.11+.
    pause
    exit /b
)

echo Installing dependencies (first run only)...
pip install -r requirements.txt >nul 2>&1

echo Launching J3LI Interface...
python j3li_app.py

pause