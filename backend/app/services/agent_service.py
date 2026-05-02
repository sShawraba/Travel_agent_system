"""Agent service for LangGraph orchestration."""

from typing import Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from langchain_core.tools import tool
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from ..tools.classifier_tool import classify_travel_style
from ..tools.rag_tool import retrieve_destination
from ..tools.weather_tool import get_weather
from ..core.models import AgentRun, ToolCallLog


class AgentState(TypedDict):
    """State for the agent graph."""
    query: str
    travel_style: str
    destination: str
    destination_info: dict
    weather_info: dict
    errors: list[str]


class AgentService:
    """Service for orchestrating the agent workflow."""
    
    def __init__(self, db: Optional[Session] = None):
        self.graph = self._build_graph()
        self.db = db
    
    def _log_tool_call(
        self,
        agent_run_id: UUID,
        tool_name: str,
        tool_input: dict,
        tool_output: Optional[dict] = None,
        error_message: Optional[str] = None
    ):
        """Log a tool call to the database."""
        if not self.db:
            return
        
        log_entry = ToolCallLog(
            agent_run_id=agent_run_id,
            tool_name=tool_name,
            tool_input=tool_input,
            tool_output=tool_output,
            error_message=error_message
        )
        self.db.add(log_entry)
        self.db.commit()
    
    def _build_graph(self):
        """Build the LangGraph workflow."""
        
        # Define nodes
        def node_classify(state: AgentState) -> AgentState:
            """Classify travel style."""
            try:
                result = classify_travel_style(state["query"])
                state["travel_style"] = result["travel_style"]
            except Exception as e:
                state["errors"].append(f"Classifier error: {str(e)}")
                state["travel_style"] = "balanced"
            return state
        
        def node_rag(state: AgentState) -> AgentState:
            """Retrieve destination information."""
            try:
                destination_info = retrieve_destination(state["travel_style"], state["query"])
                state["destination"] = destination_info["destination"]
                state["destination_info"] = destination_info
            except Exception as e:
                state["errors"].append(f"RAG error: {str(e)}")
                state["destination_info"] = {
                    "destination": "Tokyo, Japan",
                    "description": "Default destination"
                }
            return state
        
        def node_weather(state: AgentState) -> AgentState:
            """Get weather information."""
            try:
                weather = get_weather(state.get("destination", ""))
                state["weather_info"] = weather
            except Exception as e:
                state["errors"].append(f"Weather error: {str(e)}")
                state["weather_info"] = {"temperature": "22°C", "condition": "Clear"}
            return state
        
        # Build graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("classify", node_classify)
        workflow.add_node("rag", node_rag)
        workflow.add_node("weather", node_weather)
        
        # Add edges
        workflow.set_entry_point("classify")

        workflow.add_edge("classify", "rag")
        workflow.add_edge("rag", "weather")
        workflow.add_edge("weather", "__end__")
        
        return workflow.compile()
    
    async def run_agent(
        self,
        query: str,
        user_id: Optional[UUID] = None,
        db: Optional[Session] = None
    ) -> dict:
        """Run the agent with the given query."""
        
        initial_state: AgentState = {
            "query": query,
            "travel_style": "",
            "destination": "",
            "destination_info": {},
            "weather_info": {},
            "errors": []
        }
        
        # Use provided db or instance db
        db_session = db or self.db
        agent_run_id = None
        
        # Create agent run record if user_id provided
        if user_id and db_session:
            agent_run = AgentRun(
                user_id=user_id,
                query=query,
                errors=[]
            )
            db_session.add(agent_run)
            db_session.commit()
            db_session.refresh(agent_run)
            agent_run_id = agent_run.id
        
        result = self.graph.invoke(initial_state)
        
        # Update agent run with results
        if agent_run_id and db_session:
            agent_run = db_session.query(AgentRun).filter(AgentRun.id == agent_run_id).first()
            if agent_run:
                agent_run.travel_style = result.get("travel_style")
                agent_run.recommended_destination = result.get("destination")
                agent_run.errors = result.get("errors", [])
                db_session.commit()
        
        return result
