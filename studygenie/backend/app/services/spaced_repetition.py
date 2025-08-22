from datetime import datetime, timedelta
from typing import Tuple
import math

class SpacedRepetitionService:
    """
    Implements the SM-2 (SuperMemo 2) algorithm for spaced repetition
    """
    
    @staticmethod
    def calculate_next_review(
        quality: int,
        repetitions: int,
        ease_factor: float,
        interval: int
    ) -> Tuple[datetime, int, float, int]:
        """
        Calculate next review date based on SM-2 algorithm
        
        Args:
            quality: Response quality (0-5)
                0: Complete blackout
                1: Incorrect response; the correct one remembered
                2: Incorrect response; where the correct one seemed easy to recall
                3: Correct response recalled with serious difficulty
                4: Correct response after a hesitation
                5: Perfect response
            repetitions: Number of times the card has been reviewed
            ease_factor: Current ease factor (minimum 1.3)
            interval: Current interval in days
        
        Returns:
            Tuple of (next_review_date, new_repetitions, new_ease_factor, new_interval)
        """
        
        # Update ease factor
        new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease_factor = max(1.3, new_ease_factor)
        
        # Determine new repetitions and interval
        if quality < 3:
            # Incorrect response - restart
            new_repetitions = 0
            new_interval = 1
        else:
            # Correct response
            new_repetitions = repetitions + 1
            
            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 6
            else:
                new_interval = math.ceil(interval * new_ease_factor)
        
        # Calculate next review date
        next_review_date = datetime.utcnow() + timedelta(days=new_interval)
        
        return next_review_date, new_repetitions, new_ease_factor, new_interval
    
    @staticmethod
    def get_due_flashcards_query(user_id: int):
        """
        Get SQLAlchemy query for flashcards due for review
        """
        from ..database_models import Flashcard, Document
        from sqlalchemy.orm import Session
        
        def query_due_cards(db: Session):
            return db.query(Flashcard).join(Document).filter(
                Document.user_id == user_id,
                Flashcard.next_review <= datetime.utcnow()
            ).order_by(Flashcard.next_review)
        
        return query_due_cards
    
    @staticmethod
    def update_flashcard_review(
        flashcard_id: str,
        quality: int,
        db_session
    ):
        """
        Update flashcard after review using SM-2 algorithm
        """
        from ..database_models import Flashcard, FlashcardReview
        
        # Get the flashcard
        flashcard = db_session.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
        if not flashcard:
            raise ValueError("Flashcard not found")
        
        # Calculate new values using SM-2
        next_review, new_repetitions, new_ease_factor, new_interval = SpacedRepetitionService.calculate_next_review(
            quality=quality,
            repetitions=flashcard.repetitions,
            ease_factor=flashcard.ease_factor,
            interval=flashcard.interval
        )
        
        # Update flashcard
        flashcard.next_review = next_review
        flashcard.repetitions = new_repetitions
        flashcard.ease_factor = new_ease_factor
        flashcard.interval = new_interval
        
        # Create review record
        review = FlashcardReview(
            flashcard_id=flashcard_id,
            user_id=flashcard.document.user_id,
            quality=quality,
            reviewed_at=datetime.utcnow()
        )
        
        db_session.add(review)
        db_session.commit()
        
        return flashcard
    
    @staticmethod
    def get_study_statistics(user_id: int, db_session) -> dict:
        """
        Get spaced repetition statistics for a user
        """
        from ..database_models import Flashcard, Document, FlashcardReview
        from sqlalchemy import func
        
        # Total flashcards
        total_cards = db_session.query(Flashcard).join(Document).filter(
            Document.user_id == user_id
        ).count()
        
        # Due cards
        due_cards = db_session.query(Flashcard).join(Document).filter(
            Document.user_id == user_id,
            Flashcard.next_review <= datetime.utcnow()
        ).count()
        
        # Cards reviewed today
        today = datetime.utcnow().date()
        cards_reviewed_today = db_session.query(FlashcardReview).filter(
            FlashcardReview.user_id == user_id,
            func.date(FlashcardReview.reviewed_at) == today
        ).count()
        
        # Average ease factor
        avg_ease = db_session.query(func.avg(Flashcard.ease_factor)).join(Document).filter(
            Document.user_id == user_id
        ).scalar() or 2.5
        
        # Cards by difficulty
        difficulty_stats = db_session.query(
            Flashcard.difficulty,
            func.count(Flashcard.id)
        ).join(Document).filter(
            Document.user_id == user_id
        ).group_by(Flashcard.difficulty).all()
        
        return {
            "total_cards": total_cards,
            "due_cards": due_cards,
            "cards_reviewed_today": cards_reviewed_today,
            "average_ease_factor": round(float(avg_ease), 2),
            "difficulty_distribution": {str(diff): count for diff, count in difficulty_stats}
        }