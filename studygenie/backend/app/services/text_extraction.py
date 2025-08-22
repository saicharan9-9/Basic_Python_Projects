import PyPDF2
import pytesseract
from PIL import Image
import io
import os
from typing import Tuple, Optional

class TextExtractionService:
    def __init__(self):
        # Configure tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        pass
    
    def extract_from_pdf(self, file_path: str) -> Tuple[str, int]:
        """Extract text from PDF file and return text and page count"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                page_count = len(pdf_reader.pages)
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip(), page_count
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_from_image(self, file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            # Open image
            image = Image.open(file_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image, lang='eng+hin+mar')
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_from_file(self, file_path: str, file_type: str) -> Tuple[str, Optional[int]]:
        """Extract text from file based on type"""
        if file_type.lower() == 'pdf':
            text, page_count = self.extract_from_pdf(file_path)
            return text, page_count
        elif file_type.lower() in ['jpg', 'jpeg', 'png', 'tiff', 'bmp']:
            text = self.extract_from_image(file_path)
            return text, None
        elif file_type.lower() == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text, None
        else:
            raise Exception(f"Unsupported file type: {file_type}")
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess extracted text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters that might interfere with processing
        # Keep basic punctuation for context
        import re
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\']+', ' ', text)
        
        return text.strip()