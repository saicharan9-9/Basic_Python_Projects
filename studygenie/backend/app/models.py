from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    preferred_language: str = "en"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: str
    full_name: str
    preferred_language: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DocumentType(str, Enum):
    PDF = "pdf"
    IMAGE = "image"
    TEXT = "text"

class UploadResponse(BaseModel):
    document_id: str
    filename: str
    document_type: DocumentType
    extracted_text: str
    page_count: Optional[int] = None

class QuestionType(str, Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    FILL_BLANK = "fill_blank"

class MCQOption(BaseModel):
    text: str
    is_correct: bool

class Question(BaseModel):
    id: str
    question_text: str
    question_type: QuestionType
    options: Optional[List[MCQOption]] = None
    correct_answer: str
    explanation: str
    difficulty: int  # 1-5 scale
    topic: str

class Flashcard(BaseModel):
    id: str
    front: str
    back: str
    topic: str
    difficulty: int
    created_at: datetime

class Quiz(BaseModel):
    id: str
    title: str
    questions: List[Question]
    total_questions: int
    estimated_time: int  # in minutes

class StudyMaterial(BaseModel):
    document_id: str
    summary: str
    flashcards: List[Flashcard]
    quiz: Quiz
    key_topics: List[str]

class QuizAttempt(BaseModel):
    quiz_id: str
    answers: Dict[str, str]  # question_id -> answer

class QuizResult(BaseModel):
    quiz_id: str
    score: float
    total_questions: int
    correct_answers: int
    time_taken: int  # in seconds
    weak_topics: List[str]
    strong_topics: List[str]

class StudySession(BaseModel):
    document_id: str
    session_type: str  # "flashcards", "quiz", "reading"
    duration: int  # in minutes
    score: Optional[float] = None

class ProgressStats(BaseModel):
    total_study_time: int
    study_streak: int
    topics_mastered: int
    average_quiz_score: float
    weak_subjects: List[str]
    strong_subjects: List[str]
    recent_activity: List[Dict[str, Any]]

class TutorQuestion(BaseModel):
    question: str
    document_id: str
    language: str = "en"

class TutorResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float