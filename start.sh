#!/bin/bash

echo "🚀 Starting StudyGenie - AI-Powered Study Guide Generator"
echo "========================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key if you have one."
    echo "   The app will work with mock responses without an API key."
fi

# Start the backend
echo "🔧 Starting StudyGenie Backend..."
echo "   Backend will be available at: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the backend server"
echo ""

cd backend
python main.py