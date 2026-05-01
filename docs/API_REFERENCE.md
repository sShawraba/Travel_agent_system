# Smart Travel Planner - API Reference

## Quick Start

### Running the App

```bash
# Option 1: Docker (recommended)
docker-compose up --build

# Option 2: Backend only (requires frontend separate)
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Option 3: Frontend only (requires backend running)
cd frontend
npm install
npm run dev
```

## API Endpoints

### Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "ok",
  "service": "travel-ai-agent"
}
```

### Root
```
GET /
```
**Response:**
```json
{
  "message": "Smart Travel Planner API",
  "docs": "/docs",
  "health": "/health"
}
```

### Plan Trip (Main Endpoint)
```
POST /api/plan-trip
```

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
  "explanation": "Bali is perfect for relaxation with its stunning beaches, spa facilities, and peaceful spiritual temples. The tropical climate provides the ideal setting for unwinding and reconnecting with nature.",
  "weather_summary": "28°C, Sunny"
}
```

## Example Requests

### Using curl

```bash
# Relaxation
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to relax and enjoy the beach"}'

# Adventure
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I love hiking and extreme sports"}'

# Luxury
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I want luxury and high-end experiences"}'

# Culture
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I am interested in history and culture"}'

# Budget
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I am looking for budget-friendly options"}'
```

### Using Python

```python
import requests
import json

url = "http://localhost:8000/api/plan-trip"
payload = {"query": "I want to relax at a beach"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), indent=2))
```

### Using JavaScript/Fetch

```javascript
const response = await fetch('http://localhost:8000/api/plan-trip', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'I want to relax at a beach'
  })
});

const data = await response.json();
console.log(data);
```

## Travel Styles

The classifier recognizes these travel styles:

| Style | Keywords |
|-------|----------|
| **adventure** | hiking, extreme, thrilling, adventure |
| **luxury** | luxury, premium, expensive, 5-star |
| **cultural** | culture, history, museum, art |
| **relaxation** | relax, beach, spa, peace |
| **budget** | budget, cheap, backpack, economy |
| **balanced** | (default for unclassified) |

## Recommended Destinations

The RAG tool returns destinations based on travel style:

| Travel Style | Destination | Description |
|---|---|---|
| adventure | New Zealand | Hiking, extreme sports, dramatic landscapes |
| luxury | Dubai, UAE | Luxury resorts, shopping, modern architecture |
| cultural | Marrakech, Morocco | Souks, palaces, history |
| relaxation | Bali, Indonesia | Beaches, spas, temples |
| budget | Barcelona, Spain | Affordable, vibrant, cultural |
| balanced | Tokyo, Japan | Blend of everything |

## Response Schema

All responses follow this structure:

```python
{
    "recommended_destination": str,    # Full destination name
    "travel_style": str,               # Identified travel style
    "explanation": str,                # AI-generated explanation
    "weather_summary": str             # Temperature and conditions
}
```

## Error Handling

The API uses graceful fallbacks:

- If classification fails → defaults to "balanced"
- If RAG fails → defaults to "Tokyo, Japan"
- If weather fails → defaults to "22°C, Clear"

All errors are logged but won't crash the request.

## Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **README**: [README.md](README.md)
- **Setup Guide**: [SETUP.md](SETUP.md)
- **Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## Performance Notes

- **Latency**: ~2-3 seconds per request (includes Gemini API call)
- **Throughput**: Concurrent requests are handled asynchronously
- **Rate Limiting**: None configured (add for production)

## Debugging

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### View API Documentation
```
http://localhost:8000/docs
```

### Check Docker Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

### Run Backend Tests
```bash
cd backend
python -m pytest tests.py -v
```

### Run Quick Backend Test
```bash
python test_backend.py
```

## Environment Variables

Required in `backend/.env`:

```
GOOGLE_API_KEY=sk-...
LANGCHAIN_API_KEY=ls_...
LANGCHAIN_TRACING_V2=true
LANGSMITH_PROJECT=travel-ai-agent
```

## Troubleshooting

### Backend won't start
```bash
# Check Python dependencies
pip install -e ".[dev]"

# Check Google API key is set
echo $GOOGLE_API_KEY

# Run in debug mode
uvicorn app.main:app --reload --log-level debug
```

### Frontend can't reach backend
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check frontend is using correct API URL
# Should be: http://localhost:8000
```

### Tests fail
```bash
# Make sure all dependencies are installed
pip install -e ".[dev]"

# Run with verbose output
pytest tests.py -v -s
```

## Next Steps

1. ✅ Understand the code structure (see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md))
2. ✅ Test the API endpoints using curl or the frontend
3. ✅ Check LangSmith dashboard for agent traces
4. ✅ Modify the RAG tool to add more destinations
5. ✅ Train a real ML classifier with your own data
6. ✅ Deploy to production with proper configuration

## Support

For issues or questions, check:
- 📚 [README.md](README.md) - Overview
- 🔧 [SETUP.md](SETUP.md) - Setup & troubleshooting
- 📋 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Architecture details
- 📖 Code comments in `backend/app/`

---

**Happy planning! ✈️**
