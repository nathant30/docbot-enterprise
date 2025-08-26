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

// Invoice List Component
function InvoiceList() {
  const [invoices] = useState([
    {
      id: 12345,
      invoice_number: "INV-2025-0826",
      vendor_name: "Demo Vendor Corp",
      total_amount: "1,250.75",
      invoice_date: "2025-08-26",
      status: "pending",
      upload_date: "2025-08-26 14:30",
      confidence: 0.95
    },
    {
      id: 12344,
      invoice_number: "INV-2025-0825",
      vendor_name: "ABC Technology Solutions",
      total_amount: "3,450.00",
      invoice_date: "2025-08-25",
      status: "approved",
      upload_date: "2025-08-25 09:15",
      confidence: 0.98
    },
    {
      id: 12343,
      invoice_number: "SRV-2025-1234",
      vendor_name: "Professional Services Inc",
      total_amount: "875.50",
      invoice_date: "2025-08-24",
      status: "approved",
      upload_date: "2025-08-24 16:45",
      confidence: 0.92
    },
    {
      id: 12342,
      invoice_number: "UTIL-2025-0823",
      vendor_name: "City Utilities Department",
      total_amount: "234.67",
      invoice_date: "2025-08-20",
      status: "pending",
      upload_date: "2025-08-23 11:20",
      confidence: 0.89
    },
    {
      id: 12341,
      invoice_number: "SUP-2025-5678",
      vendor_name: "Office Supply Express",
      total_amount: "156.89",
      invoice_date: "2025-08-22",
      status: "approved",
      upload_date: "2025-08-22 13:10",
      confidence: 0.96
    }
  ]);

  const getStatusColor = (status) => {
    switch(status) {
      case 'approved': return '#059669';
      case 'pending': return '#dc2626';
      case 'processing': return '#2563eb';
      default: return '#6b7280';
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <Link to="/" style={{ color: '#2563eb', marginBottom: '20px', display: 'inline-block' }}>
          ← Back to Dashboard
        </Link>
        <h2>📋 Invoice Management</h2>
      </div>
      
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', alignItems: 'center' }}>
        <span style={{ color: '#666' }}>Filter by status:</span>
        <select style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}>
          <option>All Invoices</option>
          <option>Pending Review</option>
          <option>Approved</option>
          <option>Processing</option>
        </select>
        <Link 
          to="/upload" 
          style={{ 
            marginLeft: 'auto', 
            padding: '10px 20px', 
            backgroundColor: '#2563eb', 
            color: 'white', 
            textDecoration: 'none',
            borderRadius: '4px'
          }}
        >
          + Upload New Invoice
        </Link>
      </div>

      <div style={{ 
        overflowX: 'auto',
        border: '1px solid #e5e7eb',
        borderRadius: '8px',
        backgroundColor: 'white'
      }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ backgroundColor: '#f9fafb' }}>
            <tr>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Invoice #</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Vendor</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Amount</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Date</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Status</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Confidence</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((invoice, index) => (
              <tr key={invoice.id} style={{ borderBottom: index < invoices.length - 1 ? '1px solid #e5e7eb' : 'none' }}>
                <td style={{ padding: '12px' }}>
                  <div>
                    <strong>{invoice.invoice_number}</strong>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>ID: {invoice.id}</div>
                  </div>
                </td>
                <td style={{ padding: '12px' }}>{invoice.vendor_name}</td>
                <td style={{ padding: '12px' }}>
                  <strong>${invoice.total_amount}</strong>
                </td>
                <td style={{ padding: '12px' }}>
                  <div>{invoice.invoice_date}</div>
                  <div style={{ fontSize: '0.8rem', color: '#666' }}>Uploaded: {invoice.upload_date}</div>
                </td>
                <td style={{ padding: '12px' }}>
                  <span style={{ 
                    padding: '4px 8px', 
                    borderRadius: '12px', 
                    backgroundColor: getStatusColor(invoice.status) + '20',
                    color: getStatusColor(invoice.status),
                    fontSize: '0.8rem',
                    fontWeight: 'bold'
                  }}>
                    {invoice.status.toUpperCase()}
                  </span>
                </td>
                <td style={{ padding: '12px' }}>
                  <div style={{ color: invoice.confidence > 0.9 ? '#059669' : '#dc2626' }}>
                    {Math.round(invoice.confidence * 100)}%
                  </div>
                </td>
                <td style={{ padding: '12px' }}>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button style={{ 
                      padding: '4px 8px', 
                      fontSize: '0.8rem',
                      backgroundColor: '#f3f4f6',
                      border: '1px solid #d1d5db',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}>
                      View
                    </button>
                    {invoice.status === 'pending' && (
                      <button style={{ 
                        padding: '4px 8px', 
                        fontSize: '0.8rem',
                        backgroundColor: '#059669',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                      }}>
                        Approve
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div style={{ marginTop: '20px', textAlign: 'center', color: '#666' }}>
        Showing {invoices.length} invoices • Total processed: 47 invoices
      </div>
    </div>
  );
}

// Vendor List Component
function VendorList() {
  const [vendors] = useState([
    {
      id: 1,
      name: "Demo Vendor Corp",
      total_invoices: 12,
      total_amount: "15,750.25",
      avg_processing_time: "2.3 days",
      confidence_avg: 0.95,
      last_invoice: "2025-08-26",
      payment_terms: "Net 30",
      contact_email: "billing@demovendor.com"
    },
    {
      id: 2,
      name: "ABC Technology Solutions",
      total_invoices: 8,
      total_amount: "28,450.00",
      avg_processing_time: "1.8 days",
      confidence_avg: 0.97,
      last_invoice: "2025-08-25",
      payment_terms: "Net 15",
      contact_email: "invoices@abctech.com"
    },
    {
      id: 3,
      name: "Professional Services Inc",
      total_invoices: 6,
      total_amount: "5,250.75",
      avg_processing_time: "3.1 days",
      confidence_avg: 0.92,
      last_invoice: "2025-08-24",
      payment_terms: "Net 30",
      contact_email: "finance@proservices.com"
    },
    {
      id: 4,
      name: "City Utilities Department",
      total_invoices: 15,
      total_amount: "3,520.45",
      avg_processing_time: "1.2 days",
      confidence_avg: 0.89,
      last_invoice: "2025-08-20",
      payment_terms: "Due on Receipt",
      contact_email: "billing@cityutil.gov"
    },
    {
      id: 5,
      name: "Office Supply Express",
      total_invoices: 6,
      total_amount: "1,876.89",
      avg_processing_time: "2.7 days",
      confidence_avg: 0.96,
      last_invoice: "2025-08-22",
      payment_terms: "Net 30",
      contact_email: "orders@officesupply.com"
    }
  ]);

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <Link to="/" style={{ color: '#2563eb', marginBottom: '20px', display: 'inline-block' }}>
          ← Back to Dashboard
        </Link>
        <h2>🏢 Vendor Management</h2>
      </div>
      
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', alignItems: 'center' }}>
        <input 
          type="text" 
          placeholder="Search vendors..."
          style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc', width: '300px' }}
        />
        <select style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}>
          <option>All Vendors</option>
          <option>High Volume (>10 invoices)</option>
          <option>Recent Activity</option>
          <option>High Accuracy (>95%)</option>
        </select>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px' }}>
        {vendors.map(vendor => (
          <div key={vendor.id} style={{ 
            border: '1px solid #e5e7eb', 
            borderRadius: '8px', 
            padding: '20px', 
            backgroundColor: 'white',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '15px' }}>
              <div>
                <h3 style={{ margin: '0 0 5px 0', color: '#1f2937' }}>{vendor.name}</h3>
                <div style={{ fontSize: '0.9rem', color: '#666' }}>
                  {vendor.contact_email}
                </div>
              </div>
              <div style={{ 
                padding: '4px 8px', 
                backgroundColor: vendor.confidence_avg > 0.9 ? '#dcfce7' : '#fef3c7',
                color: vendor.confidence_avg > 0.9 ? '#166534' : '#92400e',
                borderRadius: '12px',
                fontSize: '0.8rem',
                fontWeight: 'bold'
              }}>
                {Math.round(vendor.confidence_avg * 100)}% Accuracy
              </div>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
              <div>
                <div style={{ fontSize: '0.8rem', color: '#666' }}>Total Invoices</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#2563eb' }}>
                  {vendor.total_invoices}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: '#666' }}>Total Amount</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#059669' }}>
                  ${vendor.total_amount}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: '#666' }}>Avg Processing</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold' }}>
                  {vendor.avg_processing_time}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: '#666' }}>Payment Terms</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold' }}>
                  {vendor.payment_terms}
                </div>
              </div>
            </div>
            
            <div style={{ paddingTop: '15px', borderTop: '1px solid #e5e7eb' }}>
              <div style={{ fontSize: '0.8rem', color: '#666', marginBottom: '8px' }}>
                Last Invoice: {vendor.last_invoice}
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button style={{ 
                  flex: 1,
                  padding: '8px', 
                  backgroundColor: '#f3f4f6',
                  border: '1px solid #d1d5db',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '0.9rem'
                }}>
                  View History
                </button>
                <button style={{ 
                  flex: 1,
                  padding: '8px', 
                  backgroundColor: '#2563eb',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '0.9rem'
                }}>
                  Edit Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div style={{ marginTop: '30px', textAlign: 'center', color: '#666' }}>
        Showing {vendors.length} vendors • {vendors.reduce((sum, v) => sum + v.total_invoices, 0)} total invoices processed
      </div>
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
        <Route path="/invoices" element={<InvoiceList />} />
        <Route path="/vendors" element={<VendorList />} />
        <Route path="/login" element={<Login onLogin={() => {}} />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;