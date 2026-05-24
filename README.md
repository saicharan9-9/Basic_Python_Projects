# StudyGenie 🧠✨
## Personalized Study Guide Generator

**Hackathon Project** - AI-powered learning platform that transforms raw materials into interactive study content.

### 🚀 Features

- **Smart Content Processing**: Upload PDFs, handwritten notes → Auto-extract text (OCR support)
- **AI-Powered Generation**: Automatic summaries, quizzes, and flashcards
- **Personalized Learning**: Adaptive study flow based on performance analytics
- **Interactive AI Tutor**: RAG-powered Q&A from your study materials
- **Multilingual Support**: English, Hindi, Marathi, and regional languages
- **Progress Dashboard**: Visual progress tracking, streaks, and knowledge heatmaps
- **Spaced Repetition**: Built-in flashcard system with active recall

### 🎯 Demo Flow
1. Student uploads Physics Chapter PDF
2. App generates 15 flashcards + 10 MCQs
3. Student takes quiz
4. Dashboard updates progress
5. AI tutor explains wrong answers in simple terms

### 🛠️ Tech Stack

**Backend**: FastAPI, Python, LangChain, OpenAI
**Frontend**: React, TypeScript, Tailwind CSS
**Database**: PostgreSQL, Redis
**AI/ML**: Transformers, Sentence Embeddings, RAG
**Deployment**: Docker, Docker Compose

### 🚀 Quick Start

1. **Clone & Setup**
```bash
git clone <your-repo>
cd StudyGenie
```

2. **Install Dependencies**
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

3. **Environment Setup**
```bash
cp .env.example .env
# Add your OpenAI API key and database credentials
```

4. **Run the Application**
```bash
# Backend
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm start
```

5. **Access the App**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 📁 Project Structure
```
StudyGenie/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── models/            # AI models and embeddings
├── database/          # Database schemas and migrations
├── utils/             # Utility functions
└── docker-compose.yml # Development environment
```

### 🎨 UI/UX Features
- Modern, responsive design
- Dark/Light theme toggle
- Progress visualization
- Interactive flashcards
- Real-time progress updates

### 🔮 Future Enhancements
- Mobile app (React Native)
- Voice-based interactions
- Collaborative study groups
- Advanced analytics
- Integration with LMS platforms

---

**Built with ❤️ for Hackathon 2024**
*Transform your study materials into intelligent learning experiences!*