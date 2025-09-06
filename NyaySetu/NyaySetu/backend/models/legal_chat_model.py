import re
import google.generativeai as genai
import os
from typing import Dict, List, Optional

# ✅ Correct API key setup (using environment variable)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# ✅ Explicitly load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Test (you can remove this later)
try:
    response = model.generate_content("Hello, how may I help you?")
    print(response.text)
except Exception as e:
    print("Gemini error:", e)
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: GEMINI_API_KEY' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]


class LegalAdviceGenerator:
    """Advanced legal advice generator with multi-language support"""

    def __init__(self):
        self.legal_topics = {
            'property': ['property', 'land', 'house', 'real estate', 'ownership', 'tenant', 'landlord'],
            'criminal': ['crime', 'theft', 'assault', 'fraud', 'harassment', 'cybercrime', 'police'],
            'family': ['marriage', 'divorce', 'custody', 'maintenance', 'inheritance', 'adoption'],
            'employment': ['job', 'salary', 'termination', 'discrimination', 'harassment', 'contract'],
            'consumer': ['refund', 'warranty', 'deficiency', 'service', 'product', 'complaint'],
            'civil': ['contract', 'agreement', 'breach', 'damages', 'compensation', 'suit']
        }

        self.language_responses = {
            'en': {
                'greeting': "Hello! I'm here to help you with legal advice.",
                'property': "For property-related legal issues, you may need to consult a property lawyer.",
                'criminal': "For criminal matters, it's crucial to seek immediate legal counsel.",
                'family': "Family law matters require specialized legal expertise.",
                'employment': "Employment law issues should be addressed with an employment lawyer.",
                'consumer': "Consumer protection laws can help resolve your issue.",
                'civil': "Civil law matters may require legal representation.",
                'general': "Based on your question, I recommend consulting with a qualified lawyer."
            },
            # ✅ keep the rest of your multilingual dictionary as-is...
        }
