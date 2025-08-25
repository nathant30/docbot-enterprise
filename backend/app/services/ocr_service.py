"""
DocBot Enterprise - OCR Processing Service
Supports multiple OCR providers: Azure Cognitive Services, Google Vision, Tesseract
"""

import os
import asyncio
import logging
import re
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import json

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class OCRResult:
    """OCR processing result"""
    raw_text: str
    extracted_fields: Dict[str, Any]
    confidence_scores: Dict[str, float]
    processing_time: float
    provider_used: str
    page_count: int = 1


class OCRService:
    """Multi-provider OCR service for invoice processing"""
    
    def __init__(self):
        self.providers = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available OCR providers"""
        if settings.AZURE_COG_SERVICES_KEY and settings.AZURE_COG_SERVICES_ENDPOINT:
            self.providers.append("azure")
            logger.info("Azure Cognitive Services OCR initialized")
        
        if settings.GOOGLE_VISION_CREDENTIALS:
            self.providers.append("google")
            logger.info("Google Vision API initialized")
        
        # Tesseract is always available as fallback
        self.providers.append("tesseract")
        logger.info("Tesseract OCR initialized as fallback")
    
    async def process_document(self, file_path: str, provider: str = None) -> OCRResult:
        """
        Process document with OCR and extract structured data
        
        Args:
            file_path: Path to the document file
            provider: Preferred OCR provider ('azure', 'google', 'tesseract')
        
        Returns:
            OCRResult with extracted text and structured fields
        """
        start_time = asyncio.get_event_loop().time()
        
        # Determine provider to use
        if provider and provider in self.providers:
            selected_provider = provider
        else:
            selected_provider = self.providers[0] if self.providers else "tesseract"
        
        logger.info(f"Processing {file_path} with {selected_provider}")
        
        try:
            # Extract text based on provider
            if selected_provider == "azure":
                raw_text = await self._process_with_azure(file_path)
            elif selected_provider == "google":
                raw_text = await self._process_with_google(file_path)
            else:
                raw_text = await self._process_with_tesseract(file_path)
            
            # Extract structured fields from text
            extracted_fields = self._extract_invoice_fields(raw_text)
            
            # Calculate confidence scores
            confidence_scores = self._calculate_confidence_scores(raw_text, extracted_fields)
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return OCRResult(
                raw_text=raw_text,
                extracted_fields=extracted_fields,
                confidence_scores=confidence_scores,
                processing_time=processing_time,
                provider_used=selected_provider
            )
            
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            # Fallback to tesseract if primary provider fails
            if selected_provider != "tesseract":
                logger.info("Falling back to Tesseract")
                return await self.process_document(file_path, "tesseract")
            raise
    
    async def _process_with_azure(self, file_path: str) -> str:
        """Process document with Azure Cognitive Services"""
        try:
            from azure.cognitiveservices.vision.computervision import ComputerVisionClient
            from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
            from msrest.authentication import CognitiveServicesCredentials
            
            # Initialize client
            credentials = CognitiveServicesCredentials(settings.AZURE_COG_SERVICES_KEY)
            client = ComputerVisionClient(settings.AZURE_COG_SERVICES_ENDPOINT, credentials)
            
            # Read file and submit for OCR
            with open(file_path, "rb") as image_stream:
                read_response = client.read_in_stream(image_stream, raw=True)
            
            # Get operation ID
            operation_id = read_response.headers["Operation-Location"].split("/")[-1]
            
            # Poll for results
            while True:
                read_result = client.get_read_result(operation_id)
                if read_result.status not in [OperationStatusCodes.not_started, OperationStatusCodes.running]:
                    break
                await asyncio.sleep(1)
            
            # Extract text
            text_lines = []
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        text_lines.append(line.text)
            
            return "\n".join(text_lines)
            
        except ImportError:
            logger.error("Azure Cognitive Services SDK not installed")
            raise
        except Exception as e:
            logger.error(f"Azure OCR failed: {str(e)}")
            raise
    
    async def _process_with_google(self, file_path: str) -> str:
        """Process document with Google Vision API"""
        try:
            from google.cloud import vision
            import io
            
            # Initialize client
            client = vision.ImageAnnotatorClient()
            
            # Read file
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Perform text detection
            response = client.text_detection(image=image)
            texts = response.text_annotations
            
            if response.error.message:
                raise Exception(f'Google Vision API error: {response.error.message}')
            
            # Return full text annotation
            return texts[0].description if texts else ""
            
        except ImportError:
            logger.error("Google Cloud Vision SDK not installed")
            raise
        except Exception as e:
            logger.error(f"Google Vision OCR failed: {str(e)}")
            raise
    
    async def _process_with_tesseract(self, file_path: str) -> str:
        """Process document with Tesseract OCR"""
        try:
            import pytesseract
            from PIL import Image
            
            # Set tesseract path if configured
            if settings.TESSERACT_PATH:
                pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH
            
            # Process image
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, config='--psm 6')
            
            return text
            
        except ImportError:
            logger.error("Pytesseract not installed")
            raise
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {str(e)}")
            raise
    
    def _extract_invoice_fields(self, text: str) -> Dict[str, Any]:
        """Extract structured fields from OCR text"""
        fields = {}
        
        # Clean text
        text = text.strip()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Extract invoice number
        invoice_patterns = [
            r'invoice\s*#?\s*:?\s*([A-Z0-9-]+)',
            r'inv\s*#?\s*:?\s*([A-Z0-9-]+)',
            r'bill\s*#?\s*:?\s*([A-Z0-9-]+)',
        ]
        
        for pattern in invoice_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields['invoice_number'] = match.group(1)
                break
        
        # Extract total amount
        amount_patterns = [
            r'total\s*:?\s*\$?(\d+[,.]?\d*\.?\d*)',
            r'amount\s*due\s*:?\s*\$?(\d+[,.]?\d*\.?\d*)',
            r'balance\s*:?\s*\$?(\d+[,.]?\d*\.?\d*)',
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    fields['total_amount'] = float(amount_str)
                except ValueError:
                    continue
                break
        
        # Extract dates
        date_patterns = [
            r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'(\d{2,4}[\/\-]\d{1,2}[\/\-]\d{1,2})',
        ]
        
        dates_found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates_found.extend(matches)
        
        if dates_found:
            # Try to identify invoice date vs due date
            fields['invoice_date'] = dates_found[0]
            if len(dates_found) > 1:
                fields['due_date'] = dates_found[1]
        
        # Extract vendor name (usually appears early in the document)
        vendor_lines = []
        for i, line in enumerate(lines[:10]):  # Check first 10 lines
            if len(line) > 5 and not re.search(r'\d', line):  # Non-numeric lines
                vendor_lines.append(line)
        
        if vendor_lines:
            # Take the longest line as potential vendor name
            fields['vendor_name'] = max(vendor_lines, key=len)
        
        # Extract PO number
        po_patterns = [
            r'p\.?o\.?\s*#?\s*:?\s*([A-Z0-9-]+)',
            r'purchase\s*order\s*#?\s*:?\s*([A-Z0-9-]+)',
        ]
        
        for pattern in po_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields['po_number'] = match.group(1)
                break
        
        # Extract tax amount
        tax_patterns = [
            r'tax\s*:?\s*\$?(\d+[,.]?\d*\.?\d*)',
            r'vat\s*:?\s*\$?(\d+[,.]?\d*\.?\d*)',
        ]
        
        for pattern in tax_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                tax_str = match.group(1).replace(',', '')
                try:
                    fields['tax_amount'] = float(tax_str)
                except ValueError:
                    continue
                break
        
        # Calculate subtotal if we have total and tax
        if 'total_amount' in fields and 'tax_amount' in fields:
            fields['subtotal'] = fields['total_amount'] - fields['tax_amount']
        
        return fields
    
    def _calculate_confidence_scores(self, text: str, fields: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for extracted fields"""
        scores = {}
        
        # Overall text quality score
        text_quality = min(1.0, len(text) / 500)  # Normalize by expected text length
        scores['text_quality'] = text_quality
        
        # Field extraction confidence
        critical_fields = ['invoice_number', 'total_amount', 'vendor_name']
        extracted_critical = sum(1 for field in critical_fields if field in fields and fields[field])
        scores['field_extraction'] = extracted_critical / len(critical_fields)
        
        # Overall confidence (weighted average)
        scores['overall'] = (text_quality * 0.3 + scores['field_extraction'] * 0.7)
        
        return scores