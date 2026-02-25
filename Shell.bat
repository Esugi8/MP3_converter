@echo off
setlocal
cd /d %~dp0

echo ==========================================
echo  Opening terminal with .venv activated...
echo ==========================================

rem Check if .venv exists
if not exist .venv (
    echo [ERROR] .venv folder not found.
    pause
    exit /b
)

rem Open a new cmd window, activate .venv, and then run the python script (/k keeps the window open)
cmd /k ".venv\Scripts\activate.bat & python mp3_converter.py"