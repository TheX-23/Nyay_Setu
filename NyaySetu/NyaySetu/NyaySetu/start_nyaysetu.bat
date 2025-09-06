@echo off
title NyaySetu Legal Aid Platform
color 0A

echo.
echo ========================================
echo    NyaySetu Legal Aid Platform
echo ========================================
echo.
echo Starting the application...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    echo.
    pause
    exit /b 1
)

:: Check if backend directory exists
if not exist "backend" (
    echo ERROR: Backend directory not found
    echo Please ensure you're running this from the project root
    echo.
    pause
    exit /b 1
)

:: Check if requirements.txt exists
if not exist "backend\requirements.txt" (
    echo ERROR: requirements.txt not found in backend directory
    echo.
    pause
    exit /b 1
)

:: Navigate to backend directory
cd backend

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    pause
    exit /b 1
)

:: Start the Flask application
echo.
echo Starting Flask backend server...
echo Backend will be available at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

:: Start Flask app
python app.py

:: If we get here, the app has stopped
echo.
echo Application stopped.
pause
