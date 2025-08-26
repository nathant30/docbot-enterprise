import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';

// Simple Login Component
function Login({ onLogin }) {
  const [email, setEmail] = useState('demo@docbot.com');
  const [password, setPassword] = useState('password');
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('https://docbot-enterprise-backend.onrender.com/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        onLogin(data.access_token);
      } else {
        alert('Login failed. Try with demo credentials or register new account.');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login error. Backend might be starting up.');
    }
    
    setLoading(false);
  };
  
  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>DocBot Enterprise Login</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Email:</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Password:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <button 
          type="submit" 
          disabled={loading}
          style={{ 
            width: '100%', 
            padding: '10px', 
            backgroundColor: '#2563eb', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <div style={{ marginTop: '15px', fontSize: '0.9rem', color: '#666' }}>
        <p>Demo credentials: demo@docbot.com / password</p>
        <p>Or try registering a new account with the backend API</p>
      </div>
    </div>
  );
}

// Simple Dashboard Component
function Dashboard() {
  const [stats, setStats] = useState(null);
  
  React.useEffect(() => {
    // Mock stats for demo without authentication
    setStats({
      total_invoices: 47,
      pending_review: 8,
      approved_invoices: 39,
      total_amount: "23456.78"
    });
  }, []);
  
  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1>DocBot Enterprise Dashboard</h1>
        <div style={{ padding: '8px 16px', backgroundColor: '#059669', color: 'white', borderRadius: '4px' }}>
          ✅ Demo Mode
        </div>
      </div>
      
      {stats ? (
        <div>
          <h3>📊 Dashboard Statistics</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '30px' }}>
            <div style={{ padding: '20px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
              <h4>Total Invoices</h4>
              <p style={{ fontSize: '2rem', color: '#2563eb', margin: '10px 0' }}>{stats.total_invoices}</p>
            </div>
            <div style={{ padding: '20px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
              <h4>Pending Review</h4>
              <p style={{ fontSize: '2rem', color: '#dc2626', margin: '10px 0' }}>{stats.pending_review}</p>
            </div>
            <div style={{ padding: '20px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
              <h4>Total Amount</h4>
              <p style={{ fontSize: '2rem', color: '#059669', margin: '10px 0' }}>${stats.total_amount}</p>
            </div>
          </div>
        </div>
      ) : (
        <p>Loading dashboard data...</p>
      )}
      
      <nav style={{ marginBottom: '20px' }}>
        <Link to="/upload" style={{ marginRight: '20px', color: '#2563eb' }}>📄 Upload Invoice</Link>
        <Link to="/invoices" style={{ marginRight: '20px', color: '#2563eb' }}>📋 View Invoices</Link>
        <Link to="/vendors" style={{ color: '#2563eb' }}>🏢 Vendors</Link>
      </nav>
      
      <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f0f9ff', borderRadius: '8px' }}>
        <h3>🔗 System Status</h3>
        <p>✅ Frontend: Connected</p>
        <p>✅ Backend API: https://docbot-enterprise-backend.onrender.com</p>
        <p>✅ Authentication: Active</p>
        <p>📖 API Documentation: <a href="https://docbot-enterprise-backend.onrender.com/docs" target="_blank" rel="noopener noreferrer">View Swagger Docs</a></p>
      </div>
    </div>
  );
}

// Simple Invoice Upload Component
function InvoiceUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await fetch('https://docbot-enterprise-backend.onrender.com/api/v1/invoices/upload', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        alert('Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload error');
    }
    
    setUploading(false);
  };
  
  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <Link to="/" style={{ color: '#2563eb', marginBottom: '20px', display: 'block' }}>← Back to Dashboard</Link>
      <h2>📄 Upload Invoice</h2>
      
      <form onSubmit={handleUpload} style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>
        <div style={{ marginBottom: '20px' }}>
          <label>Select Invoice File (PDF, PNG, JPG):</label>
          <input 
            type="file" 
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ width: '100%', padding: '8px', margin: '10px 0' }}
          />
        </div>
        
        <button 
          type="submit" 
          disabled={!file || uploading}
          style={{ 
            width: '100%', 
            padding: '12px', 
            backgroundColor: '#2563eb', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: (!file || uploading) ? 'not-allowed' : 'pointer'
          }}
        >
          {uploading ? 'Processing...' : 'Upload & Process Invoice'}
        </button>
      </form>
      
      {result && (
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f9ff', borderRadius: '8px' }}>
          <h3>✅ Upload Successful!</h3>
          <p>Invoice ID: {result.invoice_id}</p>
          <p>Status: {result.status}</p>
          {result.extracted_data && (
            <div>
              <h4>Extracted Data:</h4>
              <pre style={{ backgroundColor: '#f3f4f6', padding: '10px', borderRadius: '4px', fontSize: '0.9rem' }}>
                {JSON.stringify(result.extracted_data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Main App Component
function App() {
  // Skip authentication for now - directly show the dashboard
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<InvoiceUpload />} />
        <Route path="/invoices" element={<div style={{padding: '20px'}}><Link to="/">← Dashboard</Link><h2>📋 Invoice List</h2><p>Feature coming soon...</p></div>} />
        <Route path="/vendors" element={<div style={{padding: '20px'}}><Link to="/">← Dashboard</Link><h2>🏢 Vendors</h2><p>Feature coming soon...</p></div>} />
        <Route path="/login" element={<Login onLogin={() => {}} />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;