@echo off
cd /d "%~dp0"
set "PYTHONPATH=%~dp0"
set "J3LI_DATA_DIR=%~dp0data"
python -m uvicorn j3li.api.main:app --host 0.0.0.0 --port 8000
pause
