"""Routes for travel planning."""

from fastapi import APIRouter, Depends
from ..models.schemas import TravelPlanRequest, TravelPlanResponse
from ..services.agent_service import AgentService
from ..services.llm_service import LLMService
from ..core.config import settings

router = APIRouter(prefix="/api", tags=["travel"])


def get_agent_service() -> AgentService:
    """Dependency: get agent service."""
    return AgentService()


def get_llm_service() -> LLMService:
    """Dependency: get LLM service."""
    return LLMService(api_key=settings.google_api_key)


@router.post("/plan-trip", response_model=TravelPlanResponse)
async def plan_trip(
    request: TravelPlanRequest,
    agent_service: AgentService = Depends(get_agent_service),
    llm_service: LLMService = Depends(get_llm_service),
) -> TravelPlanResponse:
    """Plan a trip based on user query."""
    
    # Run agent pipeline
    agent_result = await agent_service.run_agent(request.query)
    
    # Synthesize response using LLM
    explanation = await llm_service.synthesize_response(
        query=request.query,
        travel_style=agent_result["travel_style"],
        destination=agent_result["destination"],
        description=agent_result["destination_info"].get("description", ""),
        temperature=agent_result["weather_info"].get("temperature", ""),
        condition=agent_result["weather_info"].get("condition", ""),
    )
    
    return TravelPlanResponse(
        recommended_destination=agent_result["destination"],
        travel_style=agent_result["travel_style"],
        explanation=explanation,
        weather_summary=f"{agent_result['weather_info'].get('temperature', '')}, {agent_result['weather_info'].get('condition', '')}"
    )
