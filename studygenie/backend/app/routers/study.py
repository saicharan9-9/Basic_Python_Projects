from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..models import (
    User, QuizAttempt, QuizResult, TutorQuestion, TutorResponse,
    StudySession, Flashcard
)
from ..database_models import (
    Quiz as DBQuiz, QuizAttempt as DBQuizAttempt, 
    Flashcard as DBFlashcard, Document as DBDocument,
    StudySession as DBStudySession
)
from ..services.database import get_db
from ..services.auth_service import verify_token
from ..services.ai_service import AIService
from ..services.rag_service import RAGService
from ..services.spaced_repetition import SpacedRepetitionService

router = APIRouter()

# Initialize services
ai_service = AIService()
rag_service = RAGService()

@router.get("/quiz/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get a specific quiz"""
    quiz = db.query(DBQuiz).join(DBDocument).filter(
        DBQuiz.id == quiz_id,
        DBDocument.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return {
        "id": quiz.id,
        "title": quiz.title,
        "questions": quiz.questions,
        "total_questions": quiz.total_questions,
        "estimated_time": quiz.estimated_time
    }

@router.post("/quiz/{quiz_id}/attempt", response_model=QuizResult)
async def submit_quiz_attempt(
    quiz_id: str,
    attempt: QuizAttempt,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Submit quiz attempt and get results"""
    quiz = db.query(DBQuiz).join(DBDocument).filter(
        DBQuiz.id == quiz_id,
        DBDocument.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Calculate score
    correct_answers = 0
    weak_topics = []
    strong_topics = []
    topic_performance = {}
    
    for question in quiz.questions:
        question_id = question["id"]
        user_answer = attempt.answers.get(question_id, "")
        correct_answer = question["correct_answer"]
        topic = question["topic"]
        
        is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
        
        if is_correct:
            correct_answers += 1
            if topic not in topic_performance:
                topic_performance[topic] = {"correct": 0, "total": 0}
            topic_performance[topic]["correct"] += 1
        
        if topic not in topic_performance:
            topic_performance[topic] = {"correct": 0, "total": 0}
        topic_performance[topic]["total"] += 1
    
    # Determine weak and strong topics
    for topic, performance in topic_performance.items():
        accuracy = performance["correct"] / performance["total"]
        if accuracy < 0.6:
            weak_topics.append(topic)
        elif accuracy >= 0.8:
            strong_topics.append(topic)
    
    score = (correct_answers / quiz.total_questions) * 100
    
    # Save quiz attempt
    db_attempt = DBQuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        answers=attempt.answers,
        score=score,
        total_questions=quiz.total_questions,
        correct_answers=correct_answers,
        weak_topics=weak_topics,
        strong_topics=strong_topics
    )
    
    db.add(db_attempt)
    db.commit()
    
    return QuizResult(
        quiz_id=quiz_id,
        score=score,
        total_questions=quiz.total_questions,
        correct_answers=correct_answers,
        time_taken=0,  # Would need frontend to track this
        weak_topics=weak_topics,
        strong_topics=strong_topics
    )

@router.get("/flashcards/due")
async def get_due_flashcards(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get flashcards due for review"""
    query_func = SpacedRepetitionService.get_due_flashcards_query(current_user.id)
    due_cards = query_func(db).limit(20).all()  # Limit to 20 cards per session
    
    return [
        {
            "id": card.id,
            "front": card.front,
            "back": card.back,
            "topic": card.topic,
            "difficulty": card.difficulty,
            "repetitions": card.repetitions,
            "ease_factor": card.ease_factor
        }
        for card in due_cards
    ]

@router.post("/flashcard/{flashcard_id}/review")
async def review_flashcard(
    flashcard_id: str,
    quality: int,  # 0-5 scale
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Submit flashcard review with quality rating"""
    if quality < 0 or quality > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quality must be between 0 and 5"
        )
    
    try:
        updated_card = SpacedRepetitionService.update_flashcard_review(
            flashcard_id=flashcard_id,
            quality=quality,
            db_session=db
        )
        
        return {
            "message": "Review recorded successfully",
            "next_review": updated_card.next_review,
            "new_interval": updated_card.interval,
            "ease_factor": updated_card.ease_factor
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/tutor/ask", response_model=TutorResponse)
async def ask_tutor(
    question_data: TutorQuestion,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Ask the AI tutor a question about study materials"""
    
    # Verify document belongs to user if document_id is provided
    if question_data.document_id:
        document = db.query(DBDocument).filter(
            DBDocument.id == question_data.document_id,
            DBDocument.user_id == current_user.id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
    
    try:
        response = rag_service.answer_question(
            question=question_data.question,
            document_id=question_data.document_id,
            language=question_data.language
        )
        
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )

@router.post("/session/start")
async def start_study_session(
    session_data: StudySession,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Start a new study session"""
    
    # Verify document belongs to user
    document = db.query(DBDocument).filter(
        DBDocument.id == session_data.document_id,
        DBDocument.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Create study session
    db_session = DBStudySession(
        user_id=current_user.id,
        document_id=session_data.document_id,
        session_type=session_data.session_type,
        duration=session_data.duration,
        score=session_data.score
    )
    
    db.add(db_session)
    db.commit()
    
    return {"message": "Study session recorded", "session_id": db_session.id}

@router.get("/flashcards/stats")
async def get_flashcard_stats(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get spaced repetition statistics"""
    stats = SpacedRepetitionService.get_study_statistics(current_user.id, db)
    return stats

@router.get("/quiz/{quiz_id}/explain/{question_id}")
async def explain_wrong_answer(
    quiz_id: str,
    question_id: str,
    user_answer: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get explanation for a wrong answer"""
    quiz = db.query(DBQuiz).join(DBDocument).filter(
        DBQuiz.id == quiz_id,
        DBDocument.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Find the specific question
    question = None
    for q in quiz.questions:
        if q["id"] == question_id:
            question = q
            break
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    try:
        explanation = ai_service.explain_answer(
            question=question["question_text"],
            correct_answer=question["correct_answer"],
            user_answer=user_answer,
            language=current_user.preferred_language
        )
        
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating explanation: {str(e)}"
        )