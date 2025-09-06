# Grok-1 Setup Guide for NyaySetu

## Overview
This guide explains how to set up Grok-1 AI model with NyaySetu for enhanced legal advice.

## Option 1: Local Grok-1 Model (Advanced)

### Prerequisites
- **Large storage space**: ~100GB+ for model checkpoints
- **High RAM**: 32GB+ recommended
- **GPU**: NVIDIA GPU with 24GB+ VRAM recommended
- **Git LFS**: For downloading large files

### Steps

1. **Install Git LFS**
   ```bash
   git lfs install
   ```

2. **Clone Grok-1 Repository**
   ```bash
   cd grok-1-main/grok-1-main
   git clone https://huggingface.co/xai-org/grok-1
   ```

3. **Download Model Files**
   ```bash
   cd grok-1
   git lfs pull
   ```

4. **Move Checkpoints**
   ```bash
   # Copy model files to checkpoints directory
   cp -r * ../checkpoints/
   ```

### Issues with Local Setup
- **Large file size**: Model is ~100GB
- **Hardware requirements**: Needs powerful GPU
- **License restrictions**: Requires approval from xAI
- **Complex setup**: Many dependencies

## Option 2: Grok-1 API (Recommended)

### Available API Providers

1. **xAI Grok API** (Official)
   - Visit: https://console.x.ai/
   - Sign up for API access
   - Get API key

2. **Third-party Providers**
   - **Together AI**: https://together.ai/
   - **Anthropic Claude**: https://console.anthropic.com/
   - **OpenAI GPT-4**: https://platform.openai.com/

### Setup Steps

1. **Get API Key**
   - Sign up with your chosen provider
   - Generate API key

2. **Set Environment Variable**
   ```bash
   # Windows
   set GROK_API_KEY=your_api_key_here
   
   # Linux/Mac
   export GROK_API_KEY=your_api_key_here
   ```

3. **Update API Configuration**
   Edit `models/legal_chat_model.py` and update the API endpoint:
   ```python
   # Replace with your provider's API endpoint
   api_url = "https://api.together.xyz/v1/chat/completions"
   ```

## Option 3: Alternative AI Models (Easiest)

### Use Claude or GPT-4 Instead

1. **Claude API Setup**
   ```bash
   export CLAUDE_API_KEY=your_claude_key
   ```

2. **GPT-4 API Setup**
   ```bash
   export OPENAI_API_KEY=your_openai_key
   ```

3. **Update Code**
   Replace Grok-1 calls with Claude/GPT-4 API calls

## Option 4: Enhanced Local Model (Current)

### Current Implementation
- Uses enhanced local legal knowledge base
- Multi-language support via translation
- No external dependencies
- Works immediately

### Benefits
- ✅ No API costs
- ✅ No internet dependency
- ✅ Privacy-focused
- ✅ Instant responses
- ✅ Multi-language support

## Testing Your Setup

1. **Start the server**
   ```bash
   python app.py
   ```

2. **Test with curl**
   ```bash
   curl -X POST http://127.0.0.1:5000/chat \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer test_token" \
     -d '{"question": "What are my rights as a tenant?", "language": "en"}'
   ```

3. **Check response**
   - Look for `"source": "grok1_ai"` in response
   - Check `"model_status"` field

## Troubleshooting

### Common Issues

1. **"Grok-1 model not available"**
   - Check if checkpoints are downloaded
   - Verify file paths
   - Check hardware requirements

2. **"API error"**
   - Verify API key is set
   - Check API endpoint URL
   - Test API connectivity

3. **"Translation failed"**
   - Check internet connection
   - Verify language codes
   - Install deep-translator: `pip install deep-translator`

### Fallback Behavior
- If Grok-1 fails → Uses enhanced local model
- If translation fails → Returns English response
- If everything fails → Shows helpful error message

## Recommendations

### For Development/Testing
- **Use Option 4** (Enhanced Local Model)
- Fast, reliable, no external dependencies
- Good for testing and development

### For Production
- **Use Option 2** (API-based)
- Better AI responses
- Scalable and maintainable
- Cost-effective for low usage

### For High-Volume Usage
- **Use Option 1** (Local Model)
- No API costs
- No rate limits
- Complete privacy

## Next Steps

1. **Choose your preferred option**
2. **Follow the setup steps**
3. **Test the integration**
4. **Monitor performance**
5. **Optimize as needed**

## Support

If you encounter issues:
1. Check the error messages in server logs
2. Verify all dependencies are installed
3. Test API connectivity
4. Review hardware requirements
5. Check file permissions and paths
