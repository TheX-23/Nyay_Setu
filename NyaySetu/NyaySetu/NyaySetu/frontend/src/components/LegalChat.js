import React, { useState, useEffect } from 'react';
import './LegalChat.css';

export default function LegalChat() {
  const [language, setLanguage] = useState('en');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [message, setMessage] = useState('');

  // Check if user is already authenticated
  useEffect(() => {
    const token = localStorage.getItem('nyaysetu_token');
    const email = localStorage.getItem('nyaysetu_email');
    if (token && email) {
      setIsAuthenticated(true);
      setUserEmail(email);
    }
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: loginEmail, password: loginPassword })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('nyaysetu_token', data.token);
        localStorage.setItem('nyaysetu_email', loginEmail);
        setIsAuthenticated(true);
        setUserEmail(loginEmail);
        setShowLogin(false);
        setMessage('Login successful!');
        setLoginEmail('');
        setLoginPassword('');
      } else {
        setMessage(data.error || 'Login failed');
      }
    } catch (error) {
      setMessage('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: registerEmail, password: registerPassword })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setMessage('Registration successful! Please check your email for verification.');
        setShowRegister(false);
        setRegisterEmail('');
        setRegisterPassword('');
      } else {
        setMessage(data.error || 'Registration failed');
      }
    } catch (error) {
      setMessage('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('nyaysetu_token');
    localStorage.removeItem('nyaysetu_email');
    setIsAuthenticated(false);
    setUserEmail('');
    setMessage('Logged out successfully');
  };

  const sendQuestion = async () => {
    if (!question.trim()) return;
    
    setIsLoading(true);
    try {
      const token = localStorage.getItem('nyaysetu_token');
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ question, language })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setAnswer(data.answer);
        setQuestion('');
      } else {
        setMessage(data.error || 'Failed to get answer');
      }
    } catch (error) {
      setMessage('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const supportedLanguages = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'hi', name: 'Hindi', native: 'हिंदी' },
    { code: 'mr', name: 'Marathi', native: 'मराठी' },
    { code: 'bn', name: 'Bengali', native: 'বাংলা' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు' }
  ];

  if (!isAuthenticated) {
    return (
      <div className="legal-chat-container">
        <div className="auth-container">
          <h2>Welcome to NyaySetu Legal AI</h2>
          <p>Get legal advice in multiple languages</p>
          
          {message && <div className="message">{message}</div>}
          
          <div className="auth-buttons">
            <button onClick={() => setShowLogin(true)} className="btn btn-primary">
              Login
            </button>
            <button onClick={() => setShowRegister(true)} className="btn btn-secondary">
              Register
            </button>
          </div>

          {showLogin && (
            <div className="auth-form">
              <h3>Login</h3>
              <form onSubmit={handleLogin}>
                <input
                  type="email"
                  placeholder="Email"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  required
                />
                <button type="submit" disabled={isLoading} className="btn btn-primary">
                  {isLoading ? 'Logging in...' : 'Login'}
                </button>
                <button type="button" onClick={() => setShowLogin(false)} className="btn btn-secondary">
                  Cancel
                </button>
              </form>
            </div>
          )}

          {showRegister && (
            <div className="auth-form">
              <h3>Register</h3>
              <form onSubmit={handleRegister}>
                <input
                  type="email"
                  placeholder="Email"
                  value={registerEmail}
                  onChange={(e) => setRegisterEmail(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={registerPassword}
                  onChange={(e) => setRegisterPassword(e.target.value)}
                  required
                />
                <button type="submit" disabled={isLoading} className="btn btn-primary">
                  {isLoading ? 'Registering...' : 'Register'}
                </button>
                <button type="button" onClick={() => setShowRegister(false)} className="btn btn-secondary">
                  Cancel
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="legal-chat-container">
      <div className="chat-header">
        <h2>NyaySetu Legal AI Chat</h2>
        <div className="user-info">
          <span>Welcome, {userEmail}</span>
          <button onClick={handleLogout} className="btn btn-small">Logout</button>
        </div>
      </div>

      {message && <div className="message">{message}</div>}

      <div className="language-selector">
        <label>Language:</label>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          {supportedLanguages.map(lang => (
            <option key={lang.code} value={lang.code}>
              {lang.native} ({lang.name})
            </option>
          ))}
        </select>
      </div>

      <div className="chat-input">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask your legal question here..."
          rows={4}
        />
        <button 
          onClick={sendQuestion} 
          disabled={isLoading || !question.trim()}
          className="btn btn-primary"
        >
          {isLoading ? 'Getting Answer...' : 'Send Question'}
        </button>
      </div>

      {answer && (
        <div className="chat-response">
          <h4>Legal Advice:</h4>
          <div className="answer-text">{answer}</div>
        </div>
      )}

      <div className="chat-tips">
        <h4>Tips for Better Legal Advice:</h4>
        <ul>
          <li>Be specific about your legal issue</li>
          <li>Include relevant details and context</li>
          <li>Mention any deadlines or time constraints</li>
          <li>Ask about next steps and documentation needed</li>
        </ul>
      </div>
    </div>
  );
}
