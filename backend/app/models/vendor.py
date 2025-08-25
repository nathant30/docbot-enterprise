"""
DocBot Enterprise - Vendor Model
"""

from sqlalchemy import Column, String, Text, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Vendor(BaseModel):
    """Vendor model for invoice processing"""
    __tablename__ = "vendors"
    
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Address fields
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True, default="US")
    
    # Tax information
    tax_id = Column(String(50), nullable=True)
    tax_rate = Column(Numeric(5, 4), nullable=True, default=0.0)
    
    # Payment information
    payment_terms = Column(String(100), nullable=True)
    preferred_payment_method = Column(String(50), nullable=True)
    
    # Business details
    industry = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Flags
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    requires_po = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    invoices = relationship("Invoice", back_populates="vendor")
    
    def get_full_address(self) -> str:
        """Get formatted full address"""
        address_parts = []
        
        if self.address_line1:
            address_parts.append(self.address_line1)
        if self.address_line2:
            address_parts.append(self.address_line2)
        
        city_state_zip = []
        if self.city:
            city_state_zip.append(self.city)
        if self.state:
            city_state_zip.append(self.state)
        if self.postal_code:
            city_state_zip.append(self.postal_code)
        
        if city_state_zip:
            address_parts.append(", ".join(city_state_zip))
        
        if self.country and self.country != "US":
            address_parts.append(self.country)
        
        return "\n".join(address_parts)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "address": {
                "line1": self.address_line1,
                "line2": self.address_line2,
                "city": self.city,
                "state": self.state,
                "postal_code": self.postal_code,
                "country": self.country,
                "full_address": self.get_full_address()
            },
            "tax_id": self.tax_id,
            "tax_rate": float(self.tax_rate) if self.tax_rate else 0.0,
            "payment_terms": self.payment_terms,
            "preferred_payment_method": self.preferred_payment_method,
            "industry": self.industry,
            "notes": self.notes,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "requires_po": self.requires_po,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }