@echo off
title J3LI - Quranic Research System
echo ============================================================
echo   J3LI - Just Three Like It
echo   Starting Quranic Research System...
echo ============================================================
echo.

cd /d "%~dp0"
echo Working directory: %CD%

set "PYTHONPATH=%CD%"
set "J3LI_DATA_DIR=%CD%\data"

echo Checking Python...

C:\Python314\python.exe --version >nul 2>nul
if %errorlevel%==0 (
    echo Found Python at C:\Python314\python.exe
    echo.
    echo Starting J3LI server...
    C:\Python314\python.exe j3li_app.py
    goto :done
)

python --version >nul 2>nul
if %errorlevel%==0 (
    echo Found Python in PATH
    echo.
    echo Starting J3LI server...
    python j3li_app.py
    goto :done
)

echo.
echo ERROR: Python not found!
echo Please install Python 3.10+ from https://python.org
echo Make sure to check "Add Python to PATH" during installation.
echo.

:done
echo.
echo J3LI server has stopped.
pause
