"""
DocBot Enterprise - FastAPI Backend Application
Production-ready invoice automation system
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
import os
from typing import List
import logging

from app.core.database import get_db, engine, Base
from app.core.config import settings
from app.core.security import verify_token, create_access_token
from app.models.user import User
from app.models.invoice import Invoice
from app.models.vendor import Vendor
from app.services.ocr_service import OCRService
from app.services.file_service import FileService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="DocBot Enterprise API",
    description="AI-powered invoice processing and ERP integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
ocr_service = OCRService()
file_service = FileService()

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "DocBot Enterprise API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "docbot-backend",
        "version": "1.0.0"
    }

# Authentication endpoints
@app.post("/api/v1/auth/login", tags=["Authentication"])
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """User authentication"""
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }

@app.get("/api/v1/users/me", tags=["Users"])
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user info"""
    token = credentials.credentials
    email = verify_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Invoice endpoints
@app.post("/api/v1/invoices/upload", tags=["Invoices"])
async def upload_invoice(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Upload and process invoice file"""
    # Validate file type
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload PDF, JPEG, or PNG files."
        )
    
    # Verify user
    token = credentials.credentials
    user_email = verify_token(token)
    user = db.query(User).filter(User.email == user_email).first()
    
    try:
        # Save file
        file_path = await file_service.save_uploaded_file(file)
        
        # Process with OCR
        ocr_result = await ocr_service.process_document(file_path)
        
        # Create invoice record
        invoice_data = {
            "invoice_number": ocr_result.extracted_fields.get("invoice_number"),
            "vendor_name": ocr_result.extracted_fields.get("vendor_name"),
            "total_amount": ocr_result.extracted_fields.get("total_amount", 0.0),
            "invoice_date": ocr_result.extracted_fields.get("invoice_date"),
            "ocr_confidence_score": ocr_result.confidence_scores.get("overall", 0.0),
            "file_path": file_path,
            "user_id": user.id,
            "status": "pending"
        }
        
        invoice = Invoice(**invoice_data)
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        
        logger.info(f"Invoice {invoice.id} processed successfully")
        
        return {
            "status": "success",
            "invoice_id": invoice.id,
            "extracted_data": ocr_result.extracted_fields,
            "confidence_score": ocr_result.confidence_scores.get("overall", 0.0)
        }
        
    except Exception as e:
        logger.error(f"Error processing invoice: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing invoice: {str(e)}"
        )

@app.get("/api/v1/invoices", tags=["Invoices"])
async def list_invoices(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """List invoices with filtering"""
    token = credentials.credentials
    user_email = verify_token(token)
    user = db.query(User).filter(User.email == user_email).first()
    
    query = db.query(Invoice).filter(Invoice.user_id == user.id)
    
    if status_filter:
        query = query.filter(Invoice.status == status_filter)
    
    invoices = query.offset(skip).limit(limit).all()
    return {"invoices": invoices}

@app.get("/api/v1/invoices/{invoice_id}", tags=["Invoices"])
async def get_invoice(
    invoice_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get invoice by ID"""
    token = credentials.credentials
    user_email = verify_token(token)
    user = db.query(User).filter(User.email == user_email).first()
    
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return invoice

@app.put("/api/v1/invoices/{invoice_id}/approve", tags=["Invoices"])
async def approve_invoice(
    invoice_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Approve invoice for ERP sync"""
    token = credentials.credentials
    user_email = verify_token(token)
    user = db.query(User).filter(User.email == user_email).first()
    
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice.status = "approved"
    invoice.approved_by = user.id
    db.commit()
    
    logger.info(f"Invoice {invoice_id} approved by user {user.id}")
    
    return {"status": "success", "message": "Invoice approved"}

@app.get("/api/v1/vendors", tags=["Vendors"])
async def list_vendors(
    skip: int = 0,
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """List vendors"""
    vendors = db.query(Vendor).offset(skip).limit(limit).all()
    return {"vendors": vendors}

# Statistics endpoint
@app.get("/api/v1/stats/dashboard", tags=["Statistics"])
async def get_dashboard_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    token = credentials.credentials
    user_email = verify_token(token)
    user = db.query(User).filter(User.email == user_email).first()
    
    total_invoices = db.query(Invoice).filter(Invoice.user_id == user.id).count()
    pending_invoices = db.query(Invoice).filter(
        Invoice.user_id == user.id,
        Invoice.status == "pending"
    ).count()
    approved_invoices = db.query(Invoice).filter(
        Invoice.user_id == user.id,
        Invoice.status == "approved"
    ).count()
    
    return {
        "total_invoices": total_invoices,
        "pending_review": pending_invoices,
        "approved_invoices": approved_invoices,
        "processing_accuracy": 95.2,  # This would be calculated from actual data
        "avg_processing_time": 28.5   # This would be calculated from actual data
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )