"""
DocBot Enterprise - Configuration Management
"""

import os
from typing import List
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./docbot.db"
    
    # Security
    SECRET_KEY: str = "docbot-enterprise-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # CORS - Use string that gets parsed to avoid environment variable conflicts
    CORS_ORIGINS_STR: str = "http://localhost:3000,http://localhost:8080,https://localhost:3000,https://localhost:8080"
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_UPLOAD_TYPES_STR: str = "pdf,png,jpg,jpeg"
    
    @property
    def ALLOWED_UPLOAD_TYPES(self) -> List[str]:
        """Parse allowed upload types from comma-separated string"""
        return [file_type.strip() for file_type in self.ALLOWED_UPLOAD_TYPES_STR.split(",")]
    
    UPLOAD_DIRECTORY: str = "uploads"
    
    # OCR Configuration
    AZURE_COG_SERVICES_KEY: str = ""
    AZURE_COG_SERVICES_ENDPOINT: str = ""
    GOOGLE_VISION_CREDENTIALS: str = ""
    TESSERACT_PATH: str = "/usr/bin/tesseract"
    OCR_TIMEOUT_SECONDS: int = 30
    MIN_CONFIDENCE_THRESHOLD: float = 0.7
    
    # ERP Integration
    QUICKBOOKS_CLIENT_ID: str = ""
    QUICKBOOKS_CLIENT_SECRET: str = ""
    XERO_CLIENT_ID: str = ""
    XERO_CLIENT_SECRET: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Monitoring
    SENTRY_DSN: str = ""
    LOG_LEVEL: str = "INFO"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()