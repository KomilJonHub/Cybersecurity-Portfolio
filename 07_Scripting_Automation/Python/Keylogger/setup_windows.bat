@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
    echo Python was not found.
    echo Install Python 3 from https://www.python.org/downloads/windows/
    echo Keep "tcl/tk and IDLE" enabled during installation, then run this file again.
    pause
    exit /b 1
)

echo Creating the project environment...
py -m venv .venv
if errorlevel 1 goto :failed

echo Installing the required pynput package...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed

echo.
echo Setup finished. Double-click run_app.bat to start the program.
pause
exit /b 0

:failed
echo.
echo Setup did not finish. Review the error shown above.
pause
exit /b 1

