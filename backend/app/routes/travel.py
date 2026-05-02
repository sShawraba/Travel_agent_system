"""Routes for travel planning."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models.schemas import TravelPlanRequest, TravelPlanResponse, AgentRunResponse
from ..services.agent_service import AgentService
from ..services.llm_service import LLMService
from ..core.config import settings
from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..core.models import User, AgentRun

router = APIRouter(prefix="/api", tags=["travel"])


def get_agent_service(db: Session = Depends(get_db)) -> AgentService:
    """Dependency: get agent service with database session."""
    return AgentService(db=db)


def get_llm_service() -> LLMService:
    """Dependency: get LLM service."""
    return LLMService(api_key=settings.google_api_key)


@router.post("/plan-trip", response_model=TravelPlanResponse)
async def plan_trip(
    request: TravelPlanRequest,
    current_user: User = Depends(get_current_user),
    agent_service: AgentService = Depends(get_agent_service),
    llm_service: LLMService = Depends(get_llm_service),
    db: Session = Depends(get_db),
) -> TravelPlanResponse:
    """Plan a trip based on user query (requires authentication)."""
    
    # Run agent pipeline with user context
    agent_result = await agent_service.run_agent(
        query=request.query,
        user_id=current_user.id,
        db=db
    )
    
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


@router.get("/agent-runs", response_model=list[AgentRunResponse])
async def get_agent_runs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all agent runs for the current user."""
    
    agent_runs = db.query(AgentRun).filter(
        AgentRun.user_id == current_user.id
    ).order_by(AgentRun.created_at.desc()).all()
    
    return [AgentRunResponse.from_orm(run) for run in agent_runs]


@router.get("/agent-runs/{run_id}", response_model=AgentRunResponse)
async def get_agent_run(
    run_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific agent run."""
    
    agent_run = db.query(AgentRun).filter(
        AgentRun.id == run_id,
        AgentRun.user_id == current_user.id
    ).first()
    
    if not agent_run:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent run not found"
        )
    
    return AgentRunResponse.from_orm(agent_run)
