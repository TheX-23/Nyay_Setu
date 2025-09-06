@echo off
title NyaySetu AI Setup
color 0A

echo.
echo ========================================
echo    NyaySetu AI Models Setup
echo ========================================
echo.
echo This script will help you set up free AI models for NyaySetu.
echo.
echo Available options:
echo 1. Google Gemini (Recommended - No credit card required)
echo 2. OpenAI GPT-3.5 (Requires payment method, $5 free credit)
echo 3. Anthropic Claude (Requires payment method, $5 free credit)
echo.

echo ========================================
echo    Google Gemini Setup
echo ========================================
echo.
echo To get your Gemini API key:
echo 1. Visit: https://makersuite.google.com/app/apikey
echo 2. Sign in with your Google account
echo 3. Click "Create API Key"
echo 4. Copy the API key (starts with "AIza...")
echo.

echo Enter your Google Gemini API Key (or press Enter to skip):
set /p GEMINI_KEY=AIzaSyDV0SNPq0XuX_ySF2fPvC50kanqxnpQgck
if not "%GEMINI_KEY%"=="" (
    setx GEMINI_API_KEY "AIzaSyDV0SNPq0XuX_ySF2fPvC50kanqxnpQgck"
    echo ✅ Gemini API Key set successfully!
) else (
    echo ⏭️  Skipping Gemini setup
)

echo.
echo ========================================
echo    OpenAI GPT-3.5 Setup
echo ========================================
echo.
echo To get your OpenAI API key:
echo 1. Visit: https://platform.openai.com/api-keys
echo 2. Sign up/Login to OpenAI
echo 3. Click "Create new secret key"
echo 4. Copy the API key (starts with "sk-...")
echo 5. Add payment method at: https://platform.openai.com/account/billing
echo.

echo Enter your OpenAI API Key (or press Enter to skip):
set /p OPENAI_KEY=
if not "%OPENAI_KEY%"=="" (
    setx OPENAI_API_KEY "%OPENAI_KEY%"
    echo ✅ OpenAI API Key set successfully!
) else (
    echo ⏭️  Skipping OpenAI setup
)

echo.
echo ========================================
echo    Anthropic Claude Setup
echo ========================================
echo.
echo To get your Claude API key:
echo 1. Visit: https://console.anthropic.com/
echo 2. Sign up/Login to Anthropic
echo 3. Go to API Keys section
echo 4. Create new API key
echo.

echo Enter your Claude API Key (or press Enter to skip):
set /p CLAUDE_KEY=
if not "%CLAUDE_KEY%"=="" (
    setx CLAUDE_API_KEY "%CLAUDE_KEY%"
    echo ✅ Claude API Key set successfully!
) else (
    echo ⏭️  Skipping Claude setup
)

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Environment variables have been set.
echo.
echo To test your setup:
echo 1. Restart your terminal/command prompt
echo 2. Run: python app.py
echo 3. Test the chat functionality
echo.
echo The system will automatically use the best available AI model:
echo 1. Google Gemini (if available)
echo 2. OpenAI GPT-3.5 (if available)
echo 3. Enhanced Local Model (fallback)
echo.
echo For more information, see: README_FREE_AI_SETUP.md
echo.
pause
