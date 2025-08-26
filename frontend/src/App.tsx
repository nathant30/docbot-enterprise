import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <div className="App">
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h1>DocBot Enterprise</h1>
        <p>AI-Powered Invoice Processing System</p>
        <p>System is initializing...</p>
      </div>
    </div>
  );
}

export default App;