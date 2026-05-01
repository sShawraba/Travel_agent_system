# Agent Flow - Step by Step

## Overview

The Smart Travel Planner uses a **LangGraph-based agent** to orchestrate a multi-step workflow. Here's exactly what happens when you submit a query.

---

## Flow Diagram

```
┌─────────────────────────────┐
│  User Query (Frontend)      │
│  "I want to relax"          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ POST /api/plan-trip         │
│ (FastAPI Route)             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Dependency Injection        │
│ Load:                       │
│ - AgentService             │
│ - LLMService               │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ LangGraph Agent Execution   │
└──────────────┬──────────────┘
               │
    ┌──────────┴──────────┬─────────────┬──────────────┐
    │                     │             │              │
    ▼                     ▼             ▼              ▼
┌─────────┐        ┌──────────┐  ┌──────────┐  ┌──────────────┐
│Classify │        │  RAG     │  │ Weather  │  │   Synthesis  │
│ Tool    │───────▶│  Tool    │─▶│  Tool    │─▶│   (Gemini)   │
└─────────┘        └──────────┘  └──────────┘  └──────────────┘
    │                  │             │              │
    │                  │             │              │
    └──────────────────┴─────────────┴──────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │ Pydantic Response       │
         │ - destination           │
         │ - travel_style          │
         │ - explanation           │
         │ - weather_summary       │
         └─────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │  Return to Frontend     │
         │  Render UI              │
         └─────────────────────────┘
```

---

## Detailed Step-by-Step

### Step 1: Request Arrives at Backend

```python
# User sends
POST /api/plan-trip
{
  "query": "I want to relax at a beach"
}

# Route handler receives
@router.post("/api/plan-trip", response_model=TravelPlanResponse)
async def plan_trip(
    request: TravelPlanRequest,  # ✅ Validated by Pydantic
    agent_service: AgentService = Depends(get_agent_service),
    llm_service: LLMService = Depends(get_llm_service),
)
```

### Step 2: Dependency Injection

FastAPI's `Depends()` creates/injects:

```python
def get_agent_service() -> AgentService:
    return AgentService()  # Initializes LangGraph agent

def get_llm_service() -> LLMService:
    return LLMService(api_key=settings.google_api_key)  # Loads Gemini
```

### Step 3: Initialize Agent State

```python
initial_state: AgentState = {
    "query": "I want to relax at a beach",
    "travel_style": "",           # Will be filled by classifier
    "destination": "",             # Will be filled by RAG
    "destination_info": {},        # Will be filled by RAG
    "weather_info": {},            # Will be filled by weather
    "errors": []                   # Track any errors
}
```

### Step 4: LangGraph Workflow Execution

The graph has 4 nodes that execute sequentially:

#### **Node 1: Classify**
```python
def node_classify(state: AgentState) -> AgentState:
    """Classify travel style from query."""
    try:
        result = classify_travel_style(state["query"])
        # Result: {"travel_style": "relaxation"}
        state["travel_style"] = result["travel_style"]
    except Exception as e:
        state["errors"].append(f"Classifier error: {str(e)}")
        state["travel_style"] = "balanced"  # Fallback
    return state
```

**Classifier Logic:**
```python
# Input: "I want to relax at a beach"
# Simple keyword matching:
- "relax" found in text
- "beach" found in text
# Output: travel_style = "relaxation"
```

#### **Node 2: RAG (Retrieve Destination)**
```python
def node_rag(state: AgentState) -> AgentState:
    """Retrieve destination based on travel style."""
    destination_info = retrieve_destination(state["travel_style"])
    # travel_style="relaxation" → destination="Bali, Indonesia"
    state["destination"] = destination_info["destination"]
    state["destination_info"] = destination_info
    return state
```

**RAG Mapping:**
```python
# Input: travel_style = "relaxation"
# Lookup: style_mapping["relaxation"] = "bali"
# Database: DESTINATIONS["bali"] = {
#     "destination": "Bali, Indonesia",
#     "description": "Tropical paradise with beaches..."
# }
# Output: Destination info dict
```

#### **Node 3: Weather**
```python
def node_weather(state: AgentState) -> AgentState:
    """Get weather for destination."""
    weather = get_weather(state.get("destination", ""))
    # Input: "Bali, Indonesia"
    # Output: {"temperature": "28°C", "condition": "Sunny"}
    state["weather_info"] = weather
    return state
```

**Weather Logic:**
```python
# Input: "Bali, Indonesia"
# Check: "tropical" in destination → set temp range 28-32°C
# Random selection: condition from ["Sunny", "Clear", "Warm"]
# Output: Weather dict
```

#### **Node 4: Synthesis**
```python
# State now contains:
state = {
    "query": "I want to relax at a beach",
    "travel_style": "relaxation",
    "destination": "Bali, Indonesia",
    "destination_info": {
        "destination": "Bali, Indonesia",
        "description": "Tropical paradise with..."
    },
    "weather_info": {
        "temperature": "28°C",
        "condition": "Sunny"
    },
    "errors": []
}
```

### Step 5: LLM Synthesis (Gemini)

```python
explanation = await llm_service.synthesize_response(
    query="I want to relax at a beach",
    travel_style="relaxation",
    destination="Bali, Indonesia",
    description="Tropical paradise with...",
    temperature="28°C",
    condition="Sunny"
)

# Prompt sent to Gemini:
"""
Based on the user's travel query and the analysis below, 
provide a concise travel recommendation:

User Query: I want to relax at a beach
Travel Style: relaxation
Recommended Destination: Bali, Indonesia
Description: Tropical paradise with stunning beaches...
Current Weather: 28°C, Sunny

Please provide a brief explanation...
"""

# Gemini Returns:
"""
Bali is the perfect destination for your relaxation needs. 
With pristine beaches, world-class spas, and spiritual temples, 
it offers the ideal escape for unwinding. The tropical weather 
ensures warm days and excellent beach conditions...
"""
```

### Step 6: Build Response

```python
response = TravelPlanResponse(
    recommended_destination="Bali, Indonesia",
    travel_style="relaxation",
    explanation="Bali is the perfect destination...",
    weather_summary="28°C, Sunny"
)
```

### Step 7: Return to Frontend

```json
{
  "recommended_destination": "Bali, Indonesia",
  "travel_style": "relaxation",
  "explanation": "Bali is the perfect destination...",
  "weather_summary": "28°C, Sunny"
}
```

### Step 8: Frontend Renders Response

```jsx
{response && (
  <div className="response">
    <div className="result-card">
      <h3>📍 Destination</h3>
      <p>{response.recommended_destination}</p>  {/* Bali, Indonesia */}
    </div>
    <div className="result-card">
      <h3>🎨 Travel Style</h3>
      <p>{response.travel_style}</p>  {/* relaxation */}
    </div>
    <div className="result-card">
      <h3>💡 Why This Destination</h3>
      <p>{response.explanation}</p>  {/* Full explanation */}
    </div>
    <div className="result-card">
      <h3>🌤️ Current Weather</h3>
      <p>{response.weather_summary}</p>  {/* 28°C, Sunny */}
    </div>
  </div>
)}
```

---

## Error Handling at Each Step

### Classifier Fails
```python
try:
    result = classify_travel_style(state["query"])
except Exception as e:
    state["errors"].append(f"Classifier error: {str(e)}")
    state["travel_style"] = "balanced"  # ✅ Fallback
```

### RAG Fails
```python
try:
    destination_info = retrieve_destination(state["travel_style"])
except Exception as e:
    state["errors"].append(f"RAG error: {str(e)}")
    state["destination_info"] = {
        "destination": "Tokyo, Japan",  # ✅ Fallback
        "description": "Default destination"
    }
```

### Weather Fails
```python
try:
    weather = get_weather(state.get("destination", ""))
except Exception as e:
    state["errors"].append(f"Weather error: {str(e)}")
    state["weather_info"] = {
        "temperature": "22°C",  # ✅ Fallback
        "condition": "Clear"
    }
```

### LLM Fails
```python
try:
    explanation = await llm_service.synthesize_response(...)
except Exception as e:
    explanation = "Unable to generate explanation at this time."  # ✅ Fallback
```

---

## LangSmith Tracing

When enabled, LangSmith traces:

1. **Agent Execution** - Full workflow trace
2. **Tool Calls** - Each tool invocation
3. **LLM Calls** - Gemini API calls
4. **Latency** - Timing of each component
5. **Errors** - Any exceptions or failures

**To view traces:**
1. Go to https://smith.langchain.com/
2. Find your project
3. View execution traces with full details

---

## Performance Timeline

```
User Query
  │ 0ms
  └─ FastAPI route (validation)
    │ 5ms
    └─ Classifier (rule-based)
      │ 10ms
      └─ RAG Tool (lookup)
        │ 15ms
        └─ Weather Tool (random)
          │ 20ms
          └─ Gemini LLM API Call (1-3 seconds)
            │ 2000ms+
            └─ Response Construction
              │ 2100ms+
              └─ Return to Frontend
```

**Total latency: ~2-3 seconds** (mostly Gemini API)

---

## Key Points

✅ **Async throughout** - All operations are non-blocking  
✅ **Graceful degradation** - Fallbacks at each step  
✅ **Type safety** - Pydantic validates all data  
✅ **Observability** - LangSmith tracks everything  
✅ **Stateless** - Each request is independent  
✅ **Dependency injection** - Services cleanly separated  
✅ **Error handling** - Never crashes, always responds  

---

## Try It Yourself

```bash
# Start the system
docker-compose up --build

# Send a request
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{"query": "I want an adventure"}'

# View response
{
  "recommended_destination": "New Zealand",
  "travel_style": "adventure",
  "explanation": "...",
  "weather_summary": "..."
}

# Check LangSmith dashboard for full trace
```

---

**Next: Check [API_REFERENCE.md](API_REFERENCE.md) for endpoint examples**
