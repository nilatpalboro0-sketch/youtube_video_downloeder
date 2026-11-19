@echo off
setlocal
cd /d "%~dp0"
set VENV_DIR=venv

echo Checking for Python virtual environment...

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Virtual environment not found. Creating one...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Failed to create virtual environment. Please ensure Python is installed and in your PATH.
        pause
        exit /b 1
    )
    echo Virtual environment created.
)

echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

rem Install only when a required package is missing.
python -c "import yt_dlp, imageio_ffmpeg" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies from requirements.txt...
    python -m pip install --disable-pip-version-check -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo Starting the application...
python main.py %*

echo.
echo Application finished.
pause
deactivate
endlocal
