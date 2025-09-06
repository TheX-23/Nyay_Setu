# Free AI Models Setup Guide for NyaySetu

## Overview
This guide shows you how to set up free AI models for NyaySetu without spending any money.

## Option 1: Google Gemini (Recommended - Most Generous Free Tier)

### Step 1: Get Google Gemini API Key
1. **Visit**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy the API key** (starts with "AIza...")

### Step 2: Set Environment Variable
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your_gemini_api_key_here"

# Windows Command Prompt
set GEMINI_API_KEY=your_gemini_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 3: Test Gemini
```bash
python -c "import os; print('Gemini API Key:', os.environ.get('GEMINI_API_KEY', 'Not set'))"
```

### Gemini Free Tier Benefits:
- ✅ **60 requests per minute**
- ✅ **15 million characters per month**
- ✅ **No credit card required**
- ✅ **Excellent for legal advice**

## Option 2: OpenAI GPT-3.5 (Free Tier)

### Step 1: Get OpenAI API Key
1. **Visit**: https://platform.openai.com/api-keys
2. **Sign up/Login** to OpenAI
3. **Click "Create new secret key"**
4. **Copy the API key** (starts with "sk-...")

### Step 2: Set Environment Variable
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "your_openai_api_key_here"

# Windows Command Prompt
set OPENAI_API_KEY=your_openai_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_openai_api_key_here
```

### Step 3: Add Payment Method (Required for Free Tier)
1. **Visit**: https://platform.openai.com/account/billing
2. **Add payment method** (required even for free tier)
3. **You get $5 free credit** (no charges unless you exceed)

### OpenAI Free Tier Benefits:
- ✅ **$5 free credit** (about 1000+ requests)
- ✅ **GPT-3.5-turbo** model
- ✅ **Good for legal advice**

## Option 3: Anthropic Claude (Free Tier)

### Step 1: Get Claude API Key
1. **Visit**: https://console.anthropic.com/
2. **Sign up/Login** to Anthropic
3. **Go to API Keys section**
4. **Create new API key**

### Step 2: Set Environment Variable
```bash
# Windows PowerShell
$env:CLAUDE_API_KEY = "your_claude_api_key_here"

# Windows Command Prompt
set CLAUDE_API_KEY=your_claude_api_key_here

# Linux/Mac
export CLAUDE_API_KEY=your_claude_api_key_here
```

### Claude Free Tier Benefits:
- ✅ **$5 free credit**
- ✅ **Claude-3 Haiku** model
- ✅ **Excellent for legal reasoning**

## Quick Setup Script

Create a file called `setup_ai_keys.bat` (Windows) or `setup_ai_keys.sh` (Linux/Mac):

### Windows (setup_ai_keys.bat):
```batch
@echo off
echo Setting up AI API Keys for NyaySetu...
echo.

echo Enter your Google Gemini API Key (or press Enter to skip):
set /p GEMINI_KEY=
if not "%GEMINI_KEY%"=="" (
    setx GEMINI_API_KEY "%GEMINI_KEY%"
    echo Gemini API Key set successfully!
)

echo.
echo Enter your OpenAI API Key (or press Enter to skip):
set /p OPENAI_KEY=
if not "%OPENAI_KEY%"=="" (
    setx OPENAI_API_KEY "%OPENAI_KEY%"
    echo OpenAI API Key set successfully!
)

echo.
echo Enter your Claude API Key (or press Enter to skip):
set /p CLAUDE_KEY=
if not "%CLAUDE_KEY%"=="" (
    setx CLAUDE_API_KEY "%CLAUDE_KEY%"
    echo Claude API Key set successfully!
)

echo.
echo Setup complete! Restart your terminal for changes to take effect.
pause
```

### Linux/Mac (setup_ai_keys.sh):
```bash
#!/bin/bash
echo "Setting up AI API Keys for NyaySetu..."
echo

echo "Enter your Google Gemini API Key (or press Enter to skip):"
read -r GEMINI_KEY
if [ ! -z "$GEMINI_KEY" ]; then
    echo "export GEMINI_API_KEY=\"$GEMINI_KEY\"" >> ~/.bashrc
    echo "Gemini API Key set successfully!"
fi

echo
echo "Enter your OpenAI API Key (or press Enter to skip):"
read -r OPENAI_KEY
if [ ! -z "$OPENAI_KEY" ]; then
    echo "export OPENAI_API_KEY=\"$OPENAI_KEY\"" >> ~/.bashrc
    echo "OpenAI API Key set successfully!"
fi

echo
echo "Enter your Claude API Key (or press Enter to skip):"
read -r CLAUDE_KEY
if [ ! -z "$CLAUDE_KEY" ]; then
    echo "export CLAUDE_API_KEY=\"$CLAUDE_KEY\"" >> ~/.bashrc
    echo "Claude API Key set successfully!"
fi

echo
echo "Setup complete! Run 'source ~/.bashrc' or restart your terminal."
```

## Testing Your Setup

### Step 1: Start the Server
```bash
python app.py
```

### Step 2: Test with curl
```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test_token" \
  -d '{"question": "What are my rights as a tenant?", "language": "en"}'
```

### Step 3: Check Response
Look for these indicators in the response:
- `"source": "gemini_ai"` - Using Google Gemini
- `"source": "openai_ai"` - Using OpenAI GPT
- `"source": "claude_ai"` - Using Anthropic Claude
- `"source": "fallback"` - Using enhanced local model

## Priority Order

The system tries AI models in this order:
1. **Local Grok-1** (if checkpoints available)
2. **Google Gemini** (free tier)
3. **OpenAI GPT-3.5** (free tier)
4. **Enhanced Local Model** (fallback)

## Troubleshooting

### Common Issues:

1. **"API key not set"**
   - Check environment variable is set correctly
   - Restart terminal after setting variables

2. **"API error"**
   - Verify API key is correct
   - Check internet connection
   - Ensure you have credits/quota

3. **"Model not available"**
   - Install required packages: `pip install google-generativeai openai`

### Testing Individual APIs:

#### Test Gemini:
```python
import google.generativeai as genai
genai.configure(api_key='your_key')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello')
print(response.text)
```

#### Test OpenAI:
```python
import openai
openai.api_key = 'your_key'
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

## Cost Comparison

| Service | Free Tier | Cost After Free |
|---------|-----------|-----------------|
| **Google Gemini** | 60 req/min, 15M chars/month | $0.00025/1K chars |
| **OpenAI GPT-3.5** | $5 credit | $0.002/1K tokens |
| **Anthropic Claude** | $5 credit | $0.0008/1K tokens |

## Recommendations

### For Development:
- **Use Gemini** - Most generous free tier
- **No credit card required**
- **Excellent performance**

### For Production:
- **Start with Gemini** - Best value
- **Add OpenAI as backup**
- **Monitor usage**

### For High Volume:
- **Use local model** - No API costs
- **Add AI models for complex queries**
- **Implement caching**

## Next Steps

1. **Choose your preferred AI model**
2. **Get API key** from the provider
3. **Set environment variable**
4. **Test the integration**
5. **Monitor usage and costs**

## Support

If you encounter issues:
1. Check the error messages in server logs
2. Verify API keys are set correctly
3. Test individual APIs
4. Check provider's documentation
5. Ensure you have internet connectivity
