from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.user import User
from app.models.progress import UserProgress, StudySession, QuizAttempt
from app.models.study_material import Quiz, Question, Flashcard, StudyMaterial
from app.api.auth import get_current_user

router = APIRouter()

# Pydantic models
class ProgressResponse(BaseModel):
    subject: str
    total_study_time: int
    quiz_scores: List[float]
    flashcard_mastery: float
    weak_topics: List[str]
    strong_topics: List[str]
    study_streak: int
    last_study_date: datetime

class StudySessionCreate(BaseModel):
    session_type: str  # quiz, flashcard, reading
    duration: int  # minutes
    items_studied: int
    correct_answers: int
    total_answers: int
    subject: str

class QuizAttemptCreate(BaseModel):
    quiz_id: int
    answers: Dict[int, str]  # question_id: answer
    time_taken: int  # seconds

class DashboardStats(BaseModel):
    total_study_time: int
    study_streak: int
    total_flashcards: int
    mastered_flashcards: int
    quiz_average: float
    recent_activity: List[Dict[str, Any]]
    subject_progress: Dict[str, Dict[str, Any]]

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard statistics"""
    
    # Calculate total study time
    total_study_time = db.query(func.sum(StudySession.duration)).filter(
        StudySession.user_id == current_user.id
    ).scalar() or 0
    
    # Calculate study streak
    user_progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).first()
    study_streak = user_progress.study_streak if user_progress else 0
    
    # Flashcard statistics
    flashcards = db.query(Flashcard).join(StudyMaterial).filter(
        StudyMaterial.user_id == current_user.id
    ).all()
    
    total_flashcards = len(flashcards)
    mastered_flashcards = sum(1 for f in flashcards if f.review_interval > 21)
    
    # Quiz average
    recent_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.completed == True
    ).order_by(QuizAttempt.completed_at.desc()).limit(10).all()
    
    quiz_average = 0.0
    if recent_attempts:
        quiz_average = sum(attempt.score for attempt in recent_attempts) / len(recent_attempts)
    
    # Recent activity
    recent_sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id
    ).order_by(StudySession.started_at.desc()).limit(5).all()
    
    recent_activity = []
    for session in recent_sessions:
        recent_activity.append({
            "type": session.session_type,
            "date": session.started_at.isoformat(),
            "duration": session.duration,
            "subject": session.subject,
            "accuracy": (session.correct_answers / session.total_answers * 100) if session.total_answers > 0 else 0
        })
    
    # Subject progress
    subject_progress = {}
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    
    for progress in progress_records:
        subject_progress[progress.subject] = {
            "study_time": progress.total_study_time,
            "quiz_scores": progress.quiz_scores,
            "flashcard_mastery": progress.flashcard_mastery,
            "weak_topics": progress.weak_topics,
            "strong_topics": progress.strong_topics
        }
    
    return DashboardStats(
        total_study_time=total_study_time,
        study_streak=study_streak,
        total_flashcards=total_flashcards,
        mastered_flashcards=mastered_flashcards,
        quiz_average=quiz_average,
        recent_activity=recent_activity,
        subject_progress=subject_progress
    )

@router.post("/session")
async def log_study_session(
    session_data: StudySessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a completed study session"""
    
    # Create study session record
    session = StudySession(
        user_id=current_user.id,
        session_type=session_data.session_type,
        duration=session_data.duration,
        items_studied=session_data.items_studied,
        correct_answers=session_data.correct_answers,
        total_answers=session_data.total_answers,
        subject=session_data.subject,
        ended_at=datetime.utcnow()
    )
    
    db.add(session)
    
    # Update or create user progress
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.subject == session_data.subject
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            subject=session_data.subject,
            total_study_time=0,
            quiz_scores=[],
            weak_topics=[],
            strong_topics=[]
        )
        db.add(progress)
    
    # Update progress
    progress.total_study_time += session_data.duration
    progress.last_study_date = datetime.utcnow()
    
    # Update study streak
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    today = datetime.utcnow().date()
    
    if progress.last_study_date and progress.last_study_date.date() == yesterday:
        progress.study_streak += 1
    elif not progress.last_study_date or progress.last_study_date.date() < yesterday:
        progress.study_streak = 1
    # If studied today already, don't change streak
    
    # Calculate flashcard mastery for this subject
    if session_data.session_type == "flashcard":
        accuracy = (session_data.correct_answers / session_data.total_answers * 100) if session_data.total_answers > 0 else 0
        progress.flashcard_mastery = (progress.flashcard_mastery + accuracy) / 2
    
    db.commit()
    
    return {"message": "Study session logged successfully"}

@router.post("/quiz-attempt")
async def submit_quiz_attempt(
    attempt_data: QuizAttemptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a quiz attempt and calculate score"""
    
    # Verify quiz exists and get questions
    quiz = db.query(Quiz).join(StudyMaterial).filter(
        Quiz.id == attempt_data.quiz_id,
        StudyMaterial.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
    
    # Calculate score
    correct_answers = 0
    total_questions = len(questions)
    detailed_results = []
    
    for question in questions:
        user_answer = attempt_data.answers.get(question.id, "")
        is_correct = user_answer == question.correct_answer
        
        if is_correct:
            correct_answers += 1
        
        detailed_results.append({
            "question_id": question.id,
            "question_text": question.question_text,
            "user_answer": user_answer,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
            "explanation": question.explanation
        })
    
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Create quiz attempt record
    quiz_attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=attempt_data.quiz_id,
        score=score,
        time_taken=attempt_data.time_taken,
        answers=attempt_data.answers,
        completed=True,
        completed_at=datetime.utcnow()
    )
    
    db.add(quiz_attempt)
    
    # Update user progress
    subject = quiz.study_material.subject or "General"
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.subject == subject
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            subject=subject,
            quiz_scores=[],
            weak_topics=[],
            strong_topics=[]
        )
        db.add(progress)
    
    # Add score to history
    quiz_scores = progress.quiz_scores or []
    quiz_scores.append(score)
    if len(quiz_scores) > 20:  # Keep only last 20 scores
        quiz_scores = quiz_scores[-20:]
    progress.quiz_scores = quiz_scores
    
    # Identify weak topics (questions answered incorrectly)
    weak_topics = progress.weak_topics or []
    strong_topics = progress.strong_topics or []
    
    for result in detailed_results:
        question = next(q for q in questions if q.id == result["question_id"])
        topic = question.question_text[:50]  # Use first 50 chars as topic identifier
        
        if not result["is_correct"] and topic not in weak_topics:
            weak_topics.append(topic)
        elif result["is_correct"] and topic in weak_topics:
            weak_topics.remove(topic)
            if topic not in strong_topics:
                strong_topics.append(topic)
    
    progress.weak_topics = weak_topics[-10:]  # Keep only last 10 weak topics
    progress.strong_topics = strong_topics[-10:]  # Keep only last 10 strong topics
    
    db.commit()
    
    return {
        "score": score,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "detailed_results": detailed_results,
        "message": f"Quiz completed! Score: {score:.1f}%"
    }

@router.get("/", response_model=List[ProgressResponse])
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all progress records for the current user"""
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    
    return progress_records

@router.get("/{subject}")
async def get_subject_progress(
    subject: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed progress for a specific subject"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.subject == subject
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="No progress found for this subject")
    
    # Get recent study sessions for this subject
    recent_sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.subject == subject
    ).order_by(StudySession.started_at.desc()).limit(10).all()
    
    # Get recent quiz attempts for this subject
    recent_quizzes = db.query(QuizAttempt).join(Quiz).join(StudyMaterial).filter(
        StudyMaterial.user_id == current_user.id,
        StudyMaterial.subject == subject,
        QuizAttempt.completed == True
    ).order_by(QuizAttempt.completed_at.desc()).limit(5).all()
    
    return {
        "progress": progress,
        "recent_sessions": [
            {
                "type": s.session_type,
                "date": s.started_at.isoformat(),
                "duration": s.duration,
                "accuracy": (s.correct_answers / s.total_answers * 100) if s.total_answers > 0 else 0
            }
            for s in recent_sessions
        ],
        "recent_quizzes": [
            {
                "quiz_title": q.quiz.title,
                "score": q.score,
                "date": q.completed_at.isoformat(),
                "time_taken": q.time_taken
            }
            for q in recent_quizzes
        ]
    }