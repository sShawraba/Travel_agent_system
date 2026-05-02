from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Auth Schemas
class UserRegister(BaseModel):
    """User registration input."""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login input."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    token_type: str
    user_id: str


class UserResponse(BaseModel):
    """User response (no password)."""
    id: str
    username: str
    email: str
    created_at: datetime


# Travel Planning Schemas
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


# Agent Run Schemas
class AgentRunResponse(BaseModel):
    """Agent run response with full details."""
    id: str
    user_id: str
    query: str
    travel_style: Optional[str]
    recommended_destination: Optional[str]
    explanation: Optional[str]
    weather_summary: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ToolCallLogResponse(BaseModel):
    """Tool call log response."""
    id: str
    agent_run_id: str
    tool_name: str
    tool_input: dict
    tool_output: Optional[dict]
    error_message: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True
