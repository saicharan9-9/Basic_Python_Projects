# StudyGenie Setup Guide 🚀

## Quick Start (Recommended)

### Step 1: Prerequisites
Make sure you have these installed:
```bash
# Check if you have the required tools
python3 --version  # Should be 3.8+
node --version     # Should be 16+
npm --version      # Should be 8+
```

If any are missing, install them:
- **Python 3.8+**: Download from [python.org](https://python.org)
- **Node.js 16+**: Download from [nodejs.org](https://nodejs.org)
- **Tesseract OCR**: 
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### Step 2: Get OpenAI API Key (Required for AI features)
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Create account or login
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-...`)

### Step 3: Configure Environment
```bash
# Navigate to the project
cd studygenie/backend

# Copy environment template
cp .env.example .env

# Edit the .env file and add your OpenAI API key
# Replace the empty OPENAI_API_KEY= line with:
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 4: Run the Application
```bash
# From the studygenie root directory
./start.sh
```

That's it! The script will:
- Set up Python virtual environment
- Install all dependencies
- Create necessary directories
- Start both backend and frontend servers

## Manual Setup (Alternative)

If the quick start doesn't work, follow these manual steps:

### Backend Setup
```bash
cd studygenie/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Create directories
mkdir -p uploads chroma_db

# Configure environment (add your OpenAI API key)
cp .env.example .env
# Edit .env file with your API key

# Start backend
python -m app.main
```

### Frontend Setup (New Terminal)
```bash
cd studygenie/frontend

# Install dependencies
npm install

# Start frontend
npm start
```

## Access the Application

Once running, you can access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## First Time Usage

1. **Register Account**: Create your account at http://localhost:3000/register
2. **Login**: Sign in with your credentials
3. **Upload Document**: Go to Documents page and upload a PDF/document
4. **Generate Study Materials**: Create quizzes, flashcards, or summaries
5. **Start Studying**: Take quizzes, review flashcards, chat with AI tutor

## Troubleshooting

### Common Issues

**1. "ModuleNotFoundError" or missing dependencies**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**2. "Port already in use"**
```bash
# Kill processes on ports 3000 and 8000
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:8000 | xargs kill -9
```

**3. "OpenAI API Error"**
- Check your API key in `backend/.env`
- Ensure you have credits in your OpenAI account
- Verify the key starts with `sk-`

**4. "Tesseract not found"**
```bash
# Install Tesseract OCR
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# Windows: Download installer from GitHub
```

**5. Database issues**
```bash
# Delete and recreate database
rm backend/studygenie.db
# Restart the backend - it will recreate the database
```

### Performance Tips

1. **For better AI responses**: Use clear, well-formatted documents
2. **For faster processing**: Keep documents under 10MB when possible
3. **For better OCR**: Use high-quality, clear images
4. **For optimal flashcards**: Upload content with clear concepts and definitions

## Development Mode

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm start
```

### Database Management
```bash
# View database
sqlite3 backend/studygenie.db
.tables
.quit

# Reset database
rm backend/studygenie.db
# Restart backend to recreate
```

## Production Deployment

### Environment Variables
```bash
# Production .env
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=your-openai-key
```

### Backend Production
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Production
```bash
npm run build
# Serve the build folder with nginx or similar
```

## Support

If you encounter any issues:
1. Check the console logs in your browser (F12)
2. Check the backend logs in the terminal
3. Verify all prerequisites are installed
4. Ensure your OpenAI API key is valid and has credits

Happy studying with StudyGenie! 🧠✨