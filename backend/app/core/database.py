"""
DocBot Enterprise - Database Configuration
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Database engine configuration
engine = create_engine(
    settings.DATABASE_URL,
    echo=False  # Set to True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

def get_db():
    """
    Database dependency for FastAPI
    Provides a database session for each request
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def drop_tables():
    """Drop all database tables - USE WITH CAUTION"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise