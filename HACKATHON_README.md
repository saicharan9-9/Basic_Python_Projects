# StudyGenie 🧠✨
## AI-Powered Study Guide Generator

**Hackathon Project** - Transform any PDF/notes into interactive quizzes, flashcards, and AI tutor support with multilingual capabilities.

## 🚀 Quick Start (2 minutes!)

### Backend Only (Recommended for Demo)
```bash
chmod +x start.sh
./start.sh
```
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Full Stack with Docker
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## 🎯 Demo Flow (5 minutes)

1. **Upload PDF** → `/api/study/upload` (Physics/Math chapter)
2. **Generate Quiz** → `/api/study/{id}/generate-quiz` (10 questions)
3. **Create Flashcards** → `/api/study/{id}/generate-flashcards` (15 cards)
4. **Ask AI Tutor** → `/api/tutor/ask` (RAG-powered Q&A)
5. **Track Progress** → `/api/progress/summary` (Analytics)

## 🌟 Key Features

- **Smart PDF Processing** with OCR for handwritten notes
- **AI-Generated Content** (quizzes, flashcards, summaries)
- **Multilingual Support** (English, Hindi, Marathi, 7+ languages)
- **RAG-Powered AI Tutor** answering questions from your materials
- **Progress Tracking** with study streaks and analytics
- **Beautiful UI** with dark/light themes

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python + LangChain + OpenAI
- **Frontend**: React + TypeScript + Tailwind CSS
- **AI**: GPT-3.5 + RAG + Sentence Embeddings
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Deployment**: Docker + Docker Compose

## 🎨 UI Highlights

- Modern, responsive design
- Interactive flashcards
- Progress visualization
- Real-time updates
- Beautiful animations

## 🔑 No API Key Required!

The app works with **mock responses** for demo purposes. Add your OpenAI API key in `.env` for real AI features.

## 📱 Perfect for Hackathon

- **Ready to demo** in 5 minutes
- **Beautiful UI** that impresses judges
- **AI features** that showcase innovation
- **Multilingual** for global impact
- **Scalable architecture** for future development

---

**🎉 Ready to win your hackathon!**

Transform study materials into intelligent learning experiences with AI-powered personalization.