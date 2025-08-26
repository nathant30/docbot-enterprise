import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

function App() {
  return (
    <div style={{ padding: '20px', textAlign: 'center', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#2563eb' }}>DocBot Enterprise</h1>
      <p>AI-Powered Invoice Processing System</p>
      <p style={{ color: '#059669' }}>✅ System Online</p>
      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
        <p>Frontend: Connected</p>
        <p>Backend: https://docbot-enterprise-backend.onrender.com</p>
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(
  document.getElementById('root')
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);