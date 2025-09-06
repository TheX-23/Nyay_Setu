@echo off
title NyaySetu Legal AI - START HERE
color 0B

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║                 NyaySetu Legal AI                    ║
echo ║              🚀 COMPLETE SETUP 🚀                   ║
echo ╚══════════════════════════════════════════════════════╝
echo.

echo ✅ All files have been cleaned and organized
echo ✅ OAuth code removed, email auth ready
echo ✅ Lingosathi AI properly integrated
echo ✅ Frontend modernized with React
echo ✅ Database and utilities configured
echo.

echo 📋 What you need to do:
echo.
echo 1️⃣  FIRST: Configure your Gmail for email verification
echo    • Enable 2-Factor Authentication in Gmail
echo    • Generate an App Password
echo    • Edit: NyaySetu\backend\.env file
echo.
echo 2️⃣  THEN: Run the complete setup
echo.

set /p choice="Ready to start? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 Starting complete setup...
    call start_nyaysetu_complete.bat
) else (
    echo.
    echo 📝 Setup steps:
    echo    1. Run: setup_environment.bat
    echo    2. Configure Gmail in .env file  
    echo    3. Run: start_nyaysetu_complete.bat
    echo.
    echo 📚 Read: README_SETUP.md for detailed instructions
)

echo.
pause
