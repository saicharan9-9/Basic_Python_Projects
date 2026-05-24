import PyPDF2
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import os
from typing import Optional
import io

class PDFService:
    def __init__(self):
        # Set tesseract path for OCR
        try:
            # For Linux, tesseract is usually in PATH
            pytesseract.pytesseract.tesseract_cmd = 'tesseract'
        except:
            pass
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF with fallback to OCR if needed"""
        try:
            # Try PyMuPDF first (better text extraction)
            text = self._extract_with_pymupdf(file_path)
            if text.strip():
                return text
            
            # Fallback to PyPDF2
            text = self._extract_with_pypdf2(file_path)
            if text.strip():
                return text
            
            # If no text found, try OCR
            return self._extract_with_ocr(file_path)
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            # Final fallback to OCR
            return self._extract_with_ocr(file_path)
    
    def _extract_with_pymupdf(self, file_path: str) -> str:
        """Extract text using PyMuPDF (fitz)"""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text.strip()
            
        except Exception as e:
            print(f"PyMuPDF extraction failed: {e}")
            return ""
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip()
                
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            return ""
    
    def _extract_with_ocr(self, file_path: str) -> str:
        """Extract text using OCR (for handwritten notes or scanned PDFs)"""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Convert page to image
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Extract text using OCR
                page_text = pytesseract.image_to_string(img, lang='eng')
                text += page_text + "\n"
            
            doc.close()
            return text.strip()
            
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return "Text extraction failed. Please check if the PDF contains readable text."
    
    def extract_images(self, file_path: str) -> list:
        """Extract images from PDF for potential OCR processing"""
        try:
            doc = fitz.open(file_path)
            images = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Convert to PIL Image
                    image = Image.open(io.BytesIO(image_bytes))
                    images.append({
                        'page': page_num + 1,
                        'index': img_index,
                        'image': image,
                        'size': image.size
                    })
            
            doc.close()
            return images
            
        except Exception as e:
            print(f"Error extracting images: {e}")
            return []
    
    def get_pdf_info(self, file_path: str) -> dict:
        """Get basic information about the PDF"""
        try:
            doc = fitz.open(file_path)
            info = {
                'num_pages': len(doc),
                'file_size': os.path.getsize(file_path),
                'title': doc.metadata.get('title', ''),
                'author': doc.metadata.get('author', ''),
                'subject': doc.metadata.get('subject', ''),
                'creator': doc.metadata.get('creator', '')
            }
            doc.close()
            return info
            
        except Exception as e:
            print(f"Error getting PDF info: {e}")
            return {}
    
    def is_scanned_pdf(self, file_path: str) -> bool:
        """Check if PDF is scanned (image-based)"""
        try:
            text = self._extract_with_pymupdf(file_path)
            # If very little text is extracted, it's likely scanned
            return len(text.strip()) < 100
            
        except Exception:
            return True
    
    def optimize_for_ocr(self, file_path: str) -> str:
        """Optimize PDF for better OCR results"""
        try:
            doc = fitz.open(file_path)
            optimized_text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Get page as image with higher resolution
                mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Preprocess image for better OCR
                # Convert to grayscale
                if img.mode != 'L':
                    img = img.convert('L')
                
                # Extract text with optimized settings
                page_text = pytesseract.image_to_string(
                    img, 
                    lang='eng',
                    config='--psm 6 --oem 3'  # Page segmentation mode 6, OCR Engine mode 3
                )
                
                optimized_text += page_text + "\n"
            
            doc.close()
            return optimized_text.strip()
            
        except Exception as e:
            print(f"OCR optimization failed: {e}")
            return self._extract_with_ocr(file_path)