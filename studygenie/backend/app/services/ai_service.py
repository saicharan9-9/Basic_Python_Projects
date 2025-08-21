import openai
from typing import List, Dict, Any, Optional
import json
import re
from app.core.config import settings

class AIService:
    """Service for AI-powered content generation using OpenAI"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            print("Warning: OpenAI API key not found. AI features will be disabled.")
    
    async def generate_summary(self, text: str, language: str = "en") -> str:
        """Generate a summary of the provided text"""
        try:
            language_map = {
                "en": "English",
                "hi": "Hindi", 
                "mr": "Marathi"
            }
            
            prompt = f"""
            Create a comprehensive summary of the following text in {language_map.get(language, 'English')}. 
            The summary should:
            1. Capture the main concepts and key points
            2. Be well-structured with clear sections
            3. Include important details and examples
            4. Be suitable for study purposes
            
            Text to summarize:
            {text[:4000]}  # Limit text to avoid token limits
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "Summary generation failed. Please try again."
    
    async def generate_quiz(self, text: str, num_questions: int = 10, language: str = "en") -> List[Dict[str, Any]]:
        """Generate quiz questions from the provided text"""
        try:
            language_map = {
                "en": "English",
                "hi": "Hindi", 
                "mr": "Marathi"
            }
            
            prompt = f"""
            Create {num_questions} multiple choice questions based on the following text in {language_map.get(language, 'English')}.
            
            Format your response as a JSON array with the following structure:
            [
                {{
                    "question": "Question text",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A",
                    "explanation": "Brief explanation of why this is correct",
                    "difficulty": "easy|medium|hard"
                }}
            ]
            
            Guidelines:
            - Questions should test understanding, not just memorization
            - Include a mix of difficulty levels
            - Options should be plausible but only one correct
            - Provide clear explanations
            
            Text:
            {text[:3000]}
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.5
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            questions = json.loads(content)
            return questions
            
        except Exception as e:
            print(f"Error generating quiz: {str(e)}")
            return []
    
    async def generate_flashcards(self, text: str, num_cards: int = 15, language: str = "en") -> List[Dict[str, str]]:
        """Generate flashcards from the provided text"""
        try:
            language_map = {
                "en": "English",
                "hi": "Hindi", 
                "mr": "Marathi"
            }
            
            prompt = f"""
            Create {num_cards} flashcards based on the following text in {language_map.get(language, 'English')}.
            
            Format your response as a JSON array:
            [
                {{
                    "front": "Question or concept",
                    "back": "Answer or explanation",
                    "difficulty": "easy|medium|hard"
                }}
            ]
            
            Guidelines:
            - Focus on key concepts, definitions, and important facts
            - Front should be concise questions or prompts
            - Back should provide clear, comprehensive answers
            - Include a mix of difficulty levels
            
            Text:
            {text[:3000]}
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.4
            )
            
            content = response.choices[0].message.content
            flashcards = json.loads(content)
            return flashcards
            
        except Exception as e:
            print(f"Error generating flashcards: {str(e)}")
            return []
    
    async def answer_question(self, question: str, context: str, language: str = "en") -> str:
        """Answer a student's question using the provided context (RAG)"""
        try:
            language_map = {
                "en": "English",
                "hi": "Hindi", 
                "mr": "Marathi"
            }
            
            prompt = f"""
            You are an AI tutor. Answer the following question based on the provided context in {language_map.get(language, 'English')}.
            
            Guidelines:
            - Use simple, clear language suitable for students
            - Base your answer primarily on the provided context
            - If the context doesn't contain enough information, say so
            - Provide examples when helpful
            - Be encouraging and supportive
            
            Context:
            {context[:2000]}
            
            Question: {question}
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful, patient AI tutor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error answering question: {str(e)}")
            return "I'm sorry, I couldn't process your question. Please try again."
    
    async def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        try:
            language_map = {
                "en": "English",
                "hi": "Hindi", 
                "mr": "Marathi"
            }
            
            prompt = f"""
            Translate the following text to {language_map.get(target_language, 'English')}:
            
            {text}
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error translating text: {str(e)}")
            return text  # Return original text if translation fails