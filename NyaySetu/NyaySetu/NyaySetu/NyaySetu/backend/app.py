from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS
from models.legal_chat_model import get_legal_advice
from utils.form_generator import generate_form
from utils.db import (
    init_db,
    insert_chat,
    insert_form,
    fetch_all_chats,
    fetch_all_forms,
    fetch_chats_filtered,
    fetch_forms_filtered,
    create_user,
    get_user_by_email,
    get_user_by_verification_token,
    set_user_verified,
)
from utils.auth import send_verification_email
import logging
import os
import time
import json
import secrets
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Optional deps
try:
    import requests
except ImportError:
    requests = None

try:
    from werkzeug.security import check_password_hash as _check_password_hash, generate_password_hash as _generate_password_hash
except Exception:
    _check_password_hash = None
    _generate_password_hash = None

try:
    import jwt
except Exception:
    jwt = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize DB
init_db()

def generate_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)

def get_current_timestamp() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()

# Password helpers
def hash_password(password: str) -> str:
    if _generate_password_hash:
        return _generate_password_hash(password)
    raise RuntimeError("werkzeug.security.generate_password_hash not available. Install Werkzeug.")

def verify_password(password: str, password_hash: str) -> bool:
    if _check_password_hash:
        return _check_password_hash(password_hash, password)
    raise RuntimeError("werkzeug.security.check_password_hash not available. Install Werkzeug.")

# JWT helpers
def create_jwt(payload: dict, expires_minutes: int = 60) -> str:
    if jwt is None:
        raise RuntimeError("PyJWT not installed")
    import datetime
    secret = os.environ.get('JWT_SECRET', 'secret')
    p = payload.copy()
    p['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    token = jwt.encode(p, secret, algorithm='HS256') # type: ignore
    # PyJWT returns bytes in some versions
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def decode_jwt(token: str) -> dict | None:
    if jwt is None:
        raise RuntimeError("PyJWT not installed")
    secret = os.environ.get('JWT_SECRET', 'secret')
    try:
        return jwt.decode(token, secret, algorithms=['HS256']) # type: ignore
    except Exception as e:
        logger.debug(f"JWT decode failed: {e}")
        return None

def get_current_user():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ', 1)[1]
    try:
        return decode_jwt(token)
    except Exception:
        return None

def call_legal_ai_remote(question: str, language: str):
    """Call the lingosathi AI service for legal advice"""
    url = os.environ.get('LEGAL_AI_URL', 'http://localhost:10000/chat')
    if not url:
        logger.debug("LEGAL_AI_URL not configured; skipping remote call")
        return None
    if requests is None:
        logger.error("requests library not available for remote Legal AI calls")
        return None
    
    # Prepare payload for lingosathi AI
    payload = {
        'message': question,
        'lang': language
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        # Extract response from lingosathi AI
        if isinstance(data, dict):
            if 'reply' in data and data['reply']:
                return data['reply']
            elif 'answer' in data and data['answer']:
                return data['answer']
            elif 'response' in data and data['response']:
                return data['response']
        
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Lingosathi AI call failed: {e}")
        return None

@app.route('/', methods=['GET'])
def root():
    html = (
        "<html><head><title>NyaySetu API</title>"
        "<style>body{font-family:Segoe UI,Tahoma,Arial,sans-serif;padding:24px;line-height:1.6;}"
        "code{background:#f5f5f5;padding:2px 6px;border-radius:4px;}"
        ".box{max-width:840px;margin:auto} .endpoint{background:#fafafa;border:1px solid #eee;padding:12px;border-radius:8px;margin:8px 0}"
        "</style></head><body><div class='box'>"
        "<h2>NyaySetu Legal Aid API</h2>"
        "<p>Status: healthy. See <code>/health</code>.</p>"
        "<h3>Auth</h3>"
        "<div class='endpoint'><b>POST</b> <code>/auth/register</code> { email, password }</div>"
        "<div class='endpoint'><b>GET</b> <code>/auth/verify?token=...</code></div>"
        "<div class='endpoint'><b>POST</b> <code>/auth/login</code> { email, password }</div>"
        "<h3>Data</h3>"
        "<div class='endpoint'><b>POST</b> <code>/chat</code> (Bearer token required)</div>"
        "<div class='endpoint'><b>POST</b> <code>/generate_form</code> (Bearer token required)</div>"
        "<div class='endpoint'><b>GET</b> <code>/data/chats</code> ?start&end&language&q</div>"
        "<div class='endpoint'><b>GET</b> <code>/data/forms</code> ?start&end&form_type&q</div>"
        "</div></body></html>"
    )
    return make_response(html, 200)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'NyaySetu Legal Aid API'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        question = (data.get('question') or '').strip()
        language = data.get('language') or 'en'
        if not question:
            return jsonify({'error': 'Question is required'}), 400

        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        answer = None
        
        # First try to get answer from lingosathi AI
        try:
            answer = call_legal_ai_remote(question, language)
            if answer:
                logger.info("Got answer from lingosathi AI")
        except Exception as remote_err:
            logger.warning(f"Lingosathi AI failed: {remote_err}")

        # Fallback to local legal model if remote AI fails
        if not answer:
            try:
                answer = get_legal_advice(question, language)
                logger.info("Got answer from local legal model")
            except Exception as local_err:
                logger.warning(f"Local legal model failed: {local_err}")

        if not answer:
            return jsonify({'error': 'No answer available from Legal AI services'}), 502

        timestamp = get_current_timestamp()
        try:
            insert_chat(question=question, answer=answer, language=language, timestamp=timestamp)
        except Exception as db_err:
            logger.error(f"Failed to persist chat: {db_err}")

        return jsonify({
            'answer': answer, 
            'question': question, 
            'language': language, 
            'timestamp': timestamp,
            'source': 'lingosathi_ai' if 'lingosathi' in str(answer).lower() else 'local_model'
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/generate_form', methods=['POST'])
def form():
    try:
        data = request.get_json() or {}
        form_type = data.get('form_type') or 'FIR'
        responses = data.get('responses') or {}
        if not form_type:
            return jsonify({'error': 'Form type is required'}), 400

        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        form_text = generate_form(form_type, responses)
        timestamp = get_current_timestamp()
        try:
            insert_form(form_type=form_type, form_text=form_text, responses=responses, timestamp=timestamp)
        except Exception as db_err:
            logger.error(f"Failed to persist form: {db_err}")

        return jsonify({'form': form_text, 'form_type': form_type, 'timestamp': timestamp})
    except Exception as e:
        logger.error(f"Error in form generation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/languages', methods=['GET'])
def get_supported_languages():
    languages = [
        {'code': 'en', 'name': 'English', 'native': 'English'},
        {'code': 'hi', 'name': 'Hindi', 'native': 'हिंदी'},
        {'code': 'mr', 'name': 'Marathi', 'native': 'मराठी'},
    ]
    return jsonify({'languages': languages})

@app.route('/form_types', methods=['GET'])
def get_form_types():
    form_types = [
        {'code': 'FIR', 'name': 'First Information Report', 'description': 'Police complaint registration'},
        {'code': 'RTI', 'name': 'Right to Information', 'description': 'Information request application'},
        {'code': 'COMPLAINT', 'name': 'General Complaint', 'description': 'General grievance complaint'},
        {'code': 'APPEAL', 'name': 'Legal Appeal', 'description': 'Appeal application'},
    ]
    return jsonify({'form_types': form_types})

@app.route('/generate_form_pdf', methods=['POST'])
def generate_form_pdf():
    try:
        data = request.get_json() or {}
        form_type = data.get('form_type') or 'FIR'
        responses = data.get('responses') or {}

        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import mm
        except ImportError:
            return jsonify({'error': 'PDF generation requires reportlab'}), 500

        form_text = generate_form(form_type, responses)

        import io
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 15 * mm
        y = height - margin
        line_height = 12
        pdf.setTitle(f"{form_type} - NyaySetu")
        pdf.setFont("Helvetica", 10)

        for line in form_text.splitlines():
            if y < margin:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - margin
            while len(line) > 110:
                segment = line[:110]
                pdf.drawString(margin, y, segment)
                y -= line_height
                line = line[110:]
                if y < margin:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    y = height - margin
            pdf.drawString(margin, y, line)
            y -= line_height

        pdf.showPage()
        pdf.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()

        filename = f"{form_type}_NyaySetu.pdf"
        response = make_response(pdf_bytes)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', f'attachment; filename="{filename}"')
        return response
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return jsonify({'error': 'Failed to generate PDF'}), 500

@app.route('/data/chats', methods=['GET'])
def get_chats():
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        language = request.args.get('language')
        q = request.args.get('q')
        if any([start, end, language, q]):
            chats = fetch_chats_filtered(start=start, end=end, language=language, q=q)
        else:
            chats = fetch_all_chats()
        return jsonify({'chats': chats})
    except Exception as e:
        logger.error(f"Error fetching chats: {e}")
        return jsonify({'error': 'Failed to fetch chats'}), 500

@app.route('/data/forms', methods=['GET'])
def get_forms():
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        form_type = request.args.get('form_type')
        q = request.args.get('q')
        if any([start, end, form_type, q]):
            forms = fetch_forms_filtered(start=start, end=end, form_type=form_type, q=q)
        else:
            forms = fetch_all_forms()
        return jsonify({'forms': forms})
    except Exception as e:
        logger.error(f"Error fetching forms: {e}")
        return jsonify({'error': 'Failed to fetch forms'}), 500

# --- Auth endpoints ---
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json() or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        if get_user_by_email(email):
            return jsonify({'error': 'Email already registered'}), 400

        password_hash = hash_password(password)
        verification_token = generate_token()
        user_id = create_user(email=email, password_hash=password_hash, verification_token=verification_token, created_at=get_current_timestamp())

        base_url = os.environ.get('APP_BASE_URL', 'http://localhost:5000')
        verify_link = f"{base_url}/auth/verify?token={verification_token}"
        try:
            send_verification_email(email, verify_link)
        except Exception as e:
            logger.error(f"Email send failed: {e}")

        smtp_host = os.environ.get('SMTP_HOST')
        smtp_user = os.environ.get('SMTP_USER')
        smtp_pass = os.environ.get('SMTP_PASS')
        expose_flag = os.environ.get('EXPOSE_VERIFY_LINK', '0') == '1'
        smtp_configured = bool(smtp_host and smtp_user and smtp_pass)
        response_body = {'message': 'Registered successfully. Please check your email to verify.'}
        if expose_flag or not smtp_configured or 'localhost' in base_url or '127.0.0.1' in base_url:
            response_body['verify_link'] = verify_link

        return jsonify(response_body)
    except Exception as e:
        logger.error(f"Error in register: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/auth/verify', methods=['GET'])
def verify():
    try:
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'Missing token'}), 400
        user = get_user_by_verification_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 400
        if user.get('is_verified'):
            return jsonify({'message': 'Already verified'})
        set_user_verified(user_id=user['id'], verified_at=get_current_timestamp())
        return jsonify({'message': 'Email verified successfully'})
    except Exception as e:
        logger.error(f"Error in verify: {e}")
        return jsonify({'error': 'Verification failed'}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        if not user.get('is_verified'):
            return jsonify({'error': 'Email not verified'}), 403
        try:
            if not verify_password(password, user['password_hash']):
                return jsonify({'error': 'Invalid credentials'}), 401
        except Exception as e:
            logger.error(f"Password verify error: {e}")
            return jsonify({'error': 'Server configuration error'}), 500

        token = create_jwt({'sub': user['id'], 'email': email}, expires_minutes=60 * 24)
        return jsonify({'token': token, 'email': email})
    except Exception as e:
        logger.error(f"Error in login: {e}")
        return jsonify({'error': 'Login failed'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', '') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)