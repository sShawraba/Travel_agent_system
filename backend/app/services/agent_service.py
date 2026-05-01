"""Agent service for LangGraph orchestration."""

from typing import Any
from langchain_core.tools import tool
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from ..tools.classifier_tool import classify_travel_style
from ..tools.rag_tool import retrieve_destination
from ..tools.weather_tool import get_weather


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
    
    def __init__(self):
        self.graph = self._build_graph()
    
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
    
    async def run_agent(self, query: str) -> dict:
        """Run the agent with the given query."""
        initial_state: AgentState = {
            "query": query,
            "travel_style": "",
            "destination": "",
            "destination_info": {},
            "weather_info": {},
            "errors": []
        }
        
        result = self.graph.invoke(initial_state)
        return result
