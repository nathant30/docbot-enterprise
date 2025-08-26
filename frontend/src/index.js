import React from 'react';
import ReactDOM from 'react-dom/client';

// Simple test component without any external dependencies
function App() {
  console.log('App component is rendering...');
  
  return React.createElement('div', {
    style: { 
      padding: '40px', 
      textAlign: 'center', 
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#ffffff',
      minHeight: '100vh'
    }
  }, [
    React.createElement('h1', { 
      key: 'title',
      style: { color: '#2563eb', fontSize: '2.5rem', marginBottom: '20px' }
    }, 'DocBot Enterprise'),
    React.createElement('p', { 
      key: 'subtitle',
      style: { fontSize: '1.2rem', marginBottom: '30px' }
    }, 'AI-Powered Invoice Processing System'),
    React.createElement('div', {
      key: 'status',
      style: { 
        padding: '20px', 
        backgroundColor: '#f0f9f0', 
        borderRadius: '8px',
        border: '2px solid #059669',
        display: 'inline-block',
        fontSize: '1.1rem'
      }
    }, '✅ System is Online and Working!')
  ]);
}

console.log('Starting React app...');

try {
  const root = ReactDOM.createRoot(document.getElementById('root'));
  console.log('React root created successfully');
  
  root.render(React.createElement(App));
  console.log('App rendered successfully');
} catch (error) {
  console.error('Error rendering app:', error);
  
  // Fallback to direct DOM manipulation
  document.getElementById('root').innerHTML = `
    <div style="padding: 40px; text-align: center; font-family: Arial, sans-serif;">
      <h1 style="color: #2563eb;">DocBot Enterprise</h1>
      <p>AI-Powered Invoice Processing System</p>
      <div style="color: #059669; font-weight: bold;">✅ System Online (Fallback Mode)</div>
      <div style="margin-top: 20px; font-size: 0.9rem; color: #666;">
        Frontend: Loaded | Backend: https://docbot-enterprise-backend.onrender.com
      </div>
    </div>
  `;
}