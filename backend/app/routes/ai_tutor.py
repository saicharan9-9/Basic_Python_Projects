from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from database.database import get_db, User, StudyMaterial
from app.routes.auth import get_current_user
from services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    material_id: Optional[int] = None
    language: str = "en"

class AnswerResponse(BaseModel):
    answer: str
    confidence: float
    source_material: Optional[str] = None
    related_questions: List[str] = []

class TranslationRequest(BaseModel):
    content: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_content: str
    original_language: str
    target_language: str

# Routes
@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    question_request: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask a question to the AI tutor"""
    try:
        context = ""
        source_material = None
        
        # If material_id is provided, use that material as context
        if question_request.material_id:
            material = db.query(StudyMaterial).filter(
                StudyMaterial.id == question_request.material_id,
                StudyMaterial.user_id == current_user.id
            ).first()
            
            if material:
                context = material.extracted_text
                source_material = material.title
            else:
                raise HTTPException(status_code=404, detail="Study material not found")
        else:
            # Use all user's study materials as context
            materials = db.query(StudyMaterial).filter(
                StudyMaterial.user_id == current_user.id
            ).all()
            
            if materials:
                context = "\n\n".join([m.extracted_text for m in materials])
                source_material = "Multiple study materials"
            else:
                # No study materials, provide general educational context
                context = "General educational knowledge"
                source_material = "General knowledge"
        
        # Get answer from AI service
        answer = ai_service.answer_question(
            question_request.question,
            context,
            question_request.language
        )
        
        # Generate related questions for better learning
        related_questions = ai_service.generate_related_questions(
            question_request.question,
            context,
            question_request.language
        )
        
        return AnswerResponse(
            answer=answer,
            confidence=0.85,  # Mock confidence score
            source_material=source_material,
            related_questions=related_questions[:3]  # Limit to 3 related questions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@router.post("/translate", response_model=TranslationResponse)
async def translate_content(
    translation_request: TranslationRequest,
    current_user: User = Depends(get_current_user)
):
    """Translate content to target language"""
    try:
        translated_content = ai_service.translate_content(
            translation_request.content,
            translation_request.target_language
        )
        
        return TranslationResponse(
            translated_content=translated_content,
            original_language="en",  # Assuming original is English
            target_language=translation_request.target_language
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error translating content: {str(e)}")

@router.post("/explain-concept")
async def explain_concept(
    concept: str = Form(...),
    material_id: int = Form(...),
    language: str = Form(default="en"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed explanation of a concept from study material"""
    try:
        material = db.query(StudyMaterial).filter(
            StudyMaterial.id == material_id,
            StudyMaterial.user_id == current_user.id
        ).first()
        
        if not material:
            raise HTTPException(status_code=404, detail="Study material not found")
        
        # Generate explanation using AI
        explanation = ai_service.explain_concept(
            concept,
            material.extracted_text,
            language
        )
        
        return {
            "concept": concept,
            "explanation": explanation,
            "source_material": material.title,
            "language": language
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining concept: {str(e)}")

@router.post("/generate-practice-questions")
async def generate_practice_questions(
    material_id: int = Form(...),
    num_questions: int = Form(default=5),
    difficulty: str = Form(default="medium"),
    language: str = Form(default="en"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate additional practice questions for a specific topic"""
    try:
        material = db.query(StudyMaterial).filter(
            StudyMaterial.id == material_id,
            StudyMaterial.user_id == current_user.id
        ).first()
        
        if not material:
            raise HTTPException(status_code=404, detail="Study material not found")
        
        # Generate practice questions using AI
        questions = ai_service.generate_practice_questions(
            material.extracted_text,
            num_questions,
            difficulty,
            language
        )
        
        return {
            "material_id": material_id,
            "questions": questions,
            "difficulty": difficulty,
            "language": language
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating practice questions: {str(e)}")

@router.get("/learning-suggestions")
async def get_learning_suggestions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized learning suggestions based on study materials"""
    try:
        materials = db.query(StudyMaterial).filter(
            StudyMaterial.user_id == current_user.id
        ).all()
        
        if not materials:
            return {
                "suggestions": [
                    "Upload your first study material to get started!",
                    "Try different types of content (PDFs, notes, etc.)",
                    "Set your preferred language for personalized learning"
                ]
            }
        
        # Generate learning suggestions using AI
        suggestions = ai_service.generate_learning_suggestions(
            [m.title for m in materials],
            current_user.preferred_language
        )
        
        return {
            "suggestions": suggestions,
            "total_materials": len(materials),
            "languages_used": list(set([m.language for m in materials]))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.post("/summarize-topic")
async def summarize_topic(
    topic: str = Form(...),
    material_ids: List[int] = Form(...),
    language: str = Form(default="en"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a comprehensive summary of a topic across multiple materials"""
    try:
        materials = db.query(StudyMaterial).filter(
            StudyMaterial.id.in_(material_ids),
            StudyMaterial.user_id == current_user.id
        ).all()
        
        if not materials:
            raise HTTPException(status_code=404, detail="No study materials found")
        
        # Combine text from all materials
        combined_text = "\n\n".join([m.extracted_text for m in materials])
        
        # Generate topic summary using AI
        summary = ai_service.generate_topic_summary(
            topic,
            combined_text,
            language
        )
        
        return {
            "topic": topic,
            "summary": summary,
            "source_materials": [m.title for m in materials],
            "language": language
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing topic: {str(e)}")

@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages for translation and content generation"""
    return {
        "languages": [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "hi", "name": "Hindi", "native_name": "हिंदी"},
            {"code": "mr", "name": "Marathi", "native_name": "मराठी"},
            {"code": "bn", "name": "Bengali", "native_name": "বাংলা"},
            {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"},
            {"code": "te", "name": "Telugu", "native_name": "తెలుగు"},
            {"code": "kn", "name": "Kannada", "native_name": "ಕನ್ನಡ"},
            {"code": "ml", "name": "Malayalam", "native_name": "മലയാളം"},
            {"code": "gu", "name": "Gujarati", "native_name": "ગુજરાતી"},
            {"code": "pa", "name": "Punjabi", "native_name": "ਪੰਜਾਬੀ"}
        ]
    }