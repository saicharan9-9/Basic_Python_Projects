# StudyGenie Demo Guide 🧠✨

## 🚀 Quick Start

### Option 1: Simple Backend Only (Recommended for Hackathon)
```bash
./start.sh
```
This will start the backend server at http://localhost:8000

### Option 2: Full Stack with Docker
```bash
docker-compose up --build
```
This will start both backend and frontend services.

## 🎯 Demo Flow

### 1. **Upload Study Material** 📚
- Go to http://localhost:8000/docs (API docs)
- Use the `/api/study/upload` endpoint
- Upload a PDF file (Physics, Math, or any educational content)
- The AI will automatically:
  - Extract text (with OCR support for handwritten notes)
  - Generate a summary
  - Support multiple languages

### 2. **Generate Quiz Questions** 🧪
- Use the `/api/study/{material_id}/generate-quiz` endpoint
- Specify number of questions (default: 10)
- Choose language (English, Hindi, Marathi, etc.)
- AI generates multiple choice questions with explanations

### 3. **Create Flashcards** 🗂️
- Use the `/api/study/{material_id}/generate-flashcards` endpoint
- Specify number of cards (default: 15)
- AI creates front/back content with difficulty levels
- Built-in spaced repetition algorithm

### 4. **AI Tutor Q&A** 🤖
- Use the `/api/tutor/ask` endpoint
- Ask questions about your study material
- AI answers using RAG (Retrieval Augmented Generation)
- Get related questions for deeper learning

### 5. **Progress Tracking** 📊
- Record study sessions: `/api/progress/record-study-session`
- Track quiz attempts: `/api/progress/record-quiz-attempt`
- Monitor flashcard reviews: `/api/progress/update-flashcard-review`
- View analytics: `/api/progress/summary`

## 🌟 Key Features Demonstrated

### **Smart Content Processing**
- PDF text extraction with OCR
- Handwritten note recognition
- Automatic content summarization

### **AI-Powered Generation**
- Context-aware quiz questions
- Educational flashcards
- Personalized learning suggestions

### **Multilingual Support**
- English, Hindi, Marathi, and 7+ regional languages
- Content translation
- Localized quiz generation

### **Personalized Learning**
- Study streak tracking
- Progress analytics
- Adaptive difficulty levels
- Spaced repetition algorithms

### **Interactive AI Tutor**
- RAG-powered Q&A
- Concept explanations
- Related question generation
- Practice question creation

## 🔧 API Endpoints Overview

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Study Materials
- `POST /api/study/upload` - Upload PDF/notes
- `GET /api/study/materials` - List all materials
- `POST /api/study/{id}/generate-quiz` - Create quiz
- `POST /api/study/{id}/generate-flashcards` - Create flashcards

### AI Tutor
- `POST /api/tutor/ask` - Ask questions
- `POST /api/tutor/translate` - Translate content
- `POST /api/tutor/explain-concept` - Get explanations
- `GET /api/tutor/supported-languages` - List languages

### Progress Tracking
- `GET /api/progress/summary` - Overall progress
- `GET /api/progress/subjects` - Subject-wise progress
- `POST /api/progress/record-study-session` - Log study time
- `GET /api/progress/weekly-progress` - Weekly analytics

## 📱 Frontend Features (When Running Full Stack)

### **Modern UI/UX**
- Responsive design for all devices
- Dark/light theme toggle
- Beautiful animations and transitions
- Progress visualization

### **Interactive Components**
- Drag & drop file upload
- Interactive flashcards
- Real-time progress updates
- Beautiful charts and graphs

## 🎨 Customization Options

### **Language Support**
- Add new languages in `backend/services/ai_service.py`
- Customize mock responses for different languages
- Implement language-specific UI elements

### **AI Models**
- Replace OpenAI with local models
- Customize prompt engineering
- Add new content generation types

### **UI Themes**
- Modify `frontend/src/index.css`
- Update color schemes in `tailwind.config.js`
- Add new animations and effects

## 🚀 Hackathon Presentation Tips

### **1. Live Demo Flow**
1. Show the beautiful landing page
2. Upload a Physics PDF in real-time
3. Generate quiz questions instantly
4. Create flashcards automatically
5. Ask AI tutor questions
6. Show progress dashboard

### **2. Key Talking Points**
- **Problem Solved**: Manual study material conversion is time-consuming
- **AI Innovation**: RAG + LLM for personalized learning
- **Multilingual**: Breaking language barriers in education
- **Scalability**: Works with any PDF/text content
- **User Experience**: Beautiful, intuitive interface

### **3. Technical Highlights**
- FastAPI backend with async support
- React frontend with TypeScript
- AI integration with fallback modes
- OCR for handwritten notes
- Spaced repetition algorithms
- Real-time progress tracking

### **4. Future Roadmap**
- Mobile app development
- Voice-based interactions
- Collaborative study groups
- Advanced analytics
- LMS integration

## 🐛 Troubleshooting

### **Common Issues**
1. **Port conflicts**: Change ports in `.env` or `docker-compose.yml`
2. **Dependencies**: Ensure Python 3.8+ and Node.js 16+
3. **File permissions**: Make sure `start.sh` is executable
4. **API errors**: Check console logs for detailed error messages

### **Getting Help**
- Check API documentation at `/docs`
- Review console logs for errors
- Ensure all dependencies are installed
- Verify file paths and permissions

---

**🎉 Ready to showcase StudyGenie at your hackathon!**

Transform any study material into an interactive learning experience with AI-powered personalization and multilingual support.