import React from 'react';
import LegalChat from './components/LegalChat';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="logo">
          <h1>NyaySetu</h1>
          <p>Legal AI Assistant</p>
        </div>
      </header>
      <main>
        <LegalChat />
      </main>
      <footer className="App-footer">
        <p>&copy; 2024 NyaySetu. Empowering legal access through AI.</p>
      </footer>
    </div>
  );
}

export default App;
