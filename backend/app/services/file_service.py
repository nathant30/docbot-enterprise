"""
DocBot Enterprise - File Processing Service
Handles file uploads, validation, storage, and management
"""

import os
import uuid
import shutil
import hashlib
import mimetypes
from pathlib import Path
from typing import Optional, Tuple, List
import logging
from datetime import datetime

from fastapi import UploadFile, HTTPException, status
from PIL import Image
import PyPDF2

from core.config import settings

logger = logging.getLogger(__name__)


class FileService:
    """Service for handling file uploads and management"""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIRECTORY)
        self.max_size = settings.MAX_UPLOAD_SIZE
        self.allowed_types = settings.ALLOWED_UPLOAD_TYPES
        self._ensure_upload_directory()
    
    def _ensure_upload_directory(self):
        """Ensure upload directory exists"""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        for subdir in ['invoices', 'temp', 'processed']:
            (self.upload_dir / subdir).mkdir(exist_ok=True)
    
    async def save_uploaded_file(self, file: UploadFile) -> str:
        """
        Save uploaded file to storage
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            str: Path to saved file
        """
        # Validate file
        await self._validate_file(file)
        
        # Generate unique filename
        file_ext = self._get_file_extension(file.filename)
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Determine storage path
        file_path = self.upload_dir / "invoices" / unique_filename
        
        try:
            # Save file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Reset file position for potential reuse
            await file.seek(0)
            
            logger.info(f"File saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            # Clean up partial file
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
    
    async def _validate_file(self, file: UploadFile):
        """Validate uploaded file"""
        # Check file size
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        # Reset file position
        await file.seek(0)
        
        if file_size > self.max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {self.max_size / 1024 / 1024:.1f}MB"
            )
        
        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file not allowed"
            )
        
        # Check file type
        file_ext = self._get_file_extension(file.filename)
        if file_ext.lower().lstrip('.') not in self.allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(self.allowed_types)}"
            )
        
        # Additional content validation
        await self._validate_file_content(file, file_ext)
    
    async def _validate_file_content(self, file: UploadFile, file_ext: str):
        """Validate file content matches extension"""
        try:
            content = await file.read()
            await file.seek(0)
            
            if file_ext.lower() == '.pdf':
                # Validate PDF
                try:
                    from io import BytesIO
                    pdf_reader = PyPDF2.PdfReader(BytesIO(content))
                    if len(pdf_reader.pages) == 0:
                        raise Exception("PDF has no pages")
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid PDF file"
                    )
            
            elif file_ext.lower() in ['.jpg', '.jpeg', '.png']:
                # Validate image
                try:
                    from io import BytesIO
                    image = Image.open(BytesIO(content))
                    image.verify()
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid image file"
                    )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"Content validation failed: {str(e)}")
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension from filename"""
        if not filename:
            return ""
        return Path(filename).suffix.lower()
    
    def get_file_info(self, file_path: str) -> dict:
        """Get information about a file"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = path.stat()
        mime_type, _ = mimetypes.guess_type(str(path))
        
        return {
            "filename": path.name,
            "size": stat.st_size,
            "mime_type": mime_type,
            "created_at": datetime.fromtimestamp(stat.st_ctime),
            "modified_at": datetime.fromtimestamp(stat.st_mtime),
            "extension": path.suffix.lower()
        }
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        
        return hash_md5.hexdigest()
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            return False
    
    def move_to_processed(self, file_path: str) -> str:
        """Move file to processed directory"""
        source_path = Path(file_path)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")
        
        # Create destination path
        dest_path = self.upload_dir / "processed" / source_path.name
        
        try:
            shutil.move(str(source_path), str(dest_path))
            logger.info(f"File moved to processed: {dest_path}")
            return str(dest_path)
        except Exception as e:
            logger.error(f"Error moving file: {str(e)}")
            raise
    
    def cleanup_temp_files(self, older_than_hours: int = 24):
        """Clean up temporary files older than specified hours"""
        temp_dir = self.upload_dir / "temp"
        cutoff_time = datetime.now().timestamp() - (older_than_hours * 3600)
        
        cleaned_count = 0
        
        try:
            for file_path in temp_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} temporary files")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return 0
    
    def get_storage_stats(self) -> dict:
        """Get storage statistics"""
        stats = {
            "total_files": 0,
            "total_size": 0,
            "by_type": {}
        }
        
        for file_path in self.upload_dir.rglob("*"):
            if file_path.is_file():
                stats["total_files"] += 1
                file_size = file_path.stat().st_size
                stats["total_size"] += file_size
                
                ext = file_path.suffix.lower()
                if ext not in stats["by_type"]:
                    stats["by_type"][ext] = {"count": 0, "size": 0}
                
                stats["by_type"][ext]["count"] += 1
                stats["by_type"][ext]["size"] += file_size
        
        return stats