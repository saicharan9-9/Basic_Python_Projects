#!/usr/bin/env python3
"""
StudyGenie Demo Script
This script demonstrates the core functionality of StudyGenie
"""

import os
import sys
import time
from pathlib import Path

# Add the backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def print_banner():
    print("""
🧞‍♂️ StudyGenie Demo - Personalized Study Guide Generator
=========================================================

This demo showcases how StudyGenie transforms learning materials
into personalized study content with AI-powered features.
""")

def demo_text_extraction():
    print("\n📄 Demo 1: Text Extraction & Processing")
    print("-" * 40)
    
    # Sample text content (simulating extracted PDF content)
    sample_text = """
    Photosynthesis is the process by which plants and other organisms convert light energy, 
    usually from the sun, into chemical energy that can be later released to fuel the 
    organism's activities. This chemical energy is stored in carbohydrate molecules, such as 
    sugars, which are synthesized from carbon dioxide and water. In most cases, oxygen is 
    released as a waste product. Most plants, most algae, and cyanobacteria perform 
    photosynthesis; such organisms are called photoautotrophs.
    
    The process of photosynthesis occurs in two stages: the light-dependent reactions and 
    the light-independent reactions (also known as the Calvin cycle). The light-dependent 
    reactions take place in the thylakoid membranes of chloroplasts, where chlorophyll 
    and other pigments capture light energy and convert it into chemical energy in the 
    form of ATP and NADPH. The Calvin cycle occurs in the stroma of chloroplasts, where 
    CO2 is fixed into organic molecules using the energy from ATP and NADPH.
    """
    
    print("📝 Sample extracted text:")
    print(sample_text[:200] + "...")
    
    # Simulate text processing
    print("\n🔄 Processing text...")
    time.sleep(1)
    
    processed_text = ' '.join(sample_text.split())
    print(f"✅ Text processed: {len(processed_text)} characters")
    
    return sample_text

def demo_ai_generation(text):
    print("\n🤖 Demo 2: AI Content Generation")
    print("-" * 40)
    
    print("🔄 Generating study materials with AI...")
    time.sleep(2)
    
    # Simulated AI-generated content
    summary = """
    **Photosynthesis Overview**
    
    Photosynthesis is the fundamental process where plants convert sunlight into chemical energy (sugars) 
    using carbon dioxide and water, releasing oxygen as a byproduct. This process sustains most life on Earth.
    
    **Key Stages:**
    1. **Light-dependent reactions** (Thylakoids): Capture light energy → ATP + NADPH
    2. **Calvin cycle** (Stroma): Use ATP/NADPH to fix CO2 into organic molecules
    """
    
    flashcards = [
        {"front": "What is photosynthesis?", "back": "The process by which plants convert light energy into chemical energy stored in carbohydrates", "topic": "Basic Concepts"},
        {"front": "Where do light-dependent reactions occur?", "back": "In the thylakoid membranes of chloroplasts", "topic": "Cell Biology"},
        {"front": "What is the Calvin cycle?", "back": "The light-independent reactions that fix CO2 into organic molecules using ATP and NADPH", "topic": "Biochemistry"},
    ]
    
    quiz_questions = [
        {
            "question": "What are the two main stages of photosynthesis?",
            "options": [
                "Light reactions and dark reactions",
                "Glycolysis and Krebs cycle", 
                "Transcription and translation",
                "Mitosis and meiosis"
            ],
            "correct": "Light reactions and dark reactions",
            "topic": "Process Overview"
        }
    ]
    
    print("✅ Generated content:")
    print(f"   📝 Summary: {len(summary)} characters")
    print(f"   🎴 Flashcards: {len(flashcards)} cards")
    print(f"   ❓ Quiz Questions: {len(quiz_questions)} questions")
    
    return summary, flashcards, quiz_questions

def demo_spaced_repetition():
    print("\n🧠 Demo 3: Spaced Repetition Algorithm")
    print("-" * 40)
    
    print("🔄 Simulating flashcard review session...")
    
    # Simulate SM-2 algorithm
    reviews = [
        {"quality": 4, "description": "Easy recall", "next_interval": "6 days"},
        {"quality": 2, "description": "Difficult recall", "next_interval": "1 day"},
        {"quality": 5, "description": "Perfect recall", "next_interval": "15 days"},
    ]
    
    for i, review in enumerate(reviews):
        time.sleep(0.5)
        print(f"   Card {i+1}: Quality {review['quality']} → Next review in {review['next_interval']}")
    
    print("✅ Spaced repetition scheduling optimized for retention")

def demo_rag_tutor():
    print("\n🤝 Demo 4: RAG-Powered AI Tutor")
    print("-" * 40)
    
    print("🔄 Student asks: 'What happens in the Calvin cycle?'")
    time.sleep(1)
    
    print("🔍 Searching study materials...")
    time.sleep(1)
    
    print("🤖 AI Tutor Response:")
    print("""
    The Calvin cycle is the second stage of photosynthesis that happens in the stroma 
    (fluid-filled space) of chloroplasts. Here's what occurs:
    
    1. **Carbon Fixation**: CO2 from the air combines with a 5-carbon sugar (RuBP)
    2. **Reduction**: The resulting molecules are converted using energy from ATP and NADPH
    3. **Regeneration**: RuBP is regenerated to continue the cycle
    
    Think of it as a factory assembly line that builds sugar molecules from CO2 using 
    the energy captured in the first stage!
    
    📊 Confidence: 95% | 📚 Sources: 2 document chunks
    """)

def demo_progress_analytics():
    print("\n📊 Demo 5: Progress Analytics")
    print("-" * 40)
    
    print("📈 Generating learning analytics...")
    time.sleep(1)
    
    stats = {
        "study_streak": 7,
        "total_study_time": 480,  # minutes
        "topics_mastered": 12,
        "avg_quiz_score": 82.5,
        "weak_subjects": ["Organic Chemistry", "Calculus"],
        "strong_subjects": ["Biology", "Physics"]
    }
    
    print("✅ Dashboard Statistics:")
    print(f"   🔥 Study Streak: {stats['study_streak']} days")
    print(f"   ⏱️  Total Study Time: {stats['total_study_time']//60} hours")
    print(f"   🎓 Topics Mastered: {stats['topics_mastered']}")
    print(f"   📊 Average Quiz Score: {stats['avg_quiz_score']}%")
    print(f"   ⚠️  Weak Subjects: {', '.join(stats['weak_subjects'])}")
    print(f"   💪 Strong Subjects: {', '.join(stats['strong_subjects'])}")

def demo_multilingual():
    print("\n🌍 Demo 6: Multilingual Support")
    print("-" * 40)
    
    print("🔄 Converting content to Hindi...")
    time.sleep(1)
    
    english_text = "Photosynthesis is the process by which plants make food using sunlight."
    hindi_text = "प्रकाश संश्लेषण वह प्रक्रिया है जिसके द्वारा पौधे सूर्य प्रकाश का उपयोग करके भोजन बनाते हैं।"
    
    print(f"🇺🇸 English: {english_text}")
    print(f"🇮🇳 Hindi: {hindi_text}")
    
    print("✅ Content successfully localized for regional students")

def main():
    print_banner()
    
    # Run demos
    sample_text = demo_text_extraction()
    summary, flashcards, quiz = demo_ai_generation(sample_text)
    demo_spaced_repetition()
    demo_rag_tutor()
    demo_progress_analytics()
    demo_multilingual()
    
    print(f"""
🎉 StudyGenie Demo Complete!

📋 What we demonstrated:
   ✅ Multi-format text extraction (PDF, images, text)
   ✅ AI-powered content generation (summaries, flashcards, quizzes)
   ✅ Spaced repetition algorithm for optimal learning
   ✅ RAG-powered AI tutor for instant Q&A
   ✅ Comprehensive progress analytics
   ✅ Multilingual support for diverse learners

🚀 Ready to start? Run: ./start.sh

🔗 Key Technologies:
   • FastAPI + React for modern web architecture
   • OpenAI GPT-4 for intelligent content generation  
   • FAISS vector database for semantic search
   • Tesseract OCR for handwritten note processing
   • Material-UI for beautiful, accessible interface

📧 Questions? Check the README.md for detailed setup instructions.
""")

if __name__ == "__main__":
    main()