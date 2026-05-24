from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import json

from database.database import get_db, User, ProgressRecord, QuizAttempt, Flashcard, StudyMaterial
from app.routes.auth import get_current_user

router = APIRouter()

# Pydantic models
class ProgressSummary(BaseModel):
    total_study_time: int  # in minutes
    total_quizzes_taken: int
    average_score: float
    study_streak: int
    total_flashcards_reviewed: int
    subjects_studied: List[str]

class SubjectProgress(BaseModel):
    subject: str
    total_time: int
    quizzes_taken: int
    average_score: float
    last_studied: datetime

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_title: str
    score: float
    total_questions: int
    correct_answers: int
    time_taken: int
    completed_at: datetime

    class Config:
        from_attributes = True

class FlashcardProgress(BaseModel):
    id: int
    front_content: str
    back_content: str
    review_count: int
    last_reviewed: Optional[datetime]
    next_review: Optional[datetime]
    difficulty: str

    class Config:
        from_attributes = True

# Routes
@router.get("/summary", response_model=ProgressSummary)
async def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall progress summary for the user"""
    try:
        # Calculate total study time
        total_time = db.query(func.sum(ProgressRecord.time_spent)).filter(
            ProgressRecord.user_id == current_user.id
        ).scalar() or 0
        
        # Count total quizzes taken
        total_quizzes = db.query(func.count(QuizAttempt.id)).filter(
            QuizAttempt.user_id == current_user.id
        ).scalar() or 0
        
        # Calculate average score
        avg_score = db.query(func.avg(QuizAttempt.score)).filter(
            QuizAttempt.user_id == current_user.id
        ).scalar() or 0.0
        
        # Calculate study streak
        streak = calculate_study_streak(current_user.id, db)
        
        # Count flashcards reviewed
        total_flashcards = db.query(func.count(Flashcard.id)).filter(
            Flashcard.user_id == current_user.id,
            Flashcard.review_count > 0
        ).scalar() or 0
        
        # Get unique subjects
        subjects = db.query(ProgressRecord.subject).filter(
            ProgressRecord.user_id == current_user.id
        ).distinct().all()
        subjects_list = [s[0] for s in subjects]
        
        return ProgressSummary(
            total_study_time=total_time,
            total_quizzes_taken=total_quizzes,
            average_score=round(avg_score, 2),
            study_streak=streak,
            total_flashcards_reviewed=total_flashcards,
            subjects_studied=subjects_list
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting progress summary: {str(e)}")

@router.get("/subjects", response_model=List[SubjectProgress])
async def get_subject_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress breakdown by subject"""
    try:
        # Get progress records grouped by subject
        subject_progress = db.query(
            ProgressRecord.subject,
            func.sum(ProgressRecord.time_spent).label('total_time'),
            func.count(ProgressRecord.id).label('quizzes_taken'),
            func.avg(ProgressRecord.score).label('average_score'),
            func.max(ProgressRecord.date).label('last_studied')
        ).filter(
            ProgressRecord.user_id == current_user.id
        ).group_by(ProgressRecord.subject).all()
        
        result = []
        for sp in subject_progress:
            result.append(SubjectProgress(
                subject=sp.subject,
                total_time=sp.total_time or 0,
                quizzes_taken=sp.quizzes_taken or 0,
                average_score=round(sp.average_score or 0.0, 2),
                last_studied=sp.last_studied
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting subject progress: {str(e)}")

@router.get("/quiz-attempts", response_model=List[QuizAttemptResponse])
async def get_quiz_attempts(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent quiz attempts"""
    try:
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == current_user.id
        ).order_by(desc(QuizAttempt.completed_at)).limit(limit).all()
        
        result = []
        for attempt in attempts:
            # Get quiz title
            quiz = db.query(QuizAttempt.quiz).first()
            quiz_title = quiz.title if quiz else "Unknown Quiz"
            
            result.append(QuizAttemptResponse(
                id=attempt.id,
                quiz_title=quiz_title,
                score=attempt.score,
                total_questions=attempt.total_questions,
                correct_answers=attempt.correct_answers,
                time_taken=attempt.time_taken,
                completed_at=attempt.completed_at
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting quiz attempts: {str(e)}")

@router.get("/flashcards", response_model=List[FlashcardProgress])
async def get_flashcard_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get flashcard progress and review schedule"""
    try:
        flashcards = db.query(Flashcard).filter(
            Flashcard.user_id == current_user.id
        ).all()
        
        result = []
        for card in flashcards:
            result.append(FlashcardProgress(
                id=card.id,
                front_content=card.front_content,
                back_content=card.back_content,
                review_count=card.review_count,
                last_reviewed=card.last_reviewed,
                next_review=card.next_review,
                difficulty=card.difficulty
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting flashcard progress: {str(e)}")

@router.post("/record-study-session")
async def record_study_session(
    subject: str = Form(...),
    topic: str = Form(...),
    time_spent: int = Form(...),  # in minutes
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a study session"""
    try:
        progress_record = ProgressRecord(
            user_id=current_user.id,
            subject=subject,
            topic=topic,
            time_spent=time_spent,
            score=0.0,  # No quiz score for study sessions
            date=datetime.utcnow()
        )
        
        db.add(progress_record)
        db.commit()
        
        return {"message": "Study session recorded successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording study session: {str(e)}")

@router.post("/record-quiz-attempt")
async def record_quiz_attempt(
    quiz_id: int = Form(...),
    score: float = Form(...),
    total_questions: int = Form(...),
    correct_answers: int = Form(...),
    time_taken: int = Form(...),  # in seconds
    answers: str = Form(...),  # JSON string of user answers
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a quiz attempt"""
    try:
        quiz_attempt = QuizAttempt(
            quiz_id=quiz_id,
            user_id=current_user.id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            time_taken=time_taken,
            answers=answers,
            completed_at=datetime.utcnow()
        )
        
        db.add(quiz_attempt)
        db.commit()
        
        return {"message": "Quiz attempt recorded successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording quiz attempt: {str(e)}")

@router.post("/update-flashcard-review")
async def update_flashcard_review(
    flashcard_id: int = Form(...),
    review_count: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update flashcard review progress"""
    try:
        flashcard = db.query(Flashcard).filter(
            Flashcard.id == flashcard_id,
            Flashcard.user_id == current_user.id
        ).first()
        
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        flashcard.review_count = review_count
        flashcard.last_reviewed = datetime.utcnow()
        
        # Calculate next review using spaced repetition
        next_review = calculate_next_review(review_count)
        flashcard.next_review = next_review
        
        db.commit()
        
        return {"message": "Flashcard review updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating flashcard review: {str(e)}")

@router.get("/study-streak")
async def get_study_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current study streak"""
    try:
        streak = calculate_study_streak(current_user.id, db)
        return {"study_streak": streak}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating study streak: {str(e)}")

@router.get("/weekly-progress")
async def get_weekly_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress for the current week"""
    try:
        # Get start of current week (Monday)
        today = datetime.utcnow().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        # Get progress records for the week
        weekly_progress = db.query(ProgressRecord).filter(
            ProgressRecord.user_id == current_user.id,
            ProgressRecord.date >= start_of_week,
            ProgressRecord.date <= end_of_week
        ).all()
        
        # Group by day
        daily_progress = {}
        for record in weekly_progress:
            day = record.date.strftime('%Y-%m-%d')
            if day not in daily_progress:
                daily_progress[day] = {
                    'time_spent': 0,
                    'quizzes_taken': 0,
                    'average_score': 0.0
                }
            
            daily_progress[day]['time_spent'] += record.time_spent
        
        return {
            "week_start": start_of_week.strftime('%Y-%m-%d'),
            "week_end": end_of_week.strftime('%Y-%m-%d'),
            "daily_progress": daily_progress
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting weekly progress: {str(e)}")

# Helper functions
def calculate_study_streak(user_id: int, db: Session) -> int:
    """Calculate current study streak in days"""
    try:
        # Get all study dates for the user
        study_dates = db.query(ProgressRecord.date).filter(
            ProgressRecord.user_id == user_id
        ).distinct().order_by(desc(ProgressRecord.date)).all()
        
        if not study_dates:
            return 0
        
        streak = 0
        current_date = datetime.utcnow().date()
        
        for i, (study_date,) in enumerate(study_dates):
            study_date = study_date.date()
            
            if i == 0:
                # Check if today or yesterday
                if current_date == study_date or current_date - study_date == timedelta(days=1):
                    streak = 1
                else:
                    break
            else:
                # Check if consecutive days
                prev_date = study_dates[i-1][0].date()
                if study_date == prev_date - timedelta(days=1):
                    streak += 1
                else:
                    break
        
        return streak
        
    except Exception as e:
        print(f"Error calculating study streak: {e}")
        return 0

def calculate_next_review(review_count: int) -> datetime:
    """Calculate next review date using spaced repetition algorithm"""
    # Simple spaced repetition: 1, 3, 7, 14, 30, 90 days
    intervals = [1, 3, 7, 14, 30, 90]
    
    if review_count < len(intervals):
        days = intervals[review_count]
    else:
        days = 90  # Max interval
    
    return datetime.utcnow() + timedelta(days=days)