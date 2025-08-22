from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any

from ..models import User, ProgressStats
from ..database_models import (
    UserProgress, StudySession, QuizAttempt, FlashcardReview,
    Document, Flashcard, Quiz as DBQuiz
)
from ..services.database import get_db
from ..services.auth_service import verify_token

router = APIRouter()

@router.get("/dashboard", response_model=ProgressStats)
async def get_dashboard_stats(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard statistics"""
    
    # Get or create user progress
    user_progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).first()
    if not user_progress:
        user_progress = UserProgress(user_id=current_user.id)
        db.add(user_progress)
        db.commit()
        db.refresh(user_progress)
    
    # Calculate total study time from sessions
    total_study_time = db.query(func.sum(StudySession.duration)).filter(
        StudySession.user_id == current_user.id
    ).scalar() or 0
    
    # Calculate study streak
    study_streak = calculate_study_streak(current_user.id, db)
    
    # Count topics mastered (topics with >80% quiz accuracy)
    topics_mastered = count_mastered_topics(current_user.id, db)
    
    # Calculate average quiz score
    avg_quiz_score = db.query(func.avg(QuizAttempt.score)).filter(
        QuizAttempt.user_id == current_user.id
    ).scalar() or 0.0
    
    # Get weak and strong subjects
    weak_subjects, strong_subjects = analyze_subject_performance(current_user.id, db)
    
    # Get recent activity
    recent_activity = get_recent_activity(current_user.id, db)
    
    # Update user progress
    user_progress.total_study_time = total_study_time
    user_progress.study_streak = study_streak
    user_progress.topics_mastered = list(topics_mastered)
    user_progress.weak_subjects = weak_subjects
    user_progress.strong_subjects = strong_subjects
    user_progress.last_study_date = datetime.utcnow().date()
    db.commit()
    
    return ProgressStats(
        total_study_time=total_study_time,
        study_streak=study_streak,
        topics_mastered=len(topics_mastered),
        average_quiz_score=round(avg_quiz_score, 1),
        weak_subjects=weak_subjects,
        strong_subjects=strong_subjects,
        recent_activity=recent_activity
    )

@router.get("/study-heatmap")
async def get_study_heatmap(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get study activity heatmap data for the last 365 days"""
    
    # Get study sessions for the last year
    one_year_ago = datetime.utcnow() - timedelta(days=365)
    
    sessions = db.query(
        func.date(StudySession.started_at).label('date'),
        func.sum(StudySession.duration).label('total_time'),
        func.count(StudySession.id).label('session_count')
    ).filter(
        StudySession.user_id == current_user.id,
        StudySession.started_at >= one_year_ago
    ).group_by(func.date(StudySession.started_at)).all()
    
    # Format for heatmap
    heatmap_data = []
    for session in sessions:
        heatmap_data.append({
            "date": session.date.isoformat(),
            "study_time": session.total_time,
            "session_count": session.session_count,
            "intensity": min(session.total_time / 60, 5)  # Cap at 5 for visualization
        })
    
    return {"heatmap_data": heatmap_data}

@router.get("/topic-performance")
async def get_topic_performance(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get performance breakdown by topic"""
    
    # Get quiz performance by topic
    quiz_performance = {}
    
    quiz_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).all()
    
    for attempt in quiz_attempts:
        quiz = db.query(DBQuiz).filter(DBQuiz.id == attempt.quiz_id).first()
        if not quiz:
            continue
            
        for question in quiz.questions:
            topic = question.get("topic", "Unknown")
            question_id = question["id"]
            user_answer = attempt.answers.get(question_id, "")
            correct_answer = question["correct_answer"]
            
            is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
            
            if topic not in quiz_performance:
                quiz_performance[topic] = {"correct": 0, "total": 0}
            
            quiz_performance[topic]["total"] += 1
            if is_correct:
                quiz_performance[topic]["correct"] += 1
    
    # Calculate accuracy percentages
    topic_stats = []
    for topic, stats in quiz_performance.items():
        accuracy = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        topic_stats.append({
            "topic": topic,
            "accuracy": round(accuracy, 1),
            "questions_answered": stats["total"],
            "correct_answers": stats["correct"]
        })
    
    # Sort by accuracy (lowest first to highlight weak areas)
    topic_stats.sort(key=lambda x: x["accuracy"])
    
    return {"topic_performance": topic_stats}

@router.get("/learning-curve")
async def get_learning_curve(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get learning curve data showing improvement over time"""
    
    # Get quiz attempts over time
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).order_by(QuizAttempt.completed_at).all()
    
    learning_curve = []
    cumulative_score = 0
    
    for i, attempt in enumerate(attempts):
        cumulative_score += attempt.score
        avg_score = cumulative_score / (i + 1)
        
        learning_curve.append({
            "attempt_number": i + 1,
            "score": attempt.score,
            "average_score": round(avg_score, 1),
            "date": attempt.completed_at.isoformat(),
            "quiz_title": attempt.quiz.title if attempt.quiz else "Unknown"
        })
    
    return {"learning_curve": learning_curve}

def calculate_study_streak(user_id: int, db: Session) -> int:
    """Calculate current study streak in days"""
    today = datetime.utcnow().date()
    streak = 0
    current_date = today
    
    while True:
        # Check if user studied on current_date
        session_count = db.query(StudySession).filter(
            StudySession.user_id == user_id,
            func.date(StudySession.started_at) == current_date
        ).count()
        
        if session_count > 0:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak

def count_mastered_topics(user_id: int, db: Session) -> set:
    """Count topics where user has >80% accuracy"""
    mastered_topics = set()
    
    quiz_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user_id
    ).all()
    
    topic_performance = {}
    
    for attempt in quiz_attempts:
        for topic in attempt.strong_topics or []:
            if topic not in topic_performance:
                topic_performance[topic] = []
            topic_performance[topic].append(attempt.score)
    
    # Consider topic mastered if average score > 80%
    for topic, scores in topic_performance.items():
        if scores and sum(scores) / len(scores) > 80:
            mastered_topics.add(topic)
    
    return mastered_topics

def analyze_subject_performance(user_id: int, db: Session) -> tuple:
    """Analyze weak and strong subjects based on quiz performance"""
    topic_performance = {}
    
    quiz_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user_id
    ).all()
    
    for attempt in quiz_attempts:
        # Add weak topics
        for topic in attempt.weak_topics or []:
            if topic not in topic_performance:
                topic_performance[topic] = {"scores": [], "attempts": 0}
            topic_performance[topic]["scores"].append(attempt.score)
            topic_performance[topic]["attempts"] += 1
        
        # Add strong topics
        for topic in attempt.strong_topics or []:
            if topic not in topic_performance:
                topic_performance[topic] = {"scores": [], "attempts": 0}
            topic_performance[topic]["scores"].append(attempt.score)
            topic_performance[topic]["attempts"] += 1
    
    weak_subjects = []
    strong_subjects = []
    
    for topic, data in topic_performance.items():
        if data["scores"]:
            avg_score = sum(data["scores"]) / len(data["scores"])
            if avg_score < 60:
                weak_subjects.append(topic)
            elif avg_score > 80:
                strong_subjects.append(topic)
    
    return weak_subjects, strong_subjects

def get_recent_activity(user_id: int, db: Session, days: int = 7) -> List[Dict[str, Any]]:
    """Get recent study activity"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    activities = []
    
    # Recent study sessions
    sessions = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.started_at >= cutoff_date
    ).order_by(desc(StudySession.started_at)).limit(10).all()
    
    for session in sessions:
        activities.append({
            "type": "study_session",
            "description": f"Studied {session.session_type} for {session.duration} minutes",
            "timestamp": session.started_at.isoformat(),
            "score": session.score
        })
    
    # Recent quiz attempts
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.completed_at >= cutoff_date
    ).order_by(desc(QuizAttempt.completed_at)).limit(5).all()
    
    for attempt in attempts:
        activities.append({
            "type": "quiz_attempt",
            "description": f"Completed quiz with {attempt.score:.1f}% score",
            "timestamp": attempt.completed_at.isoformat(),
            "score": attempt.score
        })
    
    # Sort by timestamp (most recent first)
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return activities[:10]  # Return top 10 most recent activities