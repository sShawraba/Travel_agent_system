#!/bin/bash

# Quick start script for Smart Travel Planner

set -e

echo "🚀 Smart Travel Planner - Quick Start"
echo "====================================="
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo -e "✅ Created backend/.env"
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env with your API keys!"
    echo "   - GOOGLE_API_KEY"
    echo "   - LANGCHAIN_API_KEY"
    echo ""
    echo "Get your keys from:"
    echo "   - Google Gemini: https://makersuite.google.com/"
    echo "   - LangChain: https://smith.langchain.com/"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "🐳 Starting services with Docker Compose..."
echo ""
docker-compose up --build

echo ""
echo "✅ Services are running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
