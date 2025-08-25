"""
DocBot Enterprise - Invoice Model
"""

from sqlalchemy import Column, String, Text, Numeric, DateTime, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any, Optional

from models.base import BaseModel


class Invoice(BaseModel):
    """Invoice model for processing and tracking invoices"""
    __tablename__ = "invoices"
    
    # Basic invoice information
    invoice_number = Column(String(100), nullable=True, index=True)
    po_number = Column(String(100), nullable=True, index=True)
    
    # Financial information
    subtotal = Column(Numeric(12, 2), nullable=True, default=0.0)
    tax_amount = Column(Numeric(12, 2), nullable=True, default=0.0)
    total_amount = Column(Numeric(12, 2), nullable=False, default=0.0)
    currency = Column(String(3), nullable=False, default="USD")
    
    # Dates
    invoice_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    received_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Processing information
    status = Column(String(50), nullable=False, default="pending", index=True)
    ocr_confidence_score = Column(Numeric(3, 2), nullable=True)
    manual_review_required = Column(Boolean, default=False, nullable=False)
    
    # File information
    original_filename = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=True)
    
    # OCR extracted data
    extracted_fields = Column(JSON, nullable=True)
    ocr_raw_text = Column(Text, nullable=True)
    
    # Approval and processing
    approved_at = Column(DateTime, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    synced_to_erp_at = Column(DateTime, nullable=True)
    
    # Notes and comments
    processing_notes = Column(Text, nullable=True)
    approval_notes = Column(Text, nullable=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True, index=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="invoices", foreign_keys=[user_id])
    vendor = relationship("Vendor", back_populates="invoices")
    approver = relationship("User", foreign_keys=[approved_by])
    
    def approve(self, approved_by_user_id: int, notes: str = None):
        """Approve the invoice"""
        self.status = "approved"
        self.approved_by = approved_by_user_id
        self.approved_at = datetime.utcnow()
        if notes:
            self.approval_notes = notes
    
    def reject(self, notes: str = None):
        """Reject the invoice"""
        self.status = "rejected"
        if notes:
            self.approval_notes = notes
    
    def mark_processed(self):
        """Mark invoice as processed"""
        self.status = "processed"
        self.processed_at = datetime.utcnow()
    
    def mark_synced_to_erp(self):
        """Mark invoice as synced to ERP"""
        self.synced_to_erp_at = datetime.utcnow()
        if self.status == "approved":
            self.status = "synced"
    
    def requires_manual_review(self) -> bool:
        """Check if invoice requires manual review"""
        if self.manual_review_required:
            return True
        
        # Check confidence score
        if self.ocr_confidence_score and self.ocr_confidence_score < 0.85:
            return True
        
        # Check for missing critical fields
        if not self.invoice_number or not self.total_amount or not self.vendor_id:
            return True
        
        return False
    
    def get_vendor_name(self) -> str:
        """Get vendor name from relationship or extracted fields"""
        if self.vendor and self.vendor.name:
            return self.vendor.name
        
        if self.extracted_fields and "vendor_name" in self.extracted_fields:
            return self.extracted_fields["vendor_name"]
        
        return "Unknown Vendor"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "po_number": self.po_number,
            "vendor_name": self.get_vendor_name(),
            "vendor_id": self.vendor_id,
            "subtotal": float(self.subtotal) if self.subtotal else 0.0,
            "tax_amount": float(self.tax_amount) if self.tax_amount else 0.0,
            "total_amount": float(self.total_amount),
            "currency": self.currency,
            "invoice_date": self.invoice_date.isoformat() if self.invoice_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "received_date": self.received_date.isoformat(),
            "status": self.status,
            "ocr_confidence_score": float(self.ocr_confidence_score) if self.ocr_confidence_score else None,
            "manual_review_required": self.manual_review_required,
            "requires_manual_review": self.requires_manual_review(),
            "original_filename": self.original_filename,
            "file_size": self.file_size,
            "file_type": self.file_type,
            "extracted_fields": self.extracted_fields,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "synced_to_erp_at": self.synced_to_erp_at.isoformat() if self.synced_to_erp_at else None,
            "processing_notes": self.processing_notes,
            "approval_notes": self.approval_notes,
            "user_id": self.user_id,
            "approved_by": self.approved_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }