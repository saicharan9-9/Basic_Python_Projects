from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class StudyMaterial(Base):
    __tablename__ = "study_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # summary, quiz, flashcard
    content = Column(Text)
    language = Column(String, default="en")
    difficulty_level = Column(String, default="medium")  # easy, medium, hard
    subject = Column(String)
    tags = Column(JSON)  # List of tags
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="study_materials")
    document = relationship("Document", back_populates="study_materials")
    quizzes = relationship("Quiz", back_populates="study_material")
    flashcards = relationship("Flashcard", back_populates="study_material")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    total_questions = Column(Integer, default=0)
    time_limit = Column(Integer)  # in minutes
    study_material_id = Column(Integer, ForeignKey("study_materials.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    study_material = relationship("StudyMaterial", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, default="mcq")  # mcq, true_false, fill_blank
    options = Column(JSON)  # List of options for MCQ
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text)
    difficulty = Column(String, default="medium")
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    front_text = Column(Text, nullable=False)
    back_text = Column(Text, nullable=False)
    difficulty = Column(String, default="medium")
    next_review = Column(DateTime(timezone=True))
    review_interval = Column(Integer, default=1)  # days
    ease_factor = Column(String, default="2.5")
    review_count = Column(Integer, default=0)
    study_material_id = Column(Integer, ForeignKey("study_materials.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    study_material = relationship("StudyMaterial", back_populates="flashcards")