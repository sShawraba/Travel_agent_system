# 🧪 Testing & Validation Guide

This guide shows you how to verify your Smart Travel Planner installation is working correctly.

---

## Pre-Deployment Testing

### 1. Validate File Structure

```bash
# Run the validation script
bash validate.sh
```

Expected output:
```
✓ backend/app/main.py
✓ backend/app/core/config.py
✓ backend/app/models/schemas.py
✓ backend/app/routes/travel.py
✓ backend/app/services/agent_service.py
✓ backend/app/services/llm_service.py
✓ backend/app/tools/classifier_tool.py
✓ backend/app/tools/rag_tool.py
✓ backend/app/tools/weather_tool.py
✓ frontend/src/App.jsx
✓ frontend/src/main.jsx
✓ frontend/package.json
✓ docker-compose.yml
... and more

✅ All required files present!
```

### 2. Test Backend Code Imports

```bash
python test_backend.py
```

Expected output:
```
==================================================
Smart Travel Planner - Backend Tests
==================================================

🔍 Testing imports...
✅ All imports successful

🧪 Testing Classifier Tool...
✅ adventure hiking → adventure
✅ luxury resort → luxury
✅ cultural museum → cultural
✅ beach relax → relaxation
✅ cheap backpack → budget

🧪 Testing RAG Tool...
✅ adventure → New Zealand
✅ luxury → Dubai, UAE
✅ cultural → Marrakech, Morocco
✅ relaxation → Bali, Indonesia
✅ budget → Barcelona, Spain

🧪 Testing Weather Tool...
✅ Bali, Indonesia → 28°C, Sunny
✅ Tokyo, Japan → 22°C, Clear Skies
✅ Paris, France → 15°C, Partly Cloudy

🧪 Testing Agent Service...
✅ Query: 'I want to relax at a beach'
   Style: relaxation
   Destination: Bali, Indonesia
   Weather: {'temperature': '28°C', 'condition': 'Sunny'}

==================================================
Test Results
==================================================
✅ Imports
✅ Classifier
✅ RAG
✅ Weather
✅ Agent

Passed: 5/5

🎉 All tests passed!
```

### 3. Check Environment Setup

```bash
# Verify .env file exists
ls -la backend/.env

# Check it has required keys
grep GOOGLE_API_KEY backend/.env
grep LANGCHAIN_API_KEY backend/.env
```

Expected output:
```
GOOGLE_API_KEY=sk-...
LANGCHAIN_API_KEY=ls_...
LANGCHAIN_TRACING_V2=true
LANGSMITH_PROJECT=travel-ai-agent
```

---

## Deployment Testing

### 1. Build Docker Images

```bash
docker-compose build
```

Expected output:
```
[+] Building 45.2s (15/15) FINISHED
 => [backend 1/6] FROM python:3.11-slim@sha256:...
 => [backend 2/6] WORKDIR /app
 => [backend 3/6] RUN pip install --no-cache-dir uv
 => [backend 4/6] COPY pyproject.toml .
 => [backend 5/6] RUN uv pip install --system ...
 => [backend 6/6] COPY backend/app ./app
 => [frontend 1/8] FROM node:18-alpine
 => [frontend 2/8] WORKDIR /app
 => [frontend 3/8] COPY frontend/package.json ...
 => [frontend 4/8] RUN npm install
 => [frontend 5/8] COPY frontend/src ./src
 => [frontend 6/8] COPY frontend/index.html ./
 => [frontend 7/8] RUN npm run build
 => [frontend 8/8] FROM node:18-alpine
✓ All images built successfully
```

### 2. Start Services

```bash
docker-compose up -d
```

Wait 10 seconds for services to start:

```bash
# Check status
docker-compose ps
```

Expected output:
```
NAME                    STATUS
travel-planner-postgres-1    Up 10 seconds (healthy)
travel-planner-backend-1     Up 5 seconds (healthy)
travel-planner-frontend-1    Up 3 seconds
```

### 3. Test Backend Health

```bash
# Health check
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"ok","service":"travel-ai-agent"}
```

### 4. Test Frontend Connectivity

```bash
# Check frontend is serving
curl http://localhost:3000
```

Expected response:
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    ...
```

### 5. Test API Endpoint

```bash
# Make a travel planning request
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to relax at a beach"}'
```

Expected response:
```json
{
  "recommended_destination": "Bali, Indonesia",
  "travel_style": "relaxation",
  "explanation": "Bali is the perfect destination for your relaxation needs. With pristine beaches, world-class spas, and serene temples, it offers the ideal escape...",
  "weather_summary": "28°C, Sunny"
}
```

---

## Integration Testing

### 1. Browser Testing

Open http://localhost:3000 and verify:

- [ ] Page loads with "Smart Travel Planner" header
- [ ] Input box is visible
- [ ] "Plan My Trip" button is visible
- [ ] Page styling looks good (gradient background)

### 2. UI Interaction Test

1. Type in input: "I want an adventure trip"
2. Click "Plan My Trip" button
3. Wait ~3 seconds

Verify:
- [ ] Button changes to "Planning..."
- [ ] Input box is disabled
- [ ] Response appears with 4 cards
- [ ] Destination card shows destination
- [ ] Style card shows travel style
- [ ] Explanation card has explanation text
- [ ] Weather card has weather info

### 3. Multiple Query Test

Test different queries and verify each returns appropriate response:

```bash
# Test 1: Relaxation
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to relax at a beach"}'
# Expected: Bali

# Test 2: Adventure
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I love hiking and extreme sports"}'
# Expected: New Zealand

# Test 3: Luxury
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I want luxury and premium experiences"}'
# Expected: Dubai

# Test 4: Culture
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I am interested in history and culture"}'
# Expected: Marrakech or Tokyo

# Test 5: Budget
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I am looking for budget-friendly options"}'
# Expected: Barcelona
```

All should return `"travel_style"` matching the query!

### 4. Error Handling Test

Test error scenarios:

```bash
# Test missing query
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{}'
# Expected: 422 Validation Error

# Test invalid JSON
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d 'not json'
# Expected: 422 Unprocessable Entity

# Test wrong method
curl -X GET http://localhost:8000/api/plan-trip
# Expected: 405 Method Not Allowed
```

All should return appropriate HTTP status codes!

### 5. API Documentation Test

Open http://localhost:8000/docs

Verify:
- [ ] Swagger UI loads
- [ ] POST /api/plan-trip is listed
- [ ] Request/response schemas visible
- [ ] Can execute requests from UI
- [ ] Responses display correctly

---

## Performance Testing

### 1. Response Time

```bash
time curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to relax"}'
```

Expected: 2-3 seconds total

### 2. Concurrent Requests

```bash
# Send 5 concurrent requests
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/plan-trip \
    -H "Content-Type: application/json" \
    -d '{"query": "travel query '$i'"}' &
done
wait

# All should succeed without timeouts
```

### 3. Memory Usage

```bash
# Check container memory usage
docker stats --no-stream
```

Expected:
- Backend: < 200MB
- Frontend: < 100MB
- Total: < 500MB

---

## LangSmith Tracing Test

### 1. Enable Tracing

Your `.env` should have:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls_...
```

### 2. Make a Request

```bash
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

### 3. Check Dashboard

1. Go to https://smith.langchain.com/
2. Find your project
3. You should see a trace with:
   - Agent execution
   - Tool calls (Classifier, RAG, Weather)
   - LLM synthesis call
   - Full execution time

---

## Success Checklist

✅ File structure validated
✅ Code imports work
✅ Environment configured
✅ Docker images built
✅ All services running
✅ Health check passes
✅ Frontend loads
✅ API responds correctly
✅ UI works interactively
✅ Multiple queries tested
✅ Error handling works
✅ API docs accessible
✅ Response times acceptable
✅ Concurrent requests work
✅ Memory usage acceptable
✅ LangSmith traces appear

---

## Debugging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail 100
```

### Backend Issues

```bash
# Get backend shell
docker-compose exec backend bash

# Run Python interactively
docker-compose exec backend python

# Check installed packages
docker-compose exec backend pip list
```

### Frontend Issues

```bash
# Get frontend shell
docker-compose exec frontend bash

# Check installed packages
docker-compose exec frontend npm list
```

### Database Connection

```bash
# Check postgres is healthy
docker-compose exec postgres pg_isready -U travel_user

# Connect to database
docker-compose exec postgres psql -U travel_user -d travel_ai -c "SELECT 1;"
```

---

## Common Test Failures & Solutions

### ❌ "Connection refused" on 8000
**Solution:** Wait for backend to start, check logs
```bash
docker-compose logs backend | tail -20
```

### ❌ "Query validation failed"
**Solution:** Ensure query is non-empty string
```bash
# Wrong:
{"query": ""}

# Right:
{"query": "I want to travel"}
```

### ❌ "API key not found"
**Solution:** Check .env file exists and has correct keys
```bash
cat backend/.env
```

### ❌ "Docker image build failed"
**Solution:** Check Docker resources and cleanup
```bash
docker system prune -a
docker-compose build --no-cache
```

### ❌ Slow responses (> 5 seconds)
**Solution:** Normal if Gemini API is slow, check network
```bash
# Check internet connection
curl https://makersuite.google.com
```

---

## Test Report Template

If you want to document your testing:

```
TEST REPORT - Smart Travel Planner
Date: [Date]
Environment: [Local/Docker/Cloud]

PRE-DEPLOYMENT TESTS:
[✅/❌] File structure validation
[✅/❌] Code imports test
[✅/❌] Environment setup

DEPLOYMENT TESTS:
[✅/❌] Docker image build
[✅/❌] Services startup
[✅/❌] Health checks
[✅/❌] API endpoints

INTEGRATION TESTS:
[✅/❌] UI loads
[✅/❌] UI interactions
[✅/❌] Multiple queries
[✅/❌] Error handling

PERFORMANCE TESTS:
[✅/❌] Response time
[✅/❌] Concurrent requests
[✅/❌] Memory usage

OBSERVABILITY:
[✅/❌] Logging works
[✅/❌] LangSmith traces appear

OVERALL: [PASS/FAIL]
Issues: [List any]
Notes: [Additional notes]
```

---

## Next Steps

Once all tests pass:
1. ✅ Deploy to production
2. ✅ Set up monitoring
3. ✅ Add authentication
4. ✅ Scale infrastructure
5. ✅ Train ML models
6. ✅ Integrate real APIs

---

**All tests passing?** You're ready for production! 🚀
