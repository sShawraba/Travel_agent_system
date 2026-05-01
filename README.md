# Smart Travel Planner

A full-stack AI-powered travel planning system built with FastAPI, React, and Google Gemini.

## Features

- 🤖 AI-powered travel recommendations using Google Gemini
- 🎯 Travel style classification (adventure, luxury, cultural, relaxation, budget)
- 🌍 Destination recommendations with descriptions
- 🌤️ Weather information for destinations
- 💬 Simple chat interface
- 📊 LangSmith tracing for agent execution

## Tech Stack

- **Backend**: FastAPI + LangGraph + LangChain
- **Frontend**: React + Vite
- **LLM**: Google Gemini (via LangChain)
- **Infrastructure**: Docker + docker-compose
- **Database**: PostgreSQL

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Google Gemini API key
- LangChain API key (for tracing)

### Environment Setup

1. Copy `.env.example` and set your keys:
```bash
cp backend/.env.example backend/.env
```

2. Edit `backend/.env` with your API keys:
```
GOOGLE_API_KEY=your_key_here
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
LANGSMITH_PROJECT=travel-ai-agent
```

### Run with Docker Compose

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Local Development (without Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── core/
│   │   │   └── config.py        # Settings
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── routes/
│   │   │   └── travel.py        # API endpoints
│   │   ├── services/
│   │   │   ├── agent_service.py # LangGraph agent
│   │   │   └── llm_service.py   # Gemini integration
│   │   └── tools/
│   │       ├── classifier_tool.py
│   │       ├── rag_tool.py
│   │       └── weather_tool.py
│   ├── Dockerfile
│   ├── .env.example
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── App.css
│   ├── vite.config.js
│   ├── package.json
│   ├── index.html
│   └── Dockerfile
└── docker-compose.yml
```

## API Endpoints

### POST `/api/plan-trip`

Plan a trip based on user description.

**Request:**
```json
{
  "query": "I want to relax at a beach"
}
```

**Response:**
```json
{
  "recommended_destination": "Bali, Indonesia",
  "travel_style": "relaxation",
  "explanation": "Bali is perfect for relaxation...",
  "weather_summary": "28°C, Sunny"
}
```

## Agent Flow

1. **Classify** → Determine travel style from user query
2. **Retrieve** → Get destination info from RAG tool
3. **Weather** → Fetch weather for destination
4. **Synthesize** → Generate explanation using Gemini

## Development Notes

- All backend routes are async
- Dependency injection for services
- Graceful error handling with fallbacks
- LangSmith tracing automatically enabled
- Mock tools for quick development
- Type hints throughout codebase
