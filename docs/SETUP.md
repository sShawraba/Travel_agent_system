# Smart Travel Planner - Setup Guide

## Prerequisites

- Docker Desktop installed
- Google Gemini API key (get from https://makersuite.google.com/)
- LangChain API key (for LangSmith tracing)

## Step 1: Clone and Setup

```bash
cd /home/soup/travel-ai-agent
cp backend/.env.example backend/.env
```

## Step 2: Add Your API Keys

Edit `backend/.env`:
```
GOOGLE_API_KEY=your_google_gemini_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_TRACING_V2=true
LANGSMITH_PROJECT=travel-ai-agent
```

## Step 3: Run with Docker Compose

```bash
docker-compose up --build
```

## Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Testing

Once running, try these queries:

1. "I want an adventurous trip with hiking and extreme sports"
   → Should recommend New Zealand

2. "I'm looking for luxury and high-end experiences"
   → Should recommend Dubai

3. "I want to relax and enjoy the beach"
   → Should recommend Bali

4. "I'm interested in culture and history"
   → Should recommend Marrakech or Istanbul

## Architecture Overview

### Backend Flow

```
User Query
    ↓
[FastAPI Route /plan-trip]
    ↓
[Dependency Injection: Agent + LLM]
    ↓
[LangGraph Agent]
    ├→ Classifier Tool (identify travel style)
    ├→ RAG Tool (get destination)
    ├→ Weather Tool (fetch weather)
    └→ LLM Service (synthesize response)
    ↓
[Pydantic Response Schema]
    ↓
[Frontend Display]
```

### Key Components

**Agent Service**: Orchestrates the workflow using LangGraph
**LLM Service**: Wraps Google Gemini for response synthesis
**Tools**: Classifier, RAG, Weather (all with graceful error handling)
**Schemas**: Type-safe request/response validation

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| GOOGLE_API_KEY | Yes | Your Google Gemini API key |
| LANGCHAIN_API_KEY | Yes | For LangSmith tracing |
| LANGCHAIN_TRACING_V2 | No | Enable tracing (default: true) |
| LANGSMITH_PROJECT | No | Project name for tracing |

## Troubleshooting

### Backend won't start
- Check API keys are set correctly
- Verify Google Gemini API is enabled
- Check Docker logs: `docker-compose logs backend`

### Frontend can't reach backend
- Ensure backend is running on 8000
- Check CORS is enabled (it is by default)
- Verify network connectivity between containers

### LangSmith tracing not showing
- Verify LANGCHAIN_API_KEY is set
- Check LANGCHAIN_TRACING_V2=true in env
- Traces appear in your LangSmith dashboard

## Development Tips

### Local Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Local Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
cd backend
pytest tests.py -v
```

## Next Steps / Future Enhancements

- Add real database models
- Implement user authentication
- Add itinerary generation
- Integrate real booking APIs
- Add multi-language support
- Implement vector embeddings for RAG
- Add real ML model for classification
- Scale with message queue (Redis/Celery)

---

**Need help?** Check the API documentation at http://localhost:8000/docs
