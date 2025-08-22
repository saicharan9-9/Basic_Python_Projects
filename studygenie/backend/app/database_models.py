from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    preferred_language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="user")
    study_sessions = relationship("StudySession", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    document_type = Column(String, nullable=False)  # pdf, image, text
    extracted_text = Column(Text)
    summary = Column(Text)
    key_topics = Column(JSON)  # List of topics
    page_count = Column(Integer)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    flashcards = relationship("Flashcard", back_populates="document")
    quizzes = relationship("Quiz", back_populates="document")
    study_sessions = relationship("StudySession", back_populates="document")

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    topic = Column(String, nullable=False)
    difficulty = Column(Integer, default=1)  # 1-5 scale
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Spaced repetition fields
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=1)
    repetitions = Column(Integer, default=0)
    next_review = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="flashcards")
    reviews = relationship("FlashcardReview", back_populates="flashcard")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    title = Column(String, nullable=False)
    questions = Column(JSON)  # List of questions with options
    total_questions = Column(Integer, nullable=False)
    estimated_time = Column(Integer, default=15)  # minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    answers = Column(JSON)  # question_id -> answer mapping
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    time_taken = Column(Integer)  # seconds
    weak_topics = Column(JSON)
    strong_topics = Column(JSON)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    session_type = Column(String, nullable=False)  # flashcards, quiz, reading
    duration = Column(Integer, nullable=False)  # minutes
    score = Column(Float)
    topics_covered = Column(JSON)
    started_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    document = relationship("Document", back_populates="study_sessions")

class FlashcardReview(Base):
    __tablename__ = "flashcard_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    flashcard_id = Column(String, ForeignKey("flashcards.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quality = Column(Integer, nullable=False)  # 0-5 scale (SM-2 algorithm)
    reviewed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    flashcard = relationship("Flashcard", back_populates="reviews")

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    total_study_time = Column(Integer, default=0)  # minutes
    study_streak = Column(Integer, default=0)  # days
    last_study_date = Column(DateTime)
    topics_mastered = Column(JSON, default=list)
    weak_subjects = Column(JSON, default=list)
    strong_subjects = Column(JSON, default=list)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)