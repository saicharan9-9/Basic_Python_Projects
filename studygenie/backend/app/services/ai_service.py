import openai
import json
import uuid
from typing import List, Dict, Any
from datetime import datetime
import os
from ..models import Question, Flashcard, Quiz, MCQOption, QuestionType

class AIService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()
    
    def generate_summary(self, text: str, language: str = "en") -> str:
        """Generate a concise summary of the provided text"""
        language_map = {
            "en": "English",
            "hi": "Hindi", 
            "mr": "Marathi"
        }
        
        prompt = f"""
        Create a comprehensive yet concise summary of the following text in {language_map.get(language, 'English')}:
        
        Text: {text}
        
        Requirements:
        - Capture key concepts and main ideas
        - Organize information logically
        - Use clear, student-friendly language
        - Include important details and examples
        - Maximum 500 words
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")
    
    def extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics and concepts from the text"""
        prompt = f"""
        Analyze the following text and extract 5-10 key topics/concepts that are most important for studying:
        
        Text: {text}
        
        Return only a JSON array of topic strings, no other text.
        Example: ["Photosynthesis", "Cell Structure", "DNA Replication"]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.2
            )
            
            content = response.choices[0].message.content.strip()
            # Parse JSON response
            topics = json.loads(content)
            return topics
        except Exception as e:
            print(f"Error extracting topics: {e}")
            return []
    
    def generate_flashcards(self, text: str, num_cards: int = 15, language: str = "en") -> List[Flashcard]:
        """Generate flashcards from the provided text"""
        language_map = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi"
        }
        
        prompt = f"""
        Create {num_cards} educational flashcards from the following text in {language_map.get(language, 'English')}:
        
        Text: {text}
        
        Requirements:
        - Focus on key concepts, definitions, and important facts
        - Front should be a clear question or term
        - Back should be a comprehensive but concise answer
        - Vary difficulty levels (1-5 scale)
        - Cover different topics from the text
        
        Return a JSON array with this structure:
        [{{
            "front": "Question or term",
            "back": "Answer or definition", 
            "topic": "Subject area",
            "difficulty": 3
        }}]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.4
            )
            
            content = response.choices[0].message.content.strip()
            flashcards_data = json.loads(content)
            
            flashcards = []
            for card_data in flashcards_data:
                flashcard = Flashcard(
                    id=str(uuid.uuid4()),
                    front=card_data["front"],
                    back=card_data["back"],
                    topic=card_data["topic"],
                    difficulty=card_data.get("difficulty", 3),
                    created_at=datetime.utcnow()
                )
                flashcards.append(flashcard)
            
            return flashcards
        except Exception as e:
            raise Exception(f"Error generating flashcards: {str(e)}")
    
    def generate_quiz(self, text: str, num_questions: int = 10, language: str = "en") -> Quiz:
        """Generate a quiz from the provided text"""
        language_map = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi"
        }
        
        prompt = f"""
        Create a {num_questions}-question quiz from the following text in {language_map.get(language, 'English')}:
        
        Text: {text}
        
        Requirements:
        - Mix of MCQ, True/False, and short answer questions
        - Cover key concepts from the text
        - Include 4 options for MCQ questions
        - Provide explanations for correct answers
        - Vary difficulty levels (1-5 scale)
        
        Return a JSON object with this structure:
        {{
            "title": "Quiz Title",
            "questions": [{{
                "question_text": "Question here?",
                "question_type": "mcq",
                "options": [
                    {{"text": "Option 1", "is_correct": false}},
                    {{"text": "Option 2", "is_correct": true}},
                    {{"text": "Option 3", "is_correct": false}},
                    {{"text": "Option 4", "is_correct": false}}
                ],
                "correct_answer": "Option 2",
                "explanation": "Explanation here",
                "difficulty": 3,
                "topic": "Topic name"
            }}]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
                temperature=0.4
            )
            
            content = response.choices[0].message.content.strip()
            quiz_data = json.loads(content)
            
            questions = []
            for q_data in quiz_data["questions"]:
                options = []
                if q_data.get("options"):
                    options = [MCQOption(**opt) for opt in q_data["options"]]
                
                question = Question(
                    id=str(uuid.uuid4()),
                    question_text=q_data["question_text"],
                    question_type=QuestionType(q_data["question_type"]),
                    options=options,
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data["explanation"],
                    difficulty=q_data.get("difficulty", 3),
                    topic=q_data["topic"]
                )
                questions.append(question)
            
            quiz = Quiz(
                id=str(uuid.uuid4()),
                title=quiz_data["title"],
                questions=questions,
                total_questions=len(questions),
                estimated_time=len(questions) * 2  # 2 minutes per question
            )
            
            return quiz
        except Exception as e:
            raise Exception(f"Error generating quiz: {str(e)}")
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        language_map = {
            "hi": "Hindi",
            "mr": "Marathi",
            "en": "English"
        }
        
        if target_language == "en":
            return text
        
        prompt = f"""
        Translate the following text to {language_map.get(target_language, target_language)}:
        
        {text}
        
        Maintain the educational context and technical terms appropriately.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.2
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error translating text: {str(e)}")
    
    def explain_answer(self, question: str, correct_answer: str, user_answer: str, language: str = "en") -> str:
        """Generate explanation for wrong answers in simple terms"""
        language_map = {
            "en": "English",
            "hi": "Hindi", 
            "mr": "Marathi"
        }
        
        prompt = f"""
        A student answered a question incorrectly. Explain the correct answer in simple terms in {language_map.get(language, 'English')}:
        
        Question: {question}
        Correct Answer: {correct_answer}
        Student's Answer: {user_answer}
        
        Requirements:
        - Use simple, encouraging language
        - Explain why the correct answer is right
        - Briefly explain why the student's answer was incorrect
        - Provide a helpful tip to remember the concept
        - Keep it under 150 words
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating explanation: {str(e)}")