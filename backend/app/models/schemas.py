from pydantic import BaseModel


class TravelPlanRequest(BaseModel):
    """Input schema for travel planning."""
    query: str


class TravelStyleOutput(BaseModel):
    """Output from classifier tool."""
    travel_style: str


class DestinationInfo(BaseModel):
    """Output from RAG tool."""
    destination: str
    description: str


class WeatherInfo(BaseModel):
    """Output from weather tool."""
    temperature: str
    condition: str


class TravelPlanResponse(BaseModel):
    """Final response schema."""
    recommended_destination: str
    travel_style: str
    explanation: str
    weather_summary: str
