@echo off
title NyaySetu Legal AI Platform - Complete Setup
color 0A

echo.
echo ========================================
echo    NyaySetu Legal AI Platform
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    echo.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and try again
    echo.
    pause
    exit /b 1
)

echo Step 1: Setting up Backend...
cd NyaySetu\backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Setting up Frontend...
cd ..\frontend

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

echo.
echo Step 3: Starting services...
echo.

REM Start backend in new window
echo Starting Backend API Server...
start "NyaySetu Backend" cmd /k "cd /d %CD%\..\backend && venv\Scripts\activate.bat && python app.py"

REM Wait a moment
timeout /t 3 >nul

REM Start Lingosathi AI in new window
echo Starting Lingosathi AI Service...
start "Lingosathi AI" cmd /k "cd /d %CD%\..\backend\lingosathi-ai-main && ..\venv\Scripts\activate.bat && python app.py"

REM Wait a moment
timeout /t 3 >nul

REM Start frontend in new window
echo Starting Frontend Development Server...
start "NyaySetu Frontend" cmd /k "cd /d %CD% && npm start"

echo.
echo ========================================
echo    All services are starting up!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Lingosathi AI: http://localhost:10000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
