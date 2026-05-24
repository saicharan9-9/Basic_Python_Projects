from datetime import datetime, timedelta
from typing import Dict, List
import math

class SpacedRepetitionService:
    """Service implementing spaced repetition algorithm for flashcards"""
    
    def __init__(self):
        # Default parameters for SM-2 algorithm
        self.default_ease_factor = 2.5
        self.minimum_ease_factor = 1.3
        self.initial_interval = 1  # days
    
    def calculate_next_review(self, 
                            current_ease_factor: float,
                            current_interval: int,
                            quality: int,  # 0-5 scale (0=complete blackout, 5=perfect response)
                            review_count: int) -> Dict[str, any]:
        """
        Calculate next review date using modified SM-2 algorithm
        
        Args:
            current_ease_factor: Current ease factor (typically 1.3-3.0)
            current_interval: Current interval in days
            quality: Quality of response (0-5)
            review_count: Number of times reviewed
            
        Returns:
            Dict with next_interval, next_ease_factor, next_review_date
        """
        
        # If quality < 3, reset interval to 1 day
        if quality < 3:
            next_interval = 1
            next_ease_factor = max(
                current_ease_factor - 0.8 + (0.28 * quality) - (0.02 * quality * quality),
                self.minimum_ease_factor
            )
        else:
            # Calculate new ease factor
            next_ease_factor = current_ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            next_ease_factor = max(next_ease_factor, self.minimum_ease_factor)
            
            # Calculate next interval
            if review_count == 0:
                next_interval = 1
            elif review_count == 1:
                next_interval = 6
            else:
                next_interval = math.ceil(current_interval * next_ease_factor)
        
        # Calculate next review date
        next_review_date = datetime.utcnow() + timedelta(days=next_interval)
        
        return {
            "next_interval": next_interval,
            "next_ease_factor": round(next_ease_factor, 2),
            "next_review_date": next_review_date
        }
    
    def get_due_flashcards(self, flashcards: List[Dict]) -> List[Dict]:
        """
        Get flashcards that are due for review
        
        Args:
            flashcards: List of flashcard objects
            
        Returns:
            List of due flashcards sorted by priority
        """
        now = datetime.utcnow()
        due_cards = []
        
        for card in flashcards:
            next_review = card.get('next_review')
            if not next_review or next_review <= now:
                # Calculate priority (overdue cards have higher priority)
                if next_review:
                    overdue_days = (now - next_review).days
                    priority = overdue_days + 1
                else:
                    priority = 1
                
                card['priority'] = priority
                due_cards.append(card)
        
        # Sort by priority (higher priority first)
        due_cards.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        return due_cards
    
    def get_study_stats(self, flashcards: List[Dict]) -> Dict[str, any]:
        """
        Get study statistics for flashcards
        
        Args:
            flashcards: List of flashcard objects
            
        Returns:
            Dict with various statistics
        """
        now = datetime.utcnow()
        total_cards = len(flashcards)
        
        if total_cards == 0:
            return {
                "total_cards": 0,
                "due_today": 0,
                "overdue": 0,
                "mastered": 0,
                "learning": 0,
                "new": 0
            }
        
        due_today = 0
        overdue = 0
        mastered = 0  # Cards with interval > 21 days
        learning = 0  # Cards with interval 1-21 days
        new = 0      # Cards never reviewed
        
        for card in flashcards:
            next_review = card.get('next_review')
            interval = card.get('review_interval', 0)
            review_count = card.get('review_count', 0)
            
            if review_count == 0:
                new += 1
            elif interval > 21:
                mastered += 1
            else:
                learning += 1
            
            if next_review:
                if next_review.date() == now.date():
                    due_today += 1
                elif next_review < now:
                    overdue += 1
        
        return {
            "total_cards": total_cards,
            "due_today": due_today,
            "overdue": overdue,
            "mastered": mastered,
            "learning": learning,
            "new": new
        }
    
    def quality_from_performance(self, correct: bool, confidence: str = "medium") -> int:
        """
        Convert performance to quality score for SM-2 algorithm
        
        Args:
            correct: Whether answer was correct
            confidence: Student's confidence level (low, medium, high)
            
        Returns:
            Quality score (0-5)
        """
        if not correct:
            return 0  # Complete failure
        
        confidence_map = {
            "low": 3,    # Correct but with difficulty
            "medium": 4, # Correct with some hesitation
            "high": 5    # Perfect response
        }
        
        return confidence_map.get(confidence, 4)