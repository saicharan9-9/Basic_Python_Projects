from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
import os
import shutil
from typing import List

from ..models import UploadResponse, DocumentType, User, StudyMaterial
from ..database_models import Document as DBDocument
from ..services.database import get_db
from ..services.auth_service import verify_token
from ..services.text_extraction import TextExtractionService
from ..services.ai_service import AIService
from ..services.rag_service import RAGService

router = APIRouter()

# Initialize services
text_extractor = TextExtractionService()
ai_service = AIService()
rag_service = RAGService()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {
    'pdf': DocumentType.PDF,
    'jpg': DocumentType.IMAGE,
    'jpeg': DocumentType.IMAGE,
    'png': DocumentType.IMAGE,
    'tiff': DocumentType.IMAGE,
    'bmp': DocumentType.IMAGE,
    'txt': DocumentType.TEXT
}

@router.post("/document", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Upload and process a document (PDF, image, or text file)"""
    
    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS.keys())}"
        )
    
    # Generate unique document ID and file path
    document_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{document_id}_{file.filename}")
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from file
        extracted_text, page_count = text_extractor.extract_from_file(file_path, file_extension)
        
        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text could be extracted from the file"
            )
        
        # Preprocess text
        processed_text = text_extractor.preprocess_text(extracted_text)
        
        # Save document to database
        db_document = DBDocument(
            id=document_id,
            user_id=current_user.id,
            filename=file.filename,
            document_type=ALLOWED_EXTENSIONS[file_extension].value,
            extracted_text=processed_text,
            page_count=page_count,
            file_path=file_path
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Add to RAG vector database
        rag_service.add_document(
            document_id=document_id,
            text=processed_text,
            metadata={
                "filename": file.filename,
                "user_id": current_user.id,
                "document_type": ALLOWED_EXTENSIONS[file_extension].value
            }
        )
        
        return UploadResponse(
            document_id=document_id,
            filename=file.filename,
            document_type=ALLOWED_EXTENSIONS[file_extension],
            extracted_text=processed_text[:500] + "..." if len(processed_text) > 500 else processed_text,
            page_count=page_count
        )
        
    except Exception as e:
        # Clean up file if something went wrong
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

@router.post("/generate-study-material/{document_id}", response_model=StudyMaterial)
async def generate_study_material(
    document_id: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Generate flashcards and quiz from uploaded document"""
    
    # Get document
    document = db.query(DBDocument).filter(
        DBDocument.id == document_id,
        DBDocument.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        # Generate summary
        summary = ai_service.generate_summary(
            document.extracted_text, 
            current_user.preferred_language
        )
        
        # Extract key topics
        key_topics = ai_service.extract_key_topics(document.extracted_text)
        
        # Generate flashcards
        flashcards = ai_service.generate_flashcards(
            document.extracted_text,
            num_cards=15,
            language=current_user.preferred_language
        )
        
        # Generate quiz
        quiz = ai_service.generate_quiz(
            document.extracted_text,
            num_questions=10,
            language=current_user.preferred_language
        )
        
        # Update document with generated content
        document.summary = summary
        document.key_topics = key_topics
        db.commit()
        
        # Save flashcards to database
        from ..database_models import Flashcard as DBFlashcard, Quiz as DBQuiz
        
        for flashcard in flashcards:
            db_flashcard = DBFlashcard(
                id=flashcard.id,
                document_id=document_id,
                front=flashcard.front,
                back=flashcard.back,
                topic=flashcard.topic,
                difficulty=flashcard.difficulty
            )
            db.add(db_flashcard)
        
        # Save quiz to database
        db_quiz = DBQuiz(
            id=quiz.id,
            document_id=document_id,
            title=quiz.title,
            questions=[q.dict() for q in quiz.questions],
            total_questions=quiz.total_questions,
            estimated_time=quiz.estimated_time
        )
        db.add(db_quiz)
        
        db.commit()
        
        return StudyMaterial(
            document_id=document_id,
            summary=summary,
            flashcards=flashcards,
            quiz=quiz,
            key_topics=key_topics
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating study material: {str(e)}"
        )

@router.get("/documents")
async def get_user_documents(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all documents for the current user"""
    documents = db.query(DBDocument).filter(DBDocument.user_id == current_user.id).all()
    
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "document_type": doc.document_type,
            "page_count": doc.page_count,
            "created_at": doc.created_at,
            "has_study_material": bool(doc.summary)
        }
        for doc in documents
    ]

@router.delete("/document/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a document and its associated study materials"""
    document = db.query(DBDocument).filter(
        DBDocument.id == document_id,
        DBDocument.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        # Remove from RAG database
        rag_service.remove_document(document_id)
        
        # Delete file from filesystem
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database (cascading will handle related records)
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting document: {str(e)}"
        )