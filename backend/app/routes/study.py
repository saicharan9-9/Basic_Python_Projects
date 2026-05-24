from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
from datetime import datetime

from database.database import get_db, User, StudyMaterial, Quiz, Flashcard
from app.routes.auth import get_current_user
from services.ai_service import AIService
from services.pdf_service import PDFService
from utils.config import settings

router = APIRouter()
ai_service = AIService()
pdf_service = PDFService()

# Pydantic models
class StudyMaterialResponse(BaseModel):
    id: int
    title: str
    content_type: str
    summary: Optional[str]
    language: str
    created_at: datetime

    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    id: int
    title: str
    total_questions: int
    created_at: datetime

    class Config:
        from_attributes = True

class FlashcardResponse(BaseModel):
    id: int
    front_content: str
    back_content: str
    difficulty: str
    review_count: int

    class Config:
        from_attributes = True

# Routes
@router.post("/upload", response_model=StudyMaterialResponse)
async def upload_study_material(
    file: UploadFile = File(...),
    title: str = Form(...),
    language: str = Form(default="en"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{current_user.id}_{datetime.now().timestamp()}_{file.filename}")
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Extract text from PDF
        extracted_text = pdf_service.extract_text(file_path)
        
        # Generate AI summary
        summary = ai_service.generate_summary(extracted_text, language)
        
        # Create study material record
        study_material = StudyMaterial(
            user_id=current_user.id,
            title=title,
            content_type="pdf",
            file_path=file_path,
            extracted_text=extracted_text,
            summary=summary,
            language=language
        )
        
        db.add(study_material)
        db.commit()
        db.refresh(study_material)
        
        return study_material
        
    except Exception as e:
        # Clean up file if processing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/{material_id}/generate-quiz", response_model=QuizResponse)
async def generate_quiz(
    material_id: int,
    num_questions: int = Form(default=10),
    language: str = Form(default="en"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get study material
    study_material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not study_material:
        raise HTTPException(status_code=404, detail="Study material not found")
    
    try:
        # Generate quiz questions using AI
        questions = ai_service.generate_quiz_questions(
            study_material.extracted_text,
            num_questions,
            language
        )
        
        # Create quiz record
        quiz = Quiz(
            user_id=current_user.id,
            study_material_id=material_id,
            title=f"Quiz: {study_material.title}",
            questions=json.dumps(questions),
            total_questions=num_questions
        )
        
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        
        return quiz
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@router.post("/{material_id}/generate-flashcards", response_model=List[FlashcardResponse])
async def generate_flashcards(
    material_id: int,
    num_cards: int = Form(default=15),
    language: str = Form(default="en"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get study material
    study_material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not study_material:
        raise HTTPException(status_code=404, detail="Study material not found")
    
    try:
        # Generate flashcards using AI
        flashcard_data = ai_service.generate_flashcards(
            study_material.extracted_text,
            num_cards,
            language
        )
        
        flashcards = []
        for card_data in flashcard_data:
            flashcard = Flashcard(
                user_id=current_user.id,
                study_material_id=material_id,
                front_content=card_data["front"],
                back_content=card_data["back"],
                difficulty=card_data.get("difficulty", "medium")
            )
            flashcards.append(flashcard)
        
        db.add_all(flashcards)
        db.commit()
        
        return flashcards
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating flashcards: {str(e)}")

@router.get("/materials", response_model=List[StudyMaterialResponse])
async def get_study_materials(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    materials = db.query(StudyMaterial).filter(
        StudyMaterial.user_id == current_user.id
    ).order_by(StudyMaterial.created_at.desc()).all()
    
    return materials

@router.get("/materials/{material_id}", response_model=StudyMaterialResponse)
async def get_study_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Study material not found")
    
    return material

@router.get("/materials/{material_id}/quizzes", response_model=List[QuizResponse])
async def get_material_quizzes(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quizzes = db.query(Quiz).filter(
        Quiz.study_material_id == material_id,
        Quiz.user_id == current_user.id
    ).order_by(Quiz.created_at.desc()).all()
    
    return quizzes

@router.get("/materials/{material_id}/flashcards", response_model=List[FlashcardResponse])
async def get_material_flashcards(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    flashcards = db.query(Flashcard).filter(
        Flashcard.study_material_id == material_id,
        Flashcard.user_id == current_user.id
    ).all()
    
    return flashcards

@router.delete("/materials/{material_id}")
async def delete_study_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Study material not found")
    
    # Delete associated file
    if material.file_path and os.path.exists(material.file_path):
        os.remove(material.file_path)
    
    # Delete from database
    db.delete(material)
    db.commit()
    
    return {"message": "Study material deleted successfully"}