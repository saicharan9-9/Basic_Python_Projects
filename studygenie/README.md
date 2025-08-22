# StudyGenie - Personalized Study Guide Generator

StudyGenie is an AI-powered study companion that transforms raw learning materials (PDFs, documents, handwritten notes) into interactive study content including quizzes, flashcards, and personalized learning paths.

## 🌟 Features

### Core Functionality
- **Document Processing**: Upload PDFs, DOCX, TXT files, and images with OCR text extraction
- **AI Content Generation**: Auto-generate summaries, quizzes, and flashcards from your materials
- **Spaced Repetition**: Intelligent flashcard scheduling for optimal memory retention
- **RAG-Powered AI Tutor**: Interactive AI assistant that answers questions from your study materials
- **Progress Tracking**: Comprehensive analytics with study streaks, knowledge heatmaps, and performance insights

### Multilingual Support
- **Interface Languages**: English, Hindi (हिंदी), Marathi (मराठी)
- **Content Generation**: Create study materials in multiple languages
- **Translation**: Convert summaries and content between supported languages

### Advanced Features
- **Personalized Learning**: Adaptive difficulty based on performance
- **Subject Organization**: Track progress across different subjects
- **Interactive Dashboard**: Visual progress tracking and study analytics
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.8+
- **Database**: SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL)
- **AI Integration**: OpenAI GPT for content generation
- **Vector Database**: ChromaDB for RAG functionality
- **Document Processing**: PyPDF2, Tesseract OCR, python-docx
- **Authentication**: JWT-based auth with bcrypt password hashing

### Frontend (React)
- **Framework**: React 18 with modern hooks
- **Styling**: Tailwind CSS with custom design system
- **State Management**: React Query for server state
- **Routing**: React Router v6
- **UI Components**: Custom component library with Lucide React icons
- **Internationalization**: Built-in multi-language support

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Tesseract OCR (for image text extraction)

### Backend Setup

1. **Clone and navigate to backend**:
```bash
cd studygenie/backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r ../requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Create upload directories**:
```bash
mkdir uploads chroma_db
```

6. **Run the backend**:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**:
```bash
cd studygenie/frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## 📋 Environment Configuration

### Backend (.env)
```env
# Database
DATABASE_URL=sqlite:///./studygenie.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI API (Required for AI features)
OPENAI_API_KEY=your-openai-api-key-here

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800  # 50MB

# Vector Database
CHROMA_PERSIST_DIR=./chroma_db
```

## 🎯 Usage Examples

### Example Demo Flow

1. **Upload Document**: Student uploads a Physics chapter PDF
2. **AI Processing**: App extracts text and generates study materials
3. **Study Session**: 
   - 15 flashcards created automatically
   - 10 multiple-choice questions generated
   - Summary in preferred language
4. **Interactive Learning**: Student takes quiz, reviews flashcards
5. **Progress Tracking**: Dashboard updates with performance metrics
6. **AI Tutor**: Student asks questions about confusing concepts
7. **Adaptive Learning**: System identifies weak areas and adjusts future content

### API Examples

**Upload Document**:
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@physics_chapter.pdf"
```

**Generate Quiz**:
```bash
curl -X POST "http://localhost:8000/api/study/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": 1,
    "content_type": "quiz",
    "language": "en",
    "difficulty_level": "medium"
  }'
```

**Chat with AI Tutor**:
```bash
curl -X POST "http://localhost:8000/api/ai-tutor/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain photosynthesis in simple terms",
    "language": "en",
    "document_id": 1
  }'
```

## 🔧 Advanced Configuration

### Database Migration (PostgreSQL)
```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/studygenie

# Run migrations
alembic upgrade head
```

### Production Deployment
```bash
# Backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
# Serve build folder with nginx or similar
```

## 🧪 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
black app/
flake8 app/

# Frontend linting
npm run lint
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Coming Soon]
- **Issues**: GitHub Issues
- **Email**: support@studygenie.com

## 🎉 Acknowledgments

- OpenAI for GPT API
- ChromaDB for vector database
- Tesseract OCR for text extraction
- React and FastAPI communities

---

**StudyGenie** - Transform your learning with AI-powered personalized study guides! 🧠✨