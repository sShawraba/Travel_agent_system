# Quick Start Guide - PostgreSQL & Auth Integration

## TL;DR - 5 Minute Setup

### Prerequisites
- PostgreSQL installed and running
- Python 3.11+
- Node.js 16+

### Step 1: Set Up PostgreSQL

```bash
# Create database (macOS/Linux)
createdb travel_ai
psql travel_ai -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql travel_ai -c "CREATE EXTENSION IF NOT EXISTS \"vector\";"

# OR use Docker
docker run --name travel-db -e POSTGRES_DB=travel_ai -e POSTGRES_PASSWORD=travel_password -p 5432:5432 -d pgvector/pgvector:pg15-latest
```

### Step 2: Backend Setup

```bash
cd travel-ai-agent

# Copy environment file
cp .env.example .env

# Edit .env and set DATABASE_URL
# nano .env  # or edit in your editor

# Install dependencies
source .venv/bin/activate
pip install -e .

# Run migrations
cd backend
alembic upgrade head
cd ..

# Start backend
cd backend && python -m uvicorn app.main:app --reload
```

Backend will be available at: `http://localhost:8000`

### Step 3: Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### Step 4: Try It Out

1. Go to `http://localhost:5173`
2. Sign up with an email and password
3. Login
4. Type: "I want to relax on a beach"
5. Get a trip recommendation!

---

## What Changed?

**Before:**
- No authentication
- No database persistence
- No user history
- No tool logging

**After:**
- ✅ User registration & login (JWT)
- ✅ Trip history saved per user
- ✅ Tool invocations logged
- ✅ 15 real destinations (not mock data)
- ✅ Embeddings ready for semantic search

---

## File Structure

```
backend/app/
├── core/
│   ├── auth.py              ← JWT & password hashing
│   ├── database.py          ← DB connection
│   ├── dependencies.py      ← Auth middleware
│   └── models.py            ← SQLAlchemy models
├── routes/
│   ├── auth.py              ← /api/auth/signup, /login
│   └── travel.py            ← /api/plan-trip (requires auth)
└── main.py                  ← FastAPI app
```

---

## API Examples

### Sign Up
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Plan Trip (requires token)
```bash
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to relax at a beach"}'
```

### Get Your History (requires token)
```bash
curl -X GET http://localhost:8000/api/agent-runs \
  -H "Authorization: Bearer <your_token>"
```

---

## Database Schema (Simple View)

```
Users
├── id, username, email, password_hash, created_at

Agent Runs (belongs to User)
├── id, user_id, query, travel_style, destination
├── explanation, weather_summary, created_at

Tool Call Logs (belongs to Agent Run)
├── id, agent_run_id, tool_name, tool_input, tool_output

Destinations
├── id, name, category, description, content, source

Embeddings (for future semantic search)
├── id, destination_id, embedding_vector
```

---

## Troubleshooting

**Q: "connection to server at localhost:5432 failed"**
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Or start Docker container
docker start travel-db
```

**Q: "Access denied for user 'travel_user'"**
```bash
# Fix DATABASE_URL in .env
DATABASE_URL=postgresql://postgres:@localhost/travel_ai  # No password
```

**Q: "Extension vector not found"**
```bash
# Use pgvector Docker image instead
docker run --name travel-db -e POSTGRES_DB=travel_ai -p 5432:5432 -d pgvector/pgvector:pg15-latest
```

**Q: "Alembic revision not found"**
```bash
cd backend
alembic downgrade base
alembic upgrade head
```

---

## Key Features

| Feature | Before | After |
|---------|--------|-------|
| Users | ❌ | ✅ JWT auth |
| Database | ❌ | ✅ PostgreSQL |
| History | ❌ | ✅ Per user |
| Logging | ❌ | ✅ Full tool logs |
| Destinations | 8 mock | 15 real |
| Embeddings | ❌ | ✅ pgvector ready |

---

## Environment Variables (.env)

```env
# Required
DATABASE_URL=postgresql://postgres@localhost/travel_ai
GOOGLE_API_KEY=your_google_api_key
LANGCHAIN_API_KEY=your_langsmith_key

# Optional (has defaults)
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Next Steps

1. **Add Real Embeddings**
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   embeddings = model.encode(destination_content)
   ```

2. **Use Semantic Search**
   ```sql
   SELECT * FROM destinations 
   ORDER BY embedding <-> query_embedding 
   LIMIT 5;
   ```

3. **Deploy to Production**
   - Set `SECRET_KEY` to a secure random value
   - Use `HTTPS` for all connections
   - Add rate limiting
   - Use environment secrets (not .env)

---

## Full Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup with all options
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details
- [API Docs](http://localhost:8000/docs) - Interactive API documentation

---

## Support

```bash
# Check database is working
psql -U postgres -d travel_ai -c "\dt"

# Check migrations applied
cd backend && alembic current

# View API docs
# Go to http://localhost:8000/docs
```

Happy travels! 🌍✈️
