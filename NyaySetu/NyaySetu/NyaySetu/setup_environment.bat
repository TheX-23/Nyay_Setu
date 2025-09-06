@echo off
echo Setting up NyaySetu environment...
echo.

REM Create .env file for backend
echo Creating backend environment file...
(
echo # Email Configuration for Gmail
echo SMTP_HOST=smtp.gmail.com
echo SMTP_PORT=587
echo SMTP_USER=your-email@gmail.com
echo SMTP_PASS=your-app-password
echo.
echo # JWT Configuration
echo JWT_SECRET=nyaysetu-secret-key-2024
echo.
echo # App Configuration
echo APP_BASE_URL=http://localhost:5000
echo FLASK_ENV=development
echo.
echo # Legal AI Integration
echo LEGAL_AI_URL=http://localhost:10000/chat
echo LEGAL_AI_KEY=
echo.
echo # Database
echo NYAYSETU_DB_PATH=nyaysetu.db
echo.
echo # Debug
echo EXPOSE_VERIFY_LINK=1
) > NyaySetu\backend\.env

echo Backend environment file created!
echo.
echo IMPORTANT: Please update the SMTP_USER and SMTP_PASS in NyaySetu\backend\.env with your Gmail credentials
echo For Gmail, you need to:
echo 1. Enable 2-factor authentication
echo 2. Generate an App Password
echo 3. Use that app password in SMTP_PASS
echo.
pause
