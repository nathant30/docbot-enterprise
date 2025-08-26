# DocBot Enterprise - Complete Test Plan

## 🎯 System Testing Checklist

### Phase 1: Basic System Health
- [ ] Frontend loads at https://docbot-enterprise.onrender.com
- [ ] Backend API responds at https://docbot-enterprise-backend.onrender.com
- [ ] Swagger docs accessible at /docs
- [ ] Database connection working

### Phase 2: User Authentication
- [ ] Demo user creation: POST /api/v1/setup/demo
- [ ] User registration: POST /api/v1/auth/register with new email
- [ ] Login with demo credentials: demo@docbot.com / password
- [ ] JWT token generation and storage
- [ ] Protected route access after login

### Phase 3: Dashboard Functionality  
- [ ] Dashboard loads after login
- [ ] Statistics API call: GET /api/v1/stats/dashboard
- [ ] Display invoice counts, amounts, pending items
- [ ] Navigation links work (Upload, Invoices, Vendors)
- [ ] Logout functionality

### Phase 4: Invoice Processing
- [ ] Upload page loads
- [ ] File selection (PDF/JPG/PNG)
- [ ] Invoice upload: POST /api/v1/invoices/upload
- [ ] OCR processing starts
- [ ] Extracted data display (vendor, amount, date, line items)
- [ ] Success/error feedback

### Phase 5: Data Management
- [ ] Invoice list retrieval: GET /api/v1/invoices
- [ ] Individual invoice details: GET /api/v1/invoices/{id}
- [ ] Vendor list: GET /api/v1/vendors
- [ ] Invoice approval: PUT /api/v1/invoices/{id}/approve

### Phase 6: Error Handling
- [ ] Invalid login credentials
- [ ] Expired token handling
- [ ] File upload size limits
- [ ] Unsupported file formats
- [ ] Network error recovery

## 🧪 Test Scenarios

### Scenario 1: New User Registration
1. Access https://docbot-enterprise.onrender.com
2. Try to register with test@example.com
3. Login with new credentials
4. Verify dashboard loads

### Scenario 2: Invoice Processing Workflow
1. Login as demo user
2. Navigate to Upload page
3. Upload test invoice file
4. Verify OCR extraction results
5. Check invoice appears in dashboard stats

### Scenario 3: API Integration Test
1. Create user via registration endpoint
2. Authenticate and get JWT token
3. Call protected endpoints with token
4. Upload file and process
5. Retrieve processed results

## 📊 Expected Results
- Login success rate: 100%
- OCR processing: Extract vendor, amount, date minimum
- File upload: Support PDF, PNG, JPG up to 50MB
- Response times: < 5 seconds for file processing
- Error handling: Graceful user feedback

## 🔧 Manual Testing URLs
- Frontend: https://docbot-enterprise.onrender.com
- Backend Health: https://docbot-enterprise-backend.onrender.com/health
- API Docs: https://docbot-enterprise-backend.onrender.com/docs
- Demo Setup: https://docbot-enterprise-backend.onrender.com/api/v1/setup/demo