@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo The project environment has not been created yet.
    echo Double-click setup_windows.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" main.py
if errorlevel 1 (
    echo.
    echo The application ended with an error. Review the message above.
    pause
)

