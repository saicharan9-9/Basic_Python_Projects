#!/bin/bash

echo "🧞‍♂️ Starting StudyGenie Development Environment..."

# Check if required tools are installed
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    fi
}

echo "Checking dependencies..."
check_dependency python3
check_dependency node
check_dependency npm

# Check for OpenAI API key
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Backend .env file not found. Creating from template..."
    cp backend/.env.example backend/.env
    echo "📝 Please edit backend/.env with your OpenAI API key and other settings"
    echo "   Then run this script again."
    exit 1
fi

# Start backend
echo "🐍 Starting Python backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start backend server in background
echo "Starting FastAPI server on port 8000..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "⚛️  Starting React frontend..."
cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Start frontend server
echo "Starting React development server on port 3000..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 StudyGenie is starting up!"
echo ""
echo "📍 Access the application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait