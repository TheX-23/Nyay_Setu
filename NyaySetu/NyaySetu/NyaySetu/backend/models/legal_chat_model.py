import re
from typing import Dict, List, Optional
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import translation library
try:
    from deep_translator import GoogleTranslator
    _translator_available = True
except ImportError:
    _translator_available = False

# Import Gemini library
try:
    import google.generativeai as genai
    _gemini_available = True
except ImportError:
    _gemini_available = False

class LegalAdviceGenerator:
    """Advanced legal advice generator with multi-language support using deep-translator"""
    
    def __init__(self):
        # Language mapping for translation
        self.language_mapping = {
            'en': 'en',
            'hi': 'hi',  # Hindi
            'or': 'or',  # Odia
            'bn': 'bn',  # Bengali
            'ta': 'ta',  # Tamil
            'te': 'te',  # Telugu
            'mr': 'mr',  # Marathi
            'gu': 'gu',  # Gujarati
            'kn': 'kn',  # Kannada
            'ml': 'ml',  # Malayalam
            'pa': 'pa',  # Punjabi
        }
        
        # Legal context prompts for AI models
        self.legal_prompts = {
            'en': """You are a legal AI assistant specializing in Indian law. Provide clear, practical legal advice based on Indian legal framework. Focus on:
1. Relevant Indian laws and regulations
2. Practical steps the person can take
3. Available legal remedies and procedures
4. Important deadlines and time limits
5. When to consult a lawyer
6. Available legal aid resources

Keep responses helpful, accurate, and actionable. If you're unsure about specific legal details, recommend consulting a qualified lawyer.

Question: {question}

Provide legal advice:""",
            
            'hi': """आप भारतीय कानून में विशेषज्ञता रखने वाले कानूनी AI सहायक हैं। भारतीय कानूनी ढांचे के आधार पर स्पष्ट, व्यावहारिक कानूनी सलाह दें। इन पर ध्यान दें:
1. प्रासंगिक भारतीय कानून और नियम
2. व्यक्ति द्वारा उठाए जा सकने वाले व्यावहारिक कदम
3. उपलब्ध कानूनी उपचार और प्रक्रियाएं
4. महत्वपूर्ण समय सीमाएं
5. वकील से कब सलाह लें
6. उपलब्ध कानूनी सहायता संसाधन

प्रतिक्रियाएं सहायक, सटीक और कार्रवाई योग्य रखें। यदि आप विशिष्ट कानूनी विवरणों के बारे में अनिश्चित हैं, तो योग्य वकील से सलाह लेने की सिफारिश करें।

प्रश्न: {question}

कानूनी सलाह दें:""",
            
            'or': """ଆପଣ ଭାରତୀୟ ଆଇନରେ ବିଶେଷଜ୍ଞତା ଥିବା ଆଇନଗତ AI ସହାୟକ ଅଟନ୍ତି। ଭାରତୀୟ ଆଇନଗତ ଢାଞ୍ଚା ଉପରେ ଆଧାର କରି ସ୍ପଷ୍ଟ, ବ୍ୟବହାରିକ ଆଇନଗତ ପରାମର୍ଶ ଦିଅନ୍ତୁ। ଏହା ଉପରେ ଧ୍ୟାନ ଦିଅନ୍ତୁ:
1. ପ୍ରାସଙ୍ଗିକ ଭାରତୀୟ ଆଇନ ଏବଂ ନିୟମ
2. ବ୍ୟକ୍ତି ଦ୍ୱାରା ନିଆଯାଇପାରିବା ବ୍ୟବହାରିକ ପଦକ୍ଷେପ
3. ଉପଲବ୍ଧ ଆଇନଗତ ପ୍ରତିକାର ଏବଂ ପ୍ରକ୍ରିୟା
4. ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ସମୟ ସୀମା
5. କେବେ ବକୀଳଙ୍କ ସହ ପରାମର୍ଶ ନିଅନ୍ତୁ
6. ଉପଲବ୍ଧ ଆଇନଗତ ସହାୟତା ସମ୍ବଳ

ପ୍ରତିକ୍ରିୟା ସହାୟକ, ସଠିକ ଏବଂ କାର୍ଯ୍ୟକାରୀ ରଖନ୍ତୁ। ଯଦି ଆପଣ ବିଶେଷ ଆଇନଗତ ବିବରଣୀ ବିଷୟରେ ଅନିଶ୍ଚିତ ଅଟନ୍ତି, ତେବେ ଯୋଗ୍ୟ ବକୀଳଙ୍କ ସହ ପରାମର୍ଶ ନେବାକୁ ପରାମର୍ଶ ଦିଅନ୍ତୁ।

ପ୍ରଶ୍ନ: {question}

ଆଇନଗତ ପରାମର୍ଶ ଦିଅନ୍ତୁ:"""
        }
        
        # Fallback responses for when all AI models are not available
        self.fallback_responses = {
            'en': 'I apologize, but I\'m currently unable to provide detailed legal advice. Please consult a qualified lawyer for your specific situation.',
            'hi': 'मैं क्षमा चाहता हूं, लेकिन मैं वर्तमान में विस्तृत कानूनी सलाह प्रदान करने में असमर्थ हूं। कृपया अपनी विशिष्ट स्थिति के लिए योग्य वकील से सलाह लें।',
            'or': 'ମୁଁ କ୍ଷମା ଚାହୁଁଛି, କିନ୍ତୁ ମୁଁ ବର୍ତ୍ତମାନ ବିସ୍ତୃତ ଆଇନଗତ ପରାମର୍ଶ ପ୍ରଦାନ କରିପାରୁ ନାହିଁ। ଦୟାକରି ଆପଣଙ୍କ ବିଶେଷ ପରିସ୍ଥିତି ପାଇଁ ଯୋଗ୍ୟ ବକୀଳଙ୍କ ସହ ପରାମର୍ଶ ନିଅନ୍ତୁ।'
        }
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language using deep-translator"""
        if not _translator_available:
            return text
        
        if target_language == 'en':
            return text
        
        try:
            translator = GoogleTranslator(source='en', target=target_language)
            translated = translator.translate(text)
            return translated
        except Exception as e:
            # If translation fails, return original text
            print(f"Translation error: {str(e)}")
            return text
    
    def get_legal_prompt(self, question: str, language: str = 'en') -> str:
        """Get appropriate legal prompt for the language"""
        if language in self.legal_prompts:
            return self.legal_prompts[language].format(question=question)
        else:
            # Default to English prompt
            return self.legal_prompts['en'].format(question=question)
    
    def get_fallback_response(self, language: str = 'en') -> str:
        """Get fallback response when all AI models are not available"""
        return self.fallback_responses.get(language, self.fallback_responses['en'])

# Global instance
legal_advisor = LegalAdviceGenerator()


def get_gemini_answer(question: str) -> str:
    """Get answer from Google Gemini API"""
    if not _gemini_available:
        return "Gemini not available. Install: pip install google-generativeai"
    
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return "Gemini API key not set. Set GEMINI_API_KEY environment variable."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Create legal context prompt
        legal_prompt = legal_advisor.get_legal_prompt(question, 'en')
        
        response = model.generate_content(legal_prompt)
        return response.text
        
    except Exception as e:
        return f"Gemini API error: {str(e)}"

def get_legal_advice(question: str, language: str = 'en') -> str:
    """Main function to get legal advice with Gemini only (no Grok)"""
    if not question or not question.strip():
        return "Please provide a valid legal question."
    
    try:
        # Use Gemini only
        gemini_answer = get_gemini_answer(question.strip())
        
        # If Gemini failed, return fallback
        if gemini_answer.startswith("Gemini API error") or gemini_answer.startswith("Gemini not available") or gemini_answer.startswith("Gemini API key not set"):
            return legal_advisor.get_fallback_response(language)
        
        # Translate if needed
        if language != 'en':
            translated_answer = legal_advisor.translate_text(gemini_answer, language)
            return translated_answer
        
        return gemini_answer
        
    except Exception:
        # Fallback to simple response
        return legal_advisor.get_fallback_response(language)