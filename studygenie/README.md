# 🧞‍♂️ StudyGenie - Personalized Study Guide Generator

StudyGenie transforms raw learning materials (PDFs, images, handwritten notes) into interactive study content using AI. It features personalized learning paths, multilingual support, and comprehensive progress tracking.

## ✨ Features

### 📚 Content Processing
- **Multi-format Support**: Upload PDFs, images (JPG, PNG, TIFF), and text files
- **OCR Integration**: Extract text from handwritten notes and images using Tesseract
- **Smart Text Processing**: Clean and preprocess extracted content for optimal AI processing

### 🤖 AI-Powered Content Generation
- **Automatic Summarization**: Generate concise, student-friendly summaries
- **Smart Flashcards**: Create 15+ flashcards with spaced repetition scheduling
- **Dynamic Quizzes**: Generate 10+ questions with multiple choice, true/false, and short answer formats
- **Topic Extraction**: Automatically identify key concepts and learning objectives

### 🧠 Intelligent Study System
- **Spaced Repetition**: SM-2 algorithm implementation for optimal flashcard scheduling
- **Adaptive Learning**: Personalized study paths based on performance history
- **Progress Tracking**: Comprehensive analytics with study streaks, time tracking, and performance metrics

### 🤝 RAG-Powered AI Tutor
- **Context-Aware Answers**: Ask questions and get answers based on your uploaded materials
- **Source Attribution**: Transparent sourcing from your study materials
- **Confidence Scoring**: AI confidence levels for answer reliability

### 🌍 Multilingual Support
- **Language Options**: English, Hindi (हिंदी), Marathi (मराठी)
- **Smart Translation**: Convert summaries and study materials to preferred language
- **Regional Learning**: Tailored for diverse educational contexts

### 📊 Advanced Analytics
- **Progress Dashboard**: Visual learning analytics with charts and heatmaps
- **Performance Insights**: Identify weak and strong subject areas
- **Study Streaks**: Gamified learning with streak tracking
- **Learning Curves**: Visualize improvement over time

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite by default)
- OpenAI API key
- Tesseract OCR

### Backend Setup

1. **Navigate to backend directory**:
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
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database settings
   ```

5. **Install Tesseract OCR**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar
   
   # macOS
   brew install tesseract tesseract-lang
   
   # Windows
   # Download from https://github.com/UB-Mannheim/tesseract/wiki
   ```

6. **Run the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd studygenie/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🎯 Demo Flow

### Example: Physics Chapter Study Session

1. **Upload**: Student uploads "Physics Chapter 12 - Electricity.pdf"
2. **Processing**: 
   - Text extraction from PDF (15 pages)
   - AI generates comprehensive summary
   - Creates 15 flashcards covering key concepts
   - Generates 10 MCQ questions with explanations
3. **Study Session**:
   - Student reviews flashcards using spaced repetition
   - Takes quiz and scores 75%
   - AI tutor explains incorrect answers in simple terms
4. **Analytics Update**:
   - Dashboard shows updated progress
   - Identifies "Ohm's Law" as weak area
   - Recommends focused review sessions

## 🏗️ Architecture

### Backend (Python FastAPI)
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Database ORM with PostgreSQL/SQLite support
- **OpenAI Integration**: GPT-4 for content generation and explanations
- **FAISS Vector Database**: Efficient similarity search for RAG
- **Tesseract OCR**: Text extraction from images
- **JWT Authentication**: Secure user authentication

### Frontend (React TypeScript)
- **React 18**: Modern React with hooks and context
- **Material-UI**: Beautiful, accessible component library
- **React Query**: Efficient data fetching and caching
- **Framer Motion**: Smooth animations and transitions
- **Recharts**: Interactive data visualization
- **React Router**: Client-side routing

### AI/ML Stack
- **LangChain**: Framework for LLM applications
- **Sentence Transformers**: Text embeddings for semantic search
- **OpenAI GPT-4**: Content generation and explanations
- **FAISS**: Vector similarity search
- **SM-2 Algorithm**: Spaced repetition scheduling

## 📁 Project Structure

```
studygenie/
├── backend/
│   ├── app/
│   │   ├── routers/          # API route handlers
│   │   ├── services/         # Business logic services
│   │   ├── models.py         # Pydantic models
│   │   ├── database_models.py # SQLAlchemy models
│   │   └── main.py          # FastAPI application
│   ├── uploads/             # File storage
│   ├── data/               # Vector database storage
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API communication
│   │   ├── hooks/         # Custom React hooks
│   │   └── types/         # TypeScript definitions
│   └── package.json       # Node.js dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=postgresql://username:password@localhost/studygenie

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=./uploads
VECTOR_DB_PATH=./data/vector_db

# Optional: Google Vision API (alternative to Tesseract)
GOOGLE_VISION_API_KEY=your_google_vision_api_key_here
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Document Management
- `POST /api/upload/document` - Upload document
- `POST /api/upload/generate-study-material/{id}` - Generate study content
- `GET /api/upload/documents` - List user documents
- `DELETE /api/upload/document/{id}` - Delete document

### Study Features
- `GET /api/study/flashcards/due` - Get due flashcards
- `POST /api/study/flashcard/{id}/review` - Submit flashcard review
- `GET /api/study/quiz/{id}` - Get quiz
- `POST /api/study/quiz/{id}/attempt` - Submit quiz attempt
- `POST /api/study/tutor/ask` - Ask AI tutor

### Progress & Analytics
- `GET /api/progress/dashboard` - Dashboard statistics
- `GET /api/progress/study-heatmap` - Study activity heatmap
- `GET /api/progress/topic-performance` - Topic performance analysis
- `GET /api/progress/learning-curve` - Learning progress over time

## 🎨 UI/UX Features

- **Responsive Design**: Works seamlessly on desktop and mobile
- **Dark/Light Mode**: Automatic theme detection
- **Smooth Animations**: Framer Motion for enhanced user experience
- **Accessibility**: WCAG compliant with keyboard navigation
- **Progress Visualization**: Interactive charts and heatmaps
- **Drag & Drop**: Intuitive file upload interface

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **File Validation**: Strict file type and size validation
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy
- **CORS Configuration**: Secure cross-origin resource sharing

## 🚀 Deployment

### Using Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Deployment

1. **Backend**: Deploy FastAPI with Gunicorn + Nginx
2. **Frontend**: Build and serve with Nginx
3. **Database**: PostgreSQL with connection pooling
4. **File Storage**: AWS S3 or local filesystem
5. **Vector Database**: Persistent FAISS index storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Hugging Face for transformer models
- Tesseract OCR community
- Material-UI team
- FastAPI and React communities

---

**Built with ❤️ for learners everywhere**