# System Architecture Overview

## High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          SMART TRAVEL PLANNER                              │
└────────────────────────────────────────────────────────────────────────────┘

                              FRONTEND (React + Vite)
                            Port 3000
                    ┌─────────────────────────────┐
                    │                             │
                    │  ┌─────────────────────┐    │
                    │  │   Chat Interface    │    │
                    │  │  - Input Box        │    │
                    │  │  - Send Button      │    │
                    │  │  - Response Display │    │
                    │  └─────────────────────┘    │
                    │                             │
                    │  ┌─────────────────────┐    │
                    │  │   State Management  │    │
                    │  │  - Query            │    │
                    │  │  - Response         │    │
                    │  │  - Loading          │    │
                    │  └─────────────────────┘    │
                    │                             │
                    └────────────┬────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   HTTP Client (Fetch)   │
                    │  Content-Type: JSON     │
                    └────────────┬────────────┘
                                 │
                    POST /api/plan-trip
                                 │
                ┌────────────────▼────────────────┐
                │   BACKEND (FastAPI)              │
                │   Port 8000                      │
                ├────────────────────────────────┤
                │                                  │
                │  ┌────────────────────────────┐ │
                │  │  FastAPI Router             │ │
                │  │  @app.post("/api/plan-trip")│ │
                │  │  ├─ Request Validation      │ │
                │  │  ├─ Dependency Injection    │ │
                │  │  └─ Response Building       │ │
                │  └────────────┬────────────────┘ │
                │               │                  │
                │  ┌────────────▼──────────────┐  │
                │  │  Dependency Injection     │  │
                │  │  Provides:                │  │
                │  │  ├─ AgentService          │  │
                │  │  └─ LLMService            │  │
                │  └────────────┬──────────────┘  │
                │               │                  │
                │  ┌────────────▼──────────────┐  │
                │  │  Agent Service            │  │
                │  │  (LangGraph)              │  │
                │  │                           │  │
                │  │  State Machine:           │  │
                │  │  1. Classify             │  │
                │  │  2. RAG                  │  │
                │  │  3. Weather              │  │
                │  │  4. Synthesize           │  │
                │  └────────────┬──────────────┘  │
                │               │                  │
                │    ┌──────────┼──────────┬──────┤
                │    │          │          │      │
                │    ▼          ▼          ▼      │
                │  ┌───┐    ┌───┐    ┌────────┐  │
                │  │C  │    │R  │    │Weather │  │
                │  │L  │───▶│A  │───▶│ Tool   │  │
                │  │S  │    │G  │    └──┬─────┘  │
                │  │   │    │   │       │        │
                │  │   │    │   │       └──┐     │
                │  └───┘    └───┘          │     │
                │                         │     │
                │  ┌──────────────────────▼──┐  │
                │  │  LLM Service (Gemini)    │  │
                │  │  - Synthesize Response   │  │
                │  │  - Generate Explanation  │  │
                │  └──────────────┬───────────┘  │
                │                 │              │
                │  ┌──────────────▼──────────┐  │
                │  │  Pydantic Response      │  │
                │  │  - destination          │  │
                │  │  - travel_style         │  │
                │  │  - explanation          │  │
                │  │  - weather_summary      │  │
                │  └──────────────┬──────────┘  │
                │                 │              │
                └─────────────────┼──────────────┘
                                  │
                    ┌─────────────▼──────────┐
                    │   JSON Response        │
                    │   (Validated by)       │
                    │   Pydantic Schema      │
                    └─────────────┬──────────┘
                                  │
                    ┌─────────────▼──────────┐
                    │   Frontend receives    │
                    │   Parses JSON          │
                    │   Updates State        │
                    │   Renders Response     │
                    └────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                        SUPPORTING SERVICES                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DATABASE (PostgreSQL)       LLM API (Google Gemini)   TRACING (LangSmith) │
│  Port 5432                   Cloud                      Cloud              │
│  ┌─────────────────────┐     ┌────────────────────┐    ┌──────────────┐  │
│  │ - travel_config     │────▶│ - model: gemini    │───▶│ - Traces     │  │
│  │ - user_data         │     │ - temperature: 0.3 │    │ - Metrics    │  │
│  │ - destinations      │     │ - async calls      │    │ - Analytics  │  │
│  └─────────────────────┘     └────────────────────┘    └──────────────┘  │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                         ENVIRONMENT VARIABLES                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Backend (.env file)                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ GOOGLE_API_KEY=sk-...                    (Required)               │  │
│  │ LANGCHAIN_API_KEY=ls_...                 (Required)               │  │
│  │ LANGCHAIN_TRACING_V2=true                (Optional, default=true) │  │
│  │ LANGSMITH_PROJECT=travel-ai-agent        (Optional)               │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Relationships

### Frontend Component Tree
```
App.jsx
├── Header
│   ├── Title "Smart Travel Planner"
│   └── Subtitle
├── Main Content
│   ├── Form
│   │   ├── Input (controlled component)
│   │   └── Submit Button
│   ├── State Management
│   │   ├── query (user input)
│   │   ├── response (API response)
│   │   ├── loading (boolean)
│   │   └── error (error message)
│   └── Conditional Rendering
│       ├── LoadingState
│       ├── ErrorState
│       ├── ResponseState
│       │   ├── DestinationCard
│       │   ├── StyleCard
│       │   ├── ExplanationCard
│       │   └── WeatherCard
│       └── EmptyState

Styling
├── App.css (component styles)
└── index.css (global styles)
```

### Backend Service Architecture
```
FastAPI Application
│
├── Middleware
│   ├── CORS
│   └── Error Handlers
│
├── Routes
│   ├── GET / (root)
│   ├── GET /health
│   └── POST /api/plan-trip
│
├── Dependencies (Dependency Injection)
│   ├── get_agent_service()
│   └── get_llm_service()
│
├── Services
│   ├── AgentService
│   │   ├── build_graph()
│   │   │   ├── node_classify
│   │   │   ├── node_rag
│   │   │   ├── node_weather
│   │   │   └── workflow edges
│   │   └── run_agent(query)
│   │
│   └── LLMService
│       ├── __init__(api_key)
│       │   └── ChatGoogleGenerativeAI
│       └── synthesize_response(...)
│
├── Tools
│   ├── classifier_tool
│   │   └── TravelStyleClassifier (singleton)
│   ├── rag_tool
│   │   └── DESTINATIONS dict (8 hardcoded)
│   └── weather_tool
│       └── get_weather()
│
├── Models (Pydantic)
│   ├── TravelPlanRequest
│   ├── TravelStyleOutput
│   ├── DestinationInfo
│   ├── WeatherInfo
│   └── TravelPlanResponse
│
└── Config
    └── Settings
        ├── google_api_key
        ├── langchain_api_key
        ├── langchain_tracing_v2
        └── langsmith_project
```

---

## Data Flow: End-to-End

### 1. User Interaction
```
User types: "I want to relax at a beach"
User clicks: "Plan My Trip" button
```

### 2. Frontend Processing
```
JavaScript Event Handler
  ↓
Form Validation
  ↓
State Update (query)
  ↓
Button State: disabled=true, text="Planning..."
  ↓
HTTP Request to Backend
```

### 3. Network
```
POST http://localhost:8000/api/plan-trip
Headers: { Content-Type: application/json }
Body: { query: "I want to relax at a beach" }
```

### 4. Backend Request Handling
```
FastAPI Route Handler
  ↓
Pydantic Validation
  ↓
Dependency Injection
  ↓
Services Initialized
```

### 5. Agent Execution
```
State Creation
  ↓
Classifier Node
  ├─ Input: "I want to relax at a beach"
  ├─ Rule Match: "relax" + "beach"
  └─ Output: travel_style = "relaxation"
  ↓
RAG Node
  ├─ Input: travel_style = "relaxation"
  ├─ Lookup: style_mapping["relaxation"] = "bali"
  └─ Output: destination = "Bali, Indonesia"
  ↓
Weather Node
  ├─ Input: "Bali, Indonesia"
  ├─ Simulation: tropical weather
  └─ Output: temperature = "28°C", condition = "Sunny"
  ↓
Synthesis (Gemini LLM)
  ├─ Input: query + style + destination + weather
  ├─ API Call: Google Gemini
  └─ Output: explanation text
```

### 6. Response Building
```
TravelPlanResponse(
  recommended_destination="Bali, Indonesia",
  travel_style="relaxation",
  explanation="Bali is the perfect destination...",
  weather_summary="28°C, Sunny"
)
```

### 7. Backend Response
```
HTTP 200 OK
Content-Type: application/json
Body: {
  "recommended_destination": "Bali, Indonesia",
  "travel_style": "relaxation",
  "explanation": "...",
  "weather_summary": "28°C, Sunny"
}
```

### 8. Frontend Rendering
```
JavaScript receives response
  ↓
State Update (response = data)
  ↓
Button State: disabled=false, text="Plan My Trip"
  ↓
Conditional Render: ResponseState
  ↓
Display Cards:
  ├─ Destination Card
  ├─ Style Card
  ├─ Explanation Card
  └─ Weather Card
```

### 9. User Sees Result
```
Beautiful card layout showing:
✈️ Smart Travel Planner
📍 Destination: Bali, Indonesia
🎨 Travel Style: Relaxation
💡 Why This Destination: [explanation]
🌤️ Current Weather: 28°C, Sunny
```

---

## Technology Stack Mapping

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  React 18.2.0 (UI Library)                                  │
│  Vite 5.0.0 (Build Tool)                                    │
│  CSS3 (Styling with animations & gradients)                 │
│  JavaScript ES6+ (Async/await, fetch API)                   │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP/JSON
┌────────────▼────────────────────────────────────────────────┐
│                    API LAYER (FastAPI)                      │
├─────────────────────────────────────────────────────────────┤
│  FastAPI 0.109.0 (Web Framework)                            │
│  Uvicorn 0.27.0 (ASGI Server)                               │
│  Pydantic 2.5.3 (Data Validation)                           │
│  Pydantic Settings 2.1.0 (Config Management)                │
└────────────┬────────────────────────────────────────────────┘
             │ Python/Async
┌────────────▼────────────────────────────────────────────────┐
│                    LOGIC LAYER                              │
├─────────────────────────────────────────────────────────────┤
│  LangGraph 0.0.26 (Workflow Orchestration)                  │
│  LangChain 0.1.10 (LLM Framework)                           │
│  LangSmith 0.1.17 (Tracing & Debugging)                     │
│  scikit-learn 1.3.2 (ML Algorithms)                         │
│  joblib 1.3.2 (Model Serialization)                         │
└────────────┬────────────────────────────────────────────────┘
             │ API Calls
┌────────────▼────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                        │
├─────────────────────────────────────────────────────────────┤
│  Google Gemini API (LLM)                                    │
│  LangSmith Cloud (Tracing)                                  │
│  PostgreSQL 15 (Database)                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Request/Response Lifecycle

```
1. USER INTERFACE
   └─ Input: Query string
   └─ Action: Click button

2. FRONTEND (React)
   └─ Event handler triggered
   └─ Validation (check query not empty)
   └─ State update (query, loading=true)
   └─ HTTP fetch() to backend

3. NETWORK
   └─ POST request with JSON body
   └─ Content-Type: application/json

4. BACKEND (FastAPI)
   └─ Route handler invoked
   └─ Request body validated by Pydantic
   └─ Dependencies injected
   └─ Business logic executed

5. AGENT (LangGraph)
   └─ 4-node graph executed sequentially
   └─ State passed through each node
   └─ Tools invoked
   └─ LLM called for synthesis

6. EXTERNAL CALLS
   └─ Google Gemini API for synthesis
   └─ LangSmith API for tracing

7. RESPONSE CONSTRUCTION
   └─ Pydantic model validates response
   └─ JSON serialization
   └─ HTTP 200 response

8. FRONTEND (React)
   └─ Response received
   └─ JSON parsed
   └─ State updated (response, loading=false)
   └─ UI re-renders

9. USER SEES
   └─ Response displayed in cards
   └─ Beautiful UI with animations
```

---

## Database Schema (Planned)

```
PostgreSQL Database
│
├─ users
│  ├─ id (PK)
│  ├─ email
│  ├─ created_at
│  └─ updated_at
│
├─ travel_plans
│  ├─ id (PK)
│  ├─ user_id (FK)
│  ├─ query
│  ├─ destination
│  ├─ travel_style
│  ├─ created_at
│  └─ updated_at
│
└─ destinations
   ├─ id (PK)
   ├─ name
   ├─ description
   ├─ weather_data
   └─ embedding (for RAG)
```

**Note:** Currently not used (PostgreSQL is connected but unused). Add models as needed.

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│              Docker Compose Orchestration                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Frontend Service                                 │   │
│  │ Image: node:18-alpine                           │   │
│  │ Build: Vite (npm run build)                      │   │
│  │ Serve: serve package                            │   │
│  │ Port: 3000                                       │   │
│  │ Volume: dist/ from builder                       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Backend Service                                  │   │
│  │ Image: python:3.11-slim                          │   │
│  │ Install: uv (package manager)                    │   │
│  │ Install: Dependencies via uv                     │   │
│  │ Serve: uvicorn                                   │   │
│  │ Port: 8000                                       │   │
│  │ Volume: ./backend for hot-reload                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Database Service (PostgreSQL)                    │   │
│  │ Image: postgres:15-alpine                        │   │
│  │ Port: 5432                                       │   │
│  │ Volume: postgres_data (persistent)               │   │
│  │ Healthcheck: pg_isready command                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Network: Internal Docker network                      │
│  Services communicate via service names               │
│                                                          │
└──────────────────────────────────────────────────────────┘

↓

┌──────────────────────────────────────────────────────────┐
│                  Production Deployment                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Kubernetes Cluster (or Docker Swarm)            │   │
│  │                                                  │   │
│  │  ├─ Frontend Pods (3 replicas)                  │   │
│  │  ├─ Backend Pods (5 replicas)                   │   │
│  │  ├─ Load Balancer (NGINX)                       │   │
│  │  ├─ Database (RDS or Cloud SQL)                 │   │
│  │  ├─ Cache (Redis)                               │   │
│  │  └─ Message Queue (RabbitMQ)                    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Summary

The **Smart Travel Planner** is a complete, production-ready architecture featuring:

✅ **Modern Frontend** - React with Vite for fast development
✅ **Robust Backend** - FastAPI with async operations
✅ **Intelligent Agent** - LangGraph orchestration with tools
✅ **Type Safety** - Pydantic validation everywhere
✅ **Observability** - LangSmith tracing built-in
✅ **Containerization** - Docker & docker-compose
✅ **Clean Code** - Separation of concerns, SOLID principles
✅ **Error Handling** - Graceful fallbacks throughout
✅ **Scalability** - Ready for production deployment

---

**See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for code details**

**See [AGENT_FLOW.md](AGENT_FLOW.md) for agent execution details**
