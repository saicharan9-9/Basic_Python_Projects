import openai
from typing import List, Dict, Any
import json
from utils.config import settings

class AIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            # Fallback to mock responses for demo
            self.mock_mode = True
            print("Warning: OpenAI API key not found. Using mock responses.")
    
    def generate_summary(self, text: str, language: str = "en") -> str:
        """Generate a concise summary of the study material"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_summary(text, language)
        
        try:
            prompt = f"""
            Create a comprehensive summary of the following study material in {language}.
            Focus on key concepts, main ideas, and important details.
            Keep it concise but informative.
            
            Text: {text[:3000]}  # Limit text length
            
            Summary:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational content summarizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._mock_summary(text, language)
    
    def generate_quiz_questions(self, text: str, num_questions: int, language: str = "en") -> List[Dict[str, Any]]:
        """Generate multiple choice quiz questions from study material"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_quiz_questions(text, num_questions, language)
        
        try:
            prompt = f"""
            Generate {num_questions} multiple choice questions based on the following study material.
            Questions should be in {language}.
            Each question should have 4 options (A, B, C, D) with only one correct answer.
            Include questions of varying difficulty levels.
            
            Text: {text[:3000]}
            
            Return the questions in this exact JSON format:
            [
                {{
                    "question": "Question text here?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 0,
                    "explanation": "Brief explanation of the correct answer",
                    "difficulty": "easy/medium/hard"
                }}
            ]
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator for educational content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            try:
                questions = json.loads(response.choices[0].message.content.strip())
                return questions
            except json.JSONDecodeError:
                return self._mock_quiz_questions(text, num_questions, language)
                
        except Exception as e:
            print(f"Error generating quiz questions: {e}")
            return self._mock_quiz_questions(text, num_questions, language)
    
    def generate_flashcards(self, text: str, num_cards: int, language: str = "en") -> List[Dict[str, str]]:
        """Generate flashcards from study material"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_flashcards(text, num_cards, language)
        
        try:
            prompt = f"""
            Create {num_cards} flashcards based on the following study material.
            Flashcards should be in {language}.
            Each flashcard should have a clear front (question/concept) and back (answer/explanation).
            Focus on key terms, concepts, and important facts.
            
            Text: {text[:3000]}
            
            Return the flashcards in this exact JSON format:
            [
                {{
                    "front": "Front of the card (question/concept)",
                    "back": "Back of the card (answer/explanation)",
                    "difficulty": "easy/medium/hard"
                }}
            ]
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert flashcard creator for educational content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            try:
                flashcards = json.loads(response.choices[0].message.content.strip())
                return flashcards
            except json.JSONDecodeError:
                return self._mock_flashcards(text, num_cards, language)
                
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return self._mock_flashcards(text, num_cards, language)
    
    def answer_question(self, question: str, context: str, language: str = "en") -> str:
        """Answer student questions using RAG approach"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_answer(question, context, language)
        
        try:
            prompt = f"""
            Answer the following question based on the provided study material context.
            Answer should be in {language}.
            Be clear, educational, and helpful.
            If the answer is not in the context, say so.
            
            Context: {context[:2000]}
            Question: {question}
            
            Answer:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor explaining concepts from study materials."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error answering question: {e}")
            return self._mock_answer(question, context, language)
    
    def translate_content(self, content: str, target_language: str) -> str:
        """Translate content to target language"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_translate(content, target_language)
        
        try:
            prompt = f"""
            Translate the following content to {target_language}.
            Maintain the educational tone and accuracy.
            
            Content: {content}
            
            Translation:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert translator for educational content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error translating content: {e}")
            return self._mock_translate(content, target_language)
    
    def generate_related_questions(self, question: str, context: str, language: str = "en") -> List[str]:
        """Generate related questions for better learning"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_related_questions(question, language)
        
        try:
            prompt = f"""
            Generate 3 related questions based on this question and context.
            Questions should be in {language}.
            Make them educational and helpful for learning.
            
            Original Question: {question}
            Context: {context[:1000]}
            
            Related Questions:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator generating related questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            # Parse the response to extract questions
            response_text = response.choices[0].message.content.strip()
            questions = [q.strip() for q in response_text.split('\n') if q.strip()]
            return questions[:3]  # Return max 3 questions
            
        except Exception as e:
            print(f"Error generating related questions: {e}")
            return self._mock_related_questions(question, language)
    
    def explain_concept(self, concept: str, context: str, language: str = "en") -> str:
        """Explain a concept in detail"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_explain_concept(concept, language)
        
        try:
            prompt = f"""
            Explain the concept "{concept}" in detail using the provided context.
            Explanation should be in {language}.
            Be clear, educational, and include examples if possible.
            
            Context: {context[:2000]}
            
            Explanation:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator explaining concepts clearly."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error explaining concept: {e}")
            return self._mock_explain_concept(concept, language)
    
    def generate_practice_questions(self, text: str, num_questions: int, difficulty: str, language: str = "en") -> List[Dict[str, Any]]:
        """Generate practice questions with specific difficulty"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_practice_questions(num_questions, difficulty, language)
        
        try:
            prompt = f"""
            Generate {num_questions} practice questions based on the study material.
            Questions should be {difficulty} difficulty and in {language}.
            Each question should have 4 options with one correct answer.
            
            Text: {text[:3000]}
            
            Return in this JSON format:
            [
                {{
                    "question": "Question text",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": 0,
                    "explanation": "Explanation",
                    "difficulty": "{difficulty}"
                }}
            ]
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert creating practice questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.8
            )
            
            try:
                questions = json.loads(response.choices[0].message.content.strip())
                return questions
            except json.JSONDecodeError:
                return self._mock_practice_questions(num_questions, difficulty, language)
                
        except Exception as e:
            print(f"Error generating practice questions: {e}")
            return self._mock_practice_questions(num_questions, difficulty, language)
    
    def generate_learning_suggestions(self, material_titles: List[str], language: str = "en") -> List[str]:
        """Generate personalized learning suggestions"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_learning_suggestions(material_titles, language)
        
        try:
            prompt = f"""
            Generate 5 personalized learning suggestions based on these study materials.
            Suggestions should be in {language}.
            Be specific and actionable.
            
            Materials: {', '.join(material_titles)}
            
            Suggestions:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert learning advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content.strip()
            suggestions = [s.strip() for s in response_text.split('\n') if s.strip()]
            return suggestions[:5]
            
        except Exception as e:
            print(f"Error generating learning suggestions: {e}")
            return self._mock_learning_suggestions(material_titles, language)
    
    def generate_topic_summary(self, topic: str, text: str, language: str = "en") -> str:
        """Generate comprehensive topic summary"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_topic_summary(topic, language)
        
        try:
            prompt = f"""
            Create a comprehensive summary of the topic "{topic}" based on the provided text.
            Summary should be in {language}.
            Include key concepts, main points, and important details.
            
            Text: {text[:4000]}
            
            Summary:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert creating comprehensive topic summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating topic summary: {e}")
            return self._mock_topic_summary(topic, language)
    
    # Mock methods for demo purposes
    def _mock_summary(self, text: str, language: str) -> str:
        if language == "hi":
            return "यह अध्ययन सामग्री का एक संक्षिप्त सारांश है। मुख्य अवधारणाएं और महत्वपूर्ण बिंदु शामिल हैं।"
        elif language == "mr":
            return "हा अभ्यास साहित्याचा संक्षिप्त सारांश आहे. मुख्य संकल्पना आणि महत्वाचे मुद्दे समाविष्ट आहेत."
        else:
            return "This is a concise summary of the study material. It covers key concepts and important points."
    
    def _mock_quiz_questions(self, text: str, num_questions: int, language: str) -> List[Dict[str, Any]]:
        questions = []
        for i in range(num_questions):
            if language == "hi":
                question = f"प्रश्न {i+1}: यह अध्ययन सामग्री के बारे में क्या सही है?"
                options = ["विकल्प A", "विकल्प B", "विकल्प C", "विकल्प D"]
            elif language == "mr":
                question = f"प्रश्न {i+1}: हा अभ्यास साहित्याबद्दल काय बरोबर आहे?"
                options = ["पर्याय A", "पर्याय B", "पर्याय C", "पर्याय D"]
            else:
                question = f"Question {i+1}: What is correct about this study material?"
                options = ["Option A", "Option B", "Option C", "Option D"]
            
            questions.append({
                "question": question,
                "options": options,
                "correct_answer": 0,
                "explanation": "This is the correct answer based on the study material.",
                "difficulty": "medium"
            })
        return questions
    
    def _mock_flashcards(self, text: str, num_cards: int, language: str) -> List[Dict[str, str]]:
        cards = []
        for i in range(num_cards):
            if language == "hi":
                front = f"अवधारणा {i+1}"
                back = f"अवधारणा {i+1} की व्याख्या"
            elif language == "mr":
                front = f"संकल्पना {i+1}"
                back = f"संकल्पना {i+1} ची व्याख्या"
            else:
                front = f"Concept {i+1}"
                back = f"Definition of concept {i+1}"
            
            cards.append({
                "front": front,
                "back": back,
                "difficulty": "medium"
            })
        return cards
    
    def _mock_answer(self, question: str, context: str, language: str) -> str:
        if language == "hi":
            return "यह प्रश्न अध्ययन सामग्री के आधार पर उत्तर दिया गया है।"
        elif language == "mr":
            return "हा प्रश्न अभ्यास साहित्याच्या आधारावर उत्तर दिले आहे."
        else:
            return "This question is answered based on the study material provided."
    
    def _mock_translate(self, content: str, target_language: str) -> str:
        if target_language == "hi":
            return "यह सामग्री हिंदी में अनुवादित की गई है।"
        elif target_language == "mr":
            return "हा साहित्य मराठीत भाषांतर केले आहे."
        else:
            return "This content has been translated to the target language."
    
    def _mock_related_questions(self, question: str, language: str) -> List[str]:
        if language == "hi":
            return [
                "इस विषय के बारे में आप क्या जानते हैं?",
                "इस अवधारणा को कैसे समझा जा सकता है?",
                "इसका व्यावहारिक उपयोग क्या है?"
            ]
        elif language == "mr":
            return [
                "या विषयाबद्दल तुम्हाला काय माहित आहे?",
                "ही संकल्पना कशी समजून घेता येईल?",
                "याचा व्यावहारिक वापर काय आहे?"
            ]
        else:
            return [
                "What do you know about this topic?",
                "How can this concept be understood?",
                "What are its practical applications?"
            ]
    
    def _mock_explain_concept(self, concept: str, language: str) -> str:
        if language == "hi":
            return f"'{concept}' एक महत्वपूर्ण अवधारणा है। यह अध्ययन सामग्री में विस्तार से समझाया गया है।"
        elif language == "mr":
            return f"'{concept}' ही एक महत्वाची संकल्पना आहे. हे अभ्यास साहित्यात तपशीलवार स्पष्ट केले आहे."
        else:
            return f"'{concept}' is an important concept. It is explained in detail in the study material."
    
    def _mock_practice_questions(self, num_questions: int, difficulty: str, language: str) -> List[Dict[str, Any]]:
        questions = []
        for i in range(num_questions):
            if language == "hi":
                question = f"प्रश्न {i+1}: यह अवधारणा किस बारे में है?"
                options = ["विकल्प A", "विकल्प B", "विकल्प C", "विकल्प D"]
            elif language == "mr":
                question = f"प्रश्न {i+1}: ही संकल्पना कशाबद्दल आहे?"
                options = ["पर्याय A", "पर्याय B", "पर्याय C", "पर्याय D"]
            else:
                question = f"Question {i+1}: What is this concept about?"
                options = ["Option A", "Option B", "Option C", "Option D"]
            
            questions.append({
                "question": question,
                "options": options,
                "correct_answer": 0,
                "explanation": "This is the correct answer based on the study material.",
                "difficulty": difficulty
            })
        return questions
    
    def _mock_learning_suggestions(self, material_titles: List[str], language: str) -> List[str]:
        if language == "hi":
            return [
                "अपने अध्ययन सामग्री को नियमित रूप से दोहराएं",
                "क्विज़ लेकर अपनी समझ को जांचें",
                "फ्लैशकार्ड्स का उपयोग करें",
                "अवधारणाओं को अपने शब्दों में समझाएं",
                "नियमित अध्ययन समय निर्धारित करें"
            ]
        elif language == "mr":
            return [
                "तुमच्या अभ्यास साहित्याची नियमित पुनरावृत्ती करा",
                "क्विझ घेऊन तुमची समज तपासा",
                "फ्लॅशकार्ड्स वापरा",
                "संकल्पना स्वतःच्या शब्दांत स्पष्ट करा",
                "नियमित अभ्यास वेळ निश्चित करा"
            ]
        else:
            return [
                "Regularly review your study materials",
                "Test your understanding with quizzes",
                "Use flashcards for memorization",
                "Explain concepts in your own words",
                "Set regular study time"
            ]
    
    def _mock_topic_summary(self, topic: str, language: str) -> str:
        if language == "hi":
            return f"'{topic}' विषय का यह एक व्यापक सारांश है। इसमें मुख्य अवधारणाएं, महत्वपूर्ण बिंदु और विस्तृत विवरण शामिल हैं।"
        elif language == "mr":
            return f"'{topic}' विषयाचा हा एक व्यापक सारांश आहे. त्यामध्ये मुख्य संकल्पना, महत्वाचे मुद्दे आणि तपशीलवार माहिती समाविष्ट आहे."
        else:
            return f"This is a comprehensive summary of the topic '{topic}'. It includes key concepts, main points, and detailed information."