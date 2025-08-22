from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from typing import List
import os

from utils.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    preferred_language = Column(String, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    study_materials = relationship("StudyMaterial", back_populates="user")
    quizzes = relationship("Quiz", back_populates="user")
    flashcards = relationship("Flashcard", back_populates="user")
    progress_records = relationship("ProgressRecord", back_populates="user")

class StudyMaterial(Base):
    __tablename__ = "study_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content_type = Column(String)  # pdf, text, handwritten
    file_path = Column(String, nullable=True)
    extracted_text = Column(Text)
    summary = Column(Text, nullable=True)
    language = Column(String, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="study_materials")
    quizzes = relationship("Quiz", back_populates="study_material")
    flashcards = relationship("Flashcard", back_populates="study_material")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    study_material_id = Column(Integer, ForeignKey("study_materials.id"))
    title = Column(String)
    questions = Column(Text)  # JSON string of questions
    total_questions = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="quizzes")
    study_material = relationship("StudyMaterial", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Float)
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    time_taken = Column(Integer)  # in seconds
    answers = Column(Text)  # JSON string of user answers
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User")

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    study_material_id = Column(Integer, ForeignKey("study_materials.id"))
    front_content = Column(Text)
    back_content = Column(Text)
    difficulty = Column(String, default="medium")  # easy, medium, hard
    last_reviewed = Column(DateTime(timezone=True), nullable=True)
    next_review = Column(DateTime(timezone=True), nullable=True)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="flashcards")
    study_material = relationship("StudyMaterial", back_populates="flashcards")

class ProgressRecord(Base):
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    topic = Column(String)
    score = Column(Float)
    time_spent = Column(Integer)  # in minutes
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress_records")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()