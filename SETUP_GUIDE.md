# PostgreSQL & Authentication Integration Setup Guide

This guide covers the new PostgreSQL database integration, authentication system, and real RAG content with embeddings.

## What's New

✅ **PostgreSQL Database** - Persistent storage for users, agent runs, tool logs, and embeddings  
✅ **User Authentication** - Registration, login with JWT tokens  
✅ **Agent Run Tracking** - Every trip plan is saved and tied to a user  
✅ **Tool Logging** - All tool invocations are recorded with inputs/outputs  
✅ **Real RAG Content** - 15 destinations with detailed content from Wikivoyage and travel blogs  
✅ **pgvector Integration** - Embeddings stored in Postgres (ready for similarity search)  
✅ **Alembic Migrations** - Database schema versioning and management  

## Prerequisites

- Python 3.11+
- PostgreSQL 13+ (with pgvector extension)
- Node.js 16+ (for frontend)
- Git

## Installation Steps

### 1. Set Up PostgreSQL Database

#### Option A: Local PostgreSQL (Linux/Mac)

```bash
# Install PostgreSQL if you don't have it
# Mac: brew install postgresql@15
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
# Mac: brew services start postgresql@15
# Ubuntu: sudo systemctl start postgresql

# Create database and user
psql -U postgres -c "CREATE USER travel_user WITH PASSWORD 'travel_password';"
psql -U postgres -c "CREATE DATABASE travel_ai OWNER travel_user;"
psql -U postgres -d travel_ai -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql -U postgres -d travel_ai -c "CREATE EXTENSION IF NOT EXISTS \"vector\";"
psql -U postgres -d travel_ai -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO travel_user;"
```

#### Option B: Docker PostgreSQL

```bash
# Create and run PostgreSQL container
docker run --name travel-ai-db \
  -e POSTGRES_USER=travel_user \
  -e POSTGRES_PASSWORD=travel_password \
  -e POSTGRES_DB=travel_ai \
  -p 5432:5432 \
  -d pgvector/pgvector:pg15-latest

# Enable extensions
docker exec travel-ai-db psql -U travel_user -d travel_ai -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
docker exec travel-ai-db psql -U travel_user -d travel_ai -c "CREATE EXTENSION IF NOT EXISTS \"vector\";"
```

### 2. Backend Setup

```bash
cd /home/soup/travel-ai-agent

# Copy environment template
cp .env.example .env

# Edit .env with your settings
# nano .env  # or use your favorite editor
```

Edit `.env` with:

```env
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://travel_user:travel_password@localhost:5432/travel_ai

# Google API (for Gemini LLM)
GOOGLE_API_KEY=your_google_api_key_here

# LangChain & LangSmith Configuration
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGSMITH_PROJECT=travel-ai-agent

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
VITE_API_URL=http://localhost:8000
```

### 3. Install Python Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (or upgrade)
pip install -e .

# Install the new database dependencies
pip install sqlalchemy==2.0.23 psycopg2-binary==2.9.9 alembic==1.13.1
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6 pgvector==0.2.4 email-validator
```

### 4. Run Alembic Migrations

```bash
cd backend

# Apply migrations to create tables
alembic upgrade head

# You should see:
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl with dialect postgresql
# INFO  [alembic.runtime.migration] Will assume transactional DDL is supported by the database
# INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial, Initial schema with users, agent runs, tool logs, and embeddings
```

### 5. Verify Database Setup

```bash
# Connect to database
psql -U travel_user -d travel_ai -h localhost

# List tables
\dt

# Should show:
# destinations
# destination_embeddings
# agent_runs
# tool_call_logs
# users

# Check pgvector extension
\dx

# Exit
\q
```

### 6. Backend Server

```bash
cd backend

# Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`  
API documentation: `http://localhost:8000/docs`

### 7. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication

```bash
# Sign up
POST /api/auth/signup
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}

# Login
POST /api/auth/login
{
  "email": "john@example.com",
  "password": "securepass123"
}

# Get current user
GET /api/auth/me
Authorization: Bearer <token>
```

### Travel Planning (Requires Authentication)

```bash
# Plan a trip
POST /api/plan-trip
Authorization: Bearer <token>
{
  "query": "I want to relax at a beach"
}

# Get all agent runs for user
GET /api/agent-runs
Authorization: Bearer <token>

# Get specific agent run
GET /api/agent-runs/{run_id}
Authorization: Bearer <token>
```

### Health Check

```bash
GET /health
GET /
```

## Database Schema

### Users Table
- `id` (UUID) - Primary key
- `username` (String) - Unique username
- `email` (String) - Unique email
- `password_hash` (String) - Bcrypt hashed password
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Agent Runs Table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to users
- `query` (Text) - User's query
- `travel_style` (String) - Detected style
- `recommended_destination` (String)
- `explanation` (Text)
- `weather_summary` (String)
- `errors` (JSON) - Array of errors
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Tool Call Logs Table
- `id` (UUID) - Primary key
- `agent_run_id` (UUID) - Foreign key to agent_runs
- `tool_name` (String) - Name of the tool invoked
- `tool_input` (JSON) - Input to the tool
- `tool_output` (JSON) - Output from the tool
- `error_message` (Text) - Error if any
- `timestamp` (DateTime)

### Destinations Table
- `id` (UUID) - Primary key
- `name` (String) - Destination name
- `category` (String) - Travel style category
- `description` (Text) - Short description
- `source` (String) - Source (Wikivoyage, blog, etc.)
- `source_url` (String) - URL to source
- `content` (Text) - Full content for RAG
- `created_at` (DateTime)

### Destination Embeddings Table
- `id` (UUID) - Primary key
- `destination_id` (UUID) - Foreign key to destinations
- `embedding` (VECTOR(1536)) - pgvector embedding
- `created_at` (DateTime)

## Features

### Authentication
- User registration with email validation
- Login with JWT tokens (expires in 30 minutes by default)
- Token verification on each request
- Password hashing with bcrypt

### Agent Run Tracking
- Every trip plan is recorded with user, query, and results
- Full history accessible to the user
- Tool invocations are logged for each run

### Real Destinations (15 locations)
1. **Tokyo, Japan** - Adventure & Cultural
2. **Bali, Indonesia** - Relaxation & Cultural
3. **Paris, France** - Cultural & Luxury
4. **New Zealand** - Adventure
5. **Dubai, UAE** - Luxury & Adventure
6. **Barcelona, Spain** - Cultural & Relaxation
7. **Marrakech, Morocco** - Cultural & Adventure
8. **Iceland** - Adventure
9. **Seychelles** - Relaxation & Adventure
10. **Thai Islands** - Relaxation & Adventure
11. **Swiss Alps** - Adventure & Luxury
12. **Egypt** - Cultural & Adventure
13. **Costa Rica** - Adventure
14. (+ more coming with embeddings)

### RAG System
- 15+ destinations with detailed content
- Categories: adventure, luxury, cultural, relaxation, budget
- Ready for embedding-based similarity search with pgvector
- Sources: Wikivoyage, travel blogs, tourism boards

## Environment Variables

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | ✅ | `postgresql://user:pass@localhost:5432/db` | PostgreSQL connection string |
| GOOGLE_API_KEY | ✅ | `AIzaSy...` | Google Gemini API key |
| LANGCHAIN_API_KEY | ✅ | `ls__...` | LangSmith API key |
| LANGCHAIN_TRACING_V2 | ❌ | `true` | Enable LangChain tracing |
| LANGSMITH_PROJECT | ❌ | `travel-ai-agent` | LangSmith project name |
| SECRET_KEY | ✅ | `your-secret-key` | JWT signing key |
| ALGORITHM | ❌ | `HS256` | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | ❌ | `30` | JWT token expiration |

## Troubleshooting

### PostgreSQL Connection Error
```
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed
```

**Solution:**
1. Verify PostgreSQL is running: `psql -U postgres`
2. Check DATABASE_URL in .env is correct
3. Verify database exists: `psql -U travel_user -d travel_ai -h localhost`

### pgvector Extension Not Available
```
ERROR: permission denied to create extension "vector"
```

**Solution:**
- For PostgreSQL < 15: Install pgvector manually or use Docker image with pgvector pre-installed
- Ensure you have superuser privileges or have pgvector pre-installed

### Migration Errors
```
alembic.util.exc.CommandError: Can't locate revision identified by '001_initial'
```

**Solution:**
```bash
# Check migration status
alembic current

# If needed, reset and reapply
alembic downgrade base
alembic upgrade head
```

### CORS Errors
If frontend can't reach backend, ensure CORS is properly configured in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### JWT Token Invalid
- Check SECRET_KEY is the same between requests
- Verify token hasn't expired (default 30 minutes)
- Clear localStorage and re-login if issues persist

## Security Notes

⚠️ **IMPORTANT FOR PRODUCTION:**

1. **Change SECRET_KEY** - Generate a secure random key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Use HTTPS** - Always use HTTPS in production

3. **Database Security** - Change default credentials, use strong passwords

4. **CORS Settings** - Don't use `allow_origins=["*"]` in production

5. **Password Requirements** - Implement password strength validation

6. **Rate Limiting** - Add rate limiting to auth endpoints

7. **Database Backups** - Regular backup strategy

## Next Steps

1. **Add Embeddings** - Generate embeddings for destinations using OpenAI or similar
2. **Similarity Search** - Implement pgvector-based semantic search
3. **User Profiles** - Add user preferences, favorite destinations
4. **Export Functionality** - Generate travel plans as PDF
5. **Social Features** - Share trip plans with friends
6. **Payment Integration** - Monetize with stripe
7. **Mobile App** - React Native mobile client
8. **Advanced Analytics** - Track user preferences and trends

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error logs in PostgreSQL
3. Check backend console output
4. Review browser DevTools (Network tab)

