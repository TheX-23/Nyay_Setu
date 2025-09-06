# NyaySetu - Legal Aid Platform

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask 2.3.3](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Frontend](https://img.shields.io/badge/HTML5-CSS3-JavaScript-orange.svg)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Overview

NyaySetu (Justice Bridge) is an innovative legal aid platform that bridges the gap between citizens and legal knowledge using artificial intelligence. The platform provides multi-language legal advice, automated form generation, and comprehensive legal resources to empower citizens with legal information.

## ✨ Features

### 🤖 AI Legal Assistant

- **Multi-language Support**: English, Hindi, Odia, Bengali, Tamil, and Telugu
- **Intelligent Legal Advice**: AI-powered responses based on legal topic classification
- **Real-time Chat Interface**: Interactive chat experience with legal experts
- **Topic Classification**: Automatically categorizes legal issues (Property, Criminal, Family, Employment, Consumer, Civil)

### 📝 Legal Form Generator

- **Multiple Form Types**: FIR, RTI, Complaint, and Appeal forms
- **Dynamic Field Generation**: Context-aware form fields based on form type
- **Professional Templates**: Structured, legally compliant form templates
- **Export Ready**: Generated forms ready for official submission

### 📚 Legal Resources

- **Educational Content**: Fundamental legal rights and protections
- **Legal Aid Information**: Free legal assistance and support services
- **Time Limits Guide**: Important deadlines for legal actions
- **Emergency Contacts**: Legal helpline numbers and contacts

### 🎨 Modern User Interface

- **Responsive Design**: Works seamlessly on all devices
- **Beautiful Animations**: Smooth transitions and interactive elements
- **Professional Styling**: Modern, clean interface with glassmorphism effects
- **Accessibility**: User-friendly design for all users

## 🚀 Technology Stack

### Backend

- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Web framework for API development
- **Flask-CORS**: Cross-origin resource sharing support
- **Transformers**: AI model integration capabilities
- **PyTorch**: Machine learning framework

### Frontend

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API integration
- **Font Awesome**: Icon library
- **Google Fonts**: Typography (Inter font family)

## 📋 Prerequisites

Before running this project, ensure you have:

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Git** (for cloning the repository)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nyaysetu.git
cd nyaysetu
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# No build process required - static files ready to use
# Open index.html in your browser or serve with a local server
```

### 4. Start the Application

#### Option A: Using the Batch File (Windows)

```bash
# From the project root directory
start_nyaysetu.bat
```

#### Option B: Manual Start

```bash
# Terminal 1: Start Backend
cd backend
python app.py

# Terminal 2: Serve Frontend (optional)
cd frontend
python -m http.server 8000
```

### 5. Access the Application

- **Backend API**: <http://127.0.0.1:5000>
- **Frontend**: <http://localhost:8000> (if using Python server) or open `frontend/index.html` directly

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
PORT=5000
DEBUG=True
```

### API Configuration

The frontend is configured to connect to `http://127.0.0.1:5000` by default. To change this:

1. Edit `frontend/app.js`
2. Update the `API_BASE_URL` constant:

```javascript
const API_BASE_URL = 'http://your-api-url:port';
```

## 📖 Usage Guide

### Getting Legal Advice

1. **Select Language**: Choose your preferred language from the dropdown
2. **Ask Question**: Type your legal question in the chat input
3. **Get Response**: Receive AI-powered legal advice and recommendations
4. **View History**: Access your previous conversations

### Generating Legal Forms

1. **Choose Form Type**: Select from FIR, RTI, Complaint, or Appeal
2. **Fill Fields**: Complete the relevant form fields
3. **Generate Form**: Click "Generate Form" to create the document
4. **Download/Print**: Use the generated form for official purposes

### Accessing Resources

1. **Navigate to Resources Tab**: Click on the Resources tab
2. **Browse Categories**: Explore different legal resource categories
3. **Get Information**: Access helpful legal information and contacts

## 🏗️ Project Structure

```text
NyaySetu/
├── backend/                 # Backend API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── models/             # AI models and business logic
│   │   └── legal_chat_model.py
│   └── utils/              # Utility functions
│       └── form_generator.py
├── frontend/               # Frontend web application
│   ├── index.html         # Main HTML file
│   ├── style.css          # CSS styles and animations
│   ├── app.js             # JavaScript functionality
│   └── test.html          # Test page
├── offline_app/            # Offline C++ application
│   └── offline_legal_app.cpp
├── start_nyaysetu.bat      # Windows startup script
└── README.md               # Project documentation
```

## 🔌 API Endpoints

### Core Endpoints

- `POST /chat` - Get legal advice
- `POST /generate_form` - Generate legal forms
- `GET /health` - Health check
- `GET /languages` - Get supported languages
- `GET /form_types` - Get available form types

### Request/Response Examples

#### Chat Endpoint

```json
POST /chat
{
  "question": "What are my rights as a tenant?",
  "language": "en"
}

Response:
{
  "answer": "Hello! I'm here to help you with legal advice...",
  "question": "What are my rights as a tenant?",
  "language": "en",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Form Generation Endpoint

```json
POST /generate_form
{
  "form_type": "FIR",
  "responses": {
    "name": "John Doe",
    "address": "123 Main St",
    "description": "Theft incident"
  }
}

Response:
{
  "form": "Generated FIR form content...",
  "form_type": "FIR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### Frontend Testing

Open `frontend/test.html` in your browser for basic functionality testing.

### API Testing

Use tools like Postman or curl to test API endpoints:

```bash
# Test health endpoint
curl http://127.0.0.1:5000/health

# Test chat endpoint
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Test question", "language": "en"}'
```

## 🚀 Deployment

### Production Deployment

1. **Backend**: Use Gunicorn with a production WSGI server
2. **Frontend**: Deploy to CDN or static hosting service
3. **Environment**: Set `FLASK_ENV=production`
4. **Security**: Enable HTTPS and configure CORS properly

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Legal Experts**: For guidance on legal content and form structures
- **Open Source Community**: For the amazing tools and libraries used
- **Contributors**: Everyone who has contributed to this project

## 📞 Support

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/yourusername/nyaysetu/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/yourusername/nyaysetu/discussions)
- **Email**: Contact us at <support@nyaysetu.com>

## 🔮 Roadmap

### Version 2.0 (Q2 2024)

- [ ] Advanced AI model integration
- [ ] Document analysis and review
- [ ] Legal case tracking system
- [ ] Mobile application

### Version 3.0 (Q4 2024)

- [ ] Blockchain-based document verification
- [ ] Multi-language voice support
- [ ] Integration with legal databases
- [ ] Advanced analytics dashboard

---

### Empowering citizens with legal knowledge through technology

Made with ❤️ for justice and accessibility
