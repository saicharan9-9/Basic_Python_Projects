from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
	name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	documents: Mapped[list["Document"]] = relationship("Document", back_populates="owner")
	flashcards: Mapped[list["Flashcard"]] = relationship("Flashcard", back_populates="owner")
	quiz_questions: Mapped[list["QuizQuestion"]] = relationship("QuizQuestion", back_populates="owner")


class Document(Base):
	__tablename__ = "documents"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
	title: Mapped[str] = mapped_column(String(512))
	language: Mapped[str] = mapped_column(String(32), default="en")
	source_path: Mapped[str] = mapped_column(String(1024))
	summary: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	owner: Mapped[User] = relationship("User", back_populates="documents")


class Flashcard(Base):
	__tablename__ = "flashcards"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
	document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("documents.id"), nullable=True)
	front: Mapped[str] = mapped_column(Text)
	back: Mapped[str] = mapped_column(Text)
	interval_days: Mapped[float] = mapped_column(Float, default=0.0)
	ease: Mapped[float] = mapped_column(Float, default=2.5)
	due_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	owner: Mapped[User] = relationship("User", back_populates="flashcards")
	document: Mapped[Optional[Document]] = relationship("Document")


class QuizQuestion(Base):
	__tablename__ = "quiz_questions"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
	document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("documents.id"), nullable=True)
	question: Mapped[str] = mapped_column(Text)
	options_json: Mapped[str] = mapped_column(Text)
	correct_index: Mapped[int] = mapped_column(Integer)
	explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	owner: Mapped[User] = relationship("User", back_populates="quiz_questions")
	document: Mapped[Optional[Document]] = relationship("Document")


class ProgressStat(Base):
	__tablename__ = "progress_stats"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
	study_minutes: Mapped[int] = mapped_column(Integer, default=0)
	streak_days: Mapped[int] = mapped_column(Integer, default=0)
	mastery_score: Mapped[float] = mapped_column(Float, default=0.0)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)