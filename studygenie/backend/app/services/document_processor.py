import os
import io
import tempfile
from typing import Optional, Tuple
from pathlib import Path
import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import docx

class DocumentProcessor:
    """Service for extracting text from various document formats"""
    
    def __init__(self):
        self.supported_formats = {'.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg'}
    
    def extract_text(self, file_path: str, file_type: str) -> Tuple[str, bool]:
        """
        Extract text from a document file
        
        Args:
            file_path: Path to the file
            file_type: Type of file (pdf, docx, txt, image)
            
        Returns:
            Tuple of (extracted_text, success)
        """
        try:
            if file_type.lower() == 'pdf':
                return self._extract_from_pdf(file_path)
            elif file_type.lower() == 'docx':
                return self._extract_from_docx(file_path)
            elif file_type.lower() == 'txt':
                return self._extract_from_txt(file_path)
            elif file_type.lower() in ['png', 'jpg', 'jpeg']:
                return self._extract_from_image(file_path)
            else:
                return "", False
        except Exception as e:
            print(f"Error extracting text from {file_path}: {str(e)}")
            return "", False
    
    def _extract_from_pdf(self, file_path: str) -> Tuple[str, bool]:
        """Extract text from PDF file"""
        text = ""
        try:
            # First try with PyPDF2 for text-based PDFs
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    text += page_text + "\n"
            
            # If no text extracted, try OCR
            if not text.strip():
                text = self._extract_pdf_with_ocr(file_path)
            
            return text, True
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            # Fallback to OCR
            try:
                text = self._extract_pdf_with_ocr(file_path)
                return text, True
            except:
                return "", False
    
    def _extract_pdf_with_ocr(self, file_path: str) -> str:
        """Extract text from PDF using OCR"""
        text = ""
        try:
            # Convert PDF pages to images
            images = convert_from_path(file_path)
            
            # Apply OCR to each image
            for image in images:
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
            
            return text
        except Exception as e:
            print(f"OCR extraction failed: {str(e)}")
            return ""
    
    def _extract_from_docx(self, file_path: str) -> Tuple[str, bool]:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text, True
        except Exception as e:
            print(f"Error reading DOCX: {str(e)}")
            return "", False
    
    def _extract_from_txt(self, file_path: str) -> Tuple[str, bool]:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text, True
        except Exception as e:
            print(f"Error reading TXT: {str(e)}")
            return "", False
    
    def _extract_from_image(self, file_path: str) -> Tuple[str, bool]:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text, True
        except Exception as e:
            print(f"Error reading image: {str(e)}")
            return "", False
    
    def is_supported_format(self, filename: str) -> bool:
        """Check if file format is supported"""
        file_extension = Path(filename).suffix.lower()
        return file_extension in self.supported_formats
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from filename"""
        extension = Path(filename).suffix.lower()
        if extension == '.pdf':
            return 'pdf'
        elif extension == '.docx':
            return 'docx'
        elif extension == '.txt':
            return 'txt'
        elif extension in ['.png', '.jpg', '.jpeg']:
            return 'image'
        else:
            return 'unknown'