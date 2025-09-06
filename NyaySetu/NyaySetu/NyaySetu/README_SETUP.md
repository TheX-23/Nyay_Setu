# NyaySetu Legal AI - Complete Setup Guide

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Run the complete setup script:**

   ```bash
   start_nyaysetu_complete.bat
   ```

   This will automatically:
   - Set up Python virtual environment
   - Install all dependencies
   - Start all three services (Backend, Lingosathi AI, Frontend)

### Option 2: Manual Setup

#### Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

#### Step 1: Setup Environment

```bash
# Run the environment setup
setup_environment.bat

# Edit the .env file with your Gmail credentials
# File location: NyaySetu/backend/.env
```

#### Step 2: Backend Setup

```bash
cd NyaySetu/backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### Step 3: Frontend Setup

```bash
cd NyaySetu/frontend
npm install
```

#### Step 4: Start Services

**Terminal 1 - Main Backend:**

```bash
cd NyaySetu/backend
venv\Scripts\activate.bat
python app.py
```

**Terminal 2 - Lingosathi AI:**

```bash
cd NyaySetu/backend/lingosathi-ai-main
..\venv\Scripts\activate.bat
python app.py
```

**Terminal 3 - Frontend:**

```bash
cd NyaySetu/frontend
npm start
```

## 📧 Email Configuration

### Gmail Setup (Required for Email Verification)

1. **Enable 2-Factor Authentication:**
   - Go to your Google Account settings
   - Security → 2-Step Verification → Turn on

2. **Generate App Password:**
   - Google Account → Security → App passwords
   - Select "Mail" and generate password
   - Copy the 16-character password

3. **Update Environment File:**

   ```env
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=your-16-character-app-password
   ```

## 🌐 Service URLs

- **Frontend:** <http://localhost:3000>
- **Backend API:** <http://localhost:5000>  
- **Lingosathi AI:** <http://localhost:10000>

## 🎯 Features

### ✅ Completed Features

- **Email Authentication System**
  - User registration with email verification
  - Secure login with JWT tokens
  - Password hashing with Werkzeug

- **Multi-Language Legal AI**
  - English, Hindi, Marathi support
  - Lingosathi AI integration
  - Local legal model fallback

- **Modern Frontend**
  - React-based responsive UI
  - Authentication flow
  - Legal chat interface
  - Multi-language support

- **Backend API**
  - RESTful API design
  - Database integration (SQLite)
  - Form generation and PDF export
  - Chat history tracking

### 🔧 System Architecture

```
Frontend (React) → Backend API (Flask) → Lingosathi AI (Flask)
                                     ↓
                              SQLite Database
```

## 📁 Project Structure

```
NyaySetu/
├── NyaySetu/
│   ├── backend/                 # Main Backend API
│   │   ├── models/             # AI Models
│   │   │   └── legal_chat_model.py
│   │   ├── utils/              # Utility functions
│   │   │   ├── auth.py         # Email authentication
│   │   │   ├── db.py           # Database operations
│   │   │   └── form_generator.py
│   │   ├── lingosathi-ai-main/ # AI Service
│   │   │   └── app.py
│   │   ├── app.py              # Main Flask app
│   │   └── requirements.txt
│   └── frontend/               # React Frontend
│       ├── src/
│       │   ├── components/
│       │   │   └── LegalChat.js
│       │   ├── App.js
│       │   └── index.js
│       ├── public/
│       └── package.json
├── start_nyaysetu_complete.bat # Complete setup script
├── setup_environment.bat      # Environment setup
└── README_SETUP.md            # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors:**

   ```bash
   # Make sure virtual environment is activated
   cd NyaySetu/backend
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

2. **Frontend won't start:**

   ```bash
   cd NyaySetu/frontend
   npm install
   npm start
   ```

3. **Email not sending:**
   - Check Gmail app password is correct
   - Ensure 2FA is enabled on Gmail
   - Verify SMTP settings in .env file

4. **Database errors:**
   - Delete `nyaysetu.db` file and restart backend
   - Database will be recreated automatically

### Development Tips

1. **View API documentation:**
   - Visit <http://localhost:5000> for API endpoints

2. **Test email verification:**
   - Check backend logs for verification links
   - Links are exposed in development mode

3. **Monitor services:**
   - Each service runs in separate terminal window
   - Check logs for errors and debugging info

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with Werkzeug
- Email verification required
- CORS enabled for frontend integration
- Environment variable configuration

## 🌍 Multi-Language Support

- **English:** Full legal advice
- **Hindi:** हिंदी में कानूनी सलाह  
- **Marathi:** मराठी मध्ये कायदेशीर सल्ला
- **Auto-translation:** Using Google Translate API

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are installed
3. Verify environment configuration
4. Check service logs for specific errors

---

**🎉 Your NyaySetu Legal AI system is now ready to use!**
