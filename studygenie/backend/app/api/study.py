from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.study_material import StudyMaterial, Quiz, Question, Flashcard
from app.api.auth import get_current_user
from app.services.ai_service import AIService
from app.services.spaced_repetition import SpacedRepetitionService

router = APIRouter()
ai_service = AIService()
spaced_repetition = SpacedRepetitionService()

# Pydantic models
class StudyMaterialCreate(BaseModel):
    document_id: int
    content_type: str  # summary, quiz, flashcard
    language: str = "en"
    difficulty_level: str = "medium"
    subject: Optional[str] = None

class StudyMaterialResponse(BaseModel):
    id: int
    title: str
    content_type: str
    content: Optional[str]
    language: str
    difficulty_level: str
    subject: Optional[str]
    created_at: datetime

class QuizResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    total_questions: int
    time_limit: Optional[int]
    questions: List[dict]

class FlashcardResponse(BaseModel):
    id: int
    front_text: str
    back_text: str
    difficulty: str
    next_review: Optional[datetime]
    review_interval: int
    ease_factor: str
    review_count: int

class FlashcardReview(BaseModel):
    flashcard_id: int
    correct: bool
    confidence: str = "medium"  # low, medium, high

# Background task for generating study materials
async def generate_study_material_background(material_id: int):
    """Background task to generate study content using AI"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        material = db.query(StudyMaterial).filter(StudyMaterial.id == material_id).first()
        if not material or not material.document:
            return
        
        extracted_text = material.document.extracted_text
        if not extracted_text:
            return
        
        # Generate content based on type
        if material.content_type == "summary":
            content = await ai_service.generate_summary(
                extracted_text, 
                material.language
            )
            material.content = content
            material.title = f"Summary - {material.document.original_filename}"
        
        elif material.content_type == "quiz":
            questions_data = await ai_service.generate_quiz(
                extracted_text, 
                num_questions=10, 
                language=material.language
            )
            
            if questions_data:
                # Create quiz record
                quiz = Quiz(
                    title=f"Quiz - {material.document.original_filename}",
                    description=f"Auto-generated quiz from {material.document.original_filename}",
                    total_questions=len(questions_data),
                    study_material_id=material.id
                )
                db.add(quiz)
                db.commit()
                db.refresh(quiz)
                
                # Create questions
                for q_data in questions_data:
                    question = Question(
                        question_text=q_data.get("question", ""),
                        question_type="mcq",
                        options=q_data.get("options", []),
                        correct_answer=q_data.get("correct_answer", ""),
                        explanation=q_data.get("explanation", ""),
                        difficulty=q_data.get("difficulty", "medium"),
                        quiz_id=quiz.id
                    )
                    db.add(question)
                
                material.title = quiz.title
                material.content = f"Quiz with {len(questions_data)} questions"
        
        elif material.content_type == "flashcard":
            flashcards_data = await ai_service.generate_flashcards(
                extracted_text,
                num_cards=15,
                language=material.language
            )
            
            if flashcards_data:
                for card_data in flashcards_data:
                    flashcard = Flashcard(
                        front_text=card_data.get("front", ""),
                        back_text=card_data.get("back", ""),
                        difficulty=card_data.get("difficulty", "medium"),
                        next_review=datetime.utcnow(),
                        study_material_id=material.id
                    )
                    db.add(flashcard)
                
                material.title = f"Flashcards - {material.document.original_filename}"
                material.content = f"{len(flashcards_data)} flashcards created"
        
        db.commit()
        
    except Exception as e:
        print(f"Error generating study material {material_id}: {str(e)}")
    finally:
        db.close()

@router.post("/generate", response_model=StudyMaterialResponse)
async def generate_study_material(
    material_data: StudyMaterialCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate study material from a document"""
    
    # Verify document exists and belongs to user
    document = db.query(Document).filter(
        Document.id == material_data.document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.processing_status != "completed":
        raise HTTPException(
            status_code=400, 
            detail="Document is still being processed or failed to process"
        )
    
    # Create study material record
    study_material = StudyMaterial(
        title=f"Generating {material_data.content_type}...",
        content_type=material_data.content_type,
        language=material_data.language,
        difficulty_level=material_data.difficulty_level,
        subject=material_data.subject,
        user_id=current_user.id,
        document_id=document.id
    )
    
    db.add(study_material)
    db.commit()
    db.refresh(study_material)
    
    # Start background generation
    background_tasks.add_task(
        generate_study_material_background,
        study_material.id
    )
    
    return study_material

@router.get("/", response_model=List[StudyMaterialResponse])
async def get_study_materials(
    content_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all study materials for the current user"""
    query = db.query(StudyMaterial).filter(StudyMaterial.user_id == current_user.id)
    
    if content_type:
        query = query.filter(StudyMaterial.content_type == content_type)
    
    materials = query.order_by(StudyMaterial.created_at.desc()).all()
    return materials

@router.get("/{material_id}", response_model=StudyMaterialResponse)
async def get_study_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific study material"""
    material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Study material not found")
    
    return material

@router.get("/{material_id}/quiz", response_model=QuizResponse)
async def get_quiz(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get quiz for a study material"""
    material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id,
        StudyMaterial.content_type == "quiz"
    ).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz = db.query(Quiz).filter(Quiz.study_material_id == material_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get questions
    questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
    questions_data = []
    for q in questions:
        questions_data.append({
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": q.options,
            "difficulty": q.difficulty
        })
    
    return {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "total_questions": quiz.total_questions,
        "time_limit": quiz.time_limit,
        "questions": questions_data
    }

@router.get("/{material_id}/flashcards", response_model=List[FlashcardResponse])
async def get_flashcards(
    material_id: int,
    due_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get flashcards for a study material"""
    material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id,
        StudyMaterial.content_type == "flashcard"
    ).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Flashcard set not found")
    
    query = db.query(Flashcard).filter(Flashcard.study_material_id == material_id)
    
    if due_only:
        now = datetime.utcnow()
        query = query.filter(
            (Flashcard.next_review.is_(None)) | 
            (Flashcard.next_review <= now)
        )
    
    flashcards = query.all()
    return flashcards

@router.post("/flashcards/review")
async def review_flashcard(
    review_data: FlashcardReview,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Review a flashcard and update spaced repetition schedule"""
    
    # Get flashcard
    flashcard = db.query(Flashcard).join(StudyMaterial).filter(
        Flashcard.id == review_data.flashcard_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    # Convert performance to quality score
    quality = spaced_repetition.quality_from_performance(
        review_data.correct,
        review_data.confidence
    )
    
    # Calculate next review
    result = spaced_repetition.calculate_next_review(
        current_ease_factor=float(flashcard.ease_factor),
        current_interval=flashcard.review_interval,
        quality=quality,
        review_count=flashcard.review_count
    )
    
    # Update flashcard
    flashcard.next_review = result["next_review_date"]
    flashcard.review_interval = result["next_interval"]
    flashcard.ease_factor = str(result["next_ease_factor"])
    flashcard.review_count += 1
    
    db.commit()
    
    return {
        "message": "Flashcard reviewed successfully",
        "next_review": result["next_review_date"],
        "interval": result["next_interval"]
    }

@router.delete("/{material_id}")
async def delete_study_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a study material"""
    material = db.query(StudyMaterial).filter(
        StudyMaterial.id == material_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Study material not found")
    
    db.delete(material)
    db.commit()
    
    return {"message": "Study material deleted successfully"}