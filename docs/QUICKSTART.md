# ⚡ QUICKSTART - 5 Minutes to AI Travel Planning

**Just want to run it? This is your guide.**

---

## Step 1: Get API Keys (2 minutes)

### Google Gemini
1. Go to https://makersuite.google.com/
2. Click "Get API key"
3. Copy the key

### LangChain (LangSmith)
1. Go to https://smith.langchain.com/
2. Sign up
3. Get API key from settings
4. Copy the key

---

## Step 2: Setup Env File (1 minute)

```bash
cd /home/soup/travel-ai-agent
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```
GOOGLE_API_KEY=<your_gemini_key>
LANGCHAIN_API_KEY=<your_langchain_key>
LANGCHAIN_TRACING_V2=true
LANGSMITH_PROJECT=travel-ai-agent
```

---

## Step 3: Start Everything (1 minute)

```bash
docker-compose up --build
```

Wait for everything to start... You'll see:
```
✓ backend running on port 8000
✓ frontend running on port 3000
✓ postgres ready
```

---

## Step 4: Use It! (1 minute)

Open your browser:

**Frontend (Chat UI):** http://localhost:3000

Try queries like:
- "I want to relax at a beach"
- "I love adventure and hiking"
- "I want a luxury vacation"
- "I'm interested in culture and history"

---

## API Docs (Bonus)

See what endpoints exist:
http://localhost:8000/docs

Test endpoints directly in the browser!

---

## That's It! 🎉

You now have:
✅ AI-powered travel planning
✅ Gemini LLM responses
✅ Multi-step agent workflow
✅ Beautiful React UI
✅ Full API documentation

---

## Troubleshooting

### Port already in use?
```bash
# Change ports in docker-compose.yml
# Or kill the process on that port
lsof -i :3000  # Find process
kill -9 <PID>  # Kill it
```

### API keys not working?
```bash
# Check your .env file
cat backend/.env

# Verify keys are valid
# Google key should start with: sk-
# LangChain key should start with: ls_
```

### Docker not installed?
```bash
# Install from https://www.docker.com/products/docker-desktop
# Then run again
```

### Still have issues?
Check **SETUP.md** for full troubleshooting guide

---

## Next Steps

1. ✅ Test different queries
2. ✅ Check API docs at `/docs`
3. ✅ View LangSmith traces (in your dashboard)
4. ✅ Read [README.md](README.md) for overview
5. ✅ Read [AGENT_FLOW.md](AGENT_FLOW.md) to understand how it works

---

## Local Development (Without Docker)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

**Questions?** Check README.md or SETUP.md

**Ready?** Run: `docker-compose up --build`

✈️ Enjoy planning your trip!
