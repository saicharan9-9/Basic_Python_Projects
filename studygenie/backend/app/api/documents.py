import os
import uuid
import aiofiles
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.document import Document
from app.api.auth import get_current_user
from app.services.document_processor import DocumentProcessor
from app.services.ai_service import AIService

router = APIRouter()
document_processor = DocumentProcessor()
ai_service = AIService()

# Pydantic models
class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    processing_status: str
    language: str
    created_at: str

class DocumentWithText(DocumentResponse):
    extracted_text: str

# Background task for processing documents
async def process_document_background(document_id: int, file_path: str, file_type: str):
    """Background task to extract text from uploaded document"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Get document from database
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return
        
        # Update status to processing
        document.processing_status = "processing"
        db.commit()
        
        # Extract text
        extracted_text, success = document_processor.extract_text(file_path, file_type)
        
        if success and extracted_text.strip():
            document.extracted_text = extracted_text
            document.processing_status = "completed"
        else:
            document.processing_status = "failed"
        
        db.commit()
        
    except Exception as e:
        print(f"Error processing document {document_id}: {str(e)}")
        if document:
            document.processing_status = "failed"
            db.commit()
    finally:
        db.close()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not document_processor.is_supported_format(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported formats: {document_processor.supported_formats}"
        )
    
    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Create upload directory if it doesn't exist
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    # Create database record
    file_type = document_processor.get_file_type(file.filename)
    document = Document(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file_type,
        owner_id=current_user.id,
        processing_status="pending"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Start background processing
    background_tasks.add_task(
        process_document_background,
        document.id,
        file_path,
        file_type
    )
    
    return document

@router.get("/", response_model=List[DocumentResponse])
async def get_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents for the current user"""
    documents = db.query(Document).filter(Document.owner_id == current_user.id).all()
    return documents

@router.get("/{document_id}", response_model=DocumentWithText)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific document with extracted text"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.post("/{document_id}/reprocess")
async def reprocess_document(
    document_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reprocess a document to extract text again"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Reset processing status
    document.processing_status = "pending"
    document.extracted_text = None
    db.commit()
    
    # Start background processing
    background_tasks.add_task(
        process_document_background,
        document.id,
        document.file_path,
        document.file_type
    )
    
    return {"message": "Document reprocessing started"}