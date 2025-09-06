import os
from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle legal chat requests from NyaySetu"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        user_message = data.get('message', '')
        language = data.get('lang', 'en')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Generate legal advice based on the question
        legal_advice = generate_legal_advice(user_message, language)
        
        # Translate if needed
        if language != 'en':
            try:
                legal_advice = GoogleTranslator(source='en', target=language).translate(legal_advice) # type: ignore
            except Exception as e:
                logger.warning(f"Translation failed: {e}")
                # Return in English if translation fails
                pass
        
        return jsonify({
            'reply': legal_advice,
            'original_question': user_message,
            'language': language,
            'source': 'lingosathi_ai'
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def generate_legal_advice(question: str, language: str = 'en') -> str:
    """Generate legal advice based on the question"""
    question_lower = question.lower()
    
    # Basic legal advice patterns
    if any(word in question_lower for word in ['property', 'land', 'house', 'real estate']):
        return "For property-related legal issues, I recommend consulting a property lawyer. Document all transactions and keep records of payments and agreements."
    
    elif any(word in question_lower for word in ['criminal', 'crime', 'theft', 'assault', 'police']):
        return "For criminal matters, seek immediate legal counsel. Do not make statements without a lawyer present. Document all incidents and preserve evidence."
    
    elif any(word in question_lower for word in ['marriage', 'divorce', 'custody', 'family']):
        return "Family law matters require specialized legal expertise. Consider mediation for amicable resolutions. Document all communications and agreements."
    
    elif any(word in question_lower for word in ['employment', 'job', 'salary', 'termination']):
        return "Employment law issues should be addressed with an employment lawyer. Keep records of all workplace communications and document any incidents."
    
    elif any(word in question_lower for word in ['consumer', 'refund', 'warranty', 'complaint']):
        return "Consumer protection laws can help resolve your issue. Document all communications, keep receipts, and file complaints with consumer forums if needed."
    
    else:
        return "Based on your question, I recommend consulting with a qualified lawyer for specific legal advice. Document all relevant information and act promptly as legal matters often have time limits."

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'LingoSathi Legal AI'})

@app.route('/', methods=['GET'])
def home():
    return 'LingoSathi Legal AI backend running!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
