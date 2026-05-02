"""SQLAlchemy ORM models for database entities."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, VECTOR
import uuid

from .database import Base


class User(Base):
    """User model for authentication and run tracking."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent_runs = relationship("AgentRun", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class AgentRun(Base):
    """Agent run record with user scope."""
    
    __tablename__ = "agent_runs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    query = Column(Text, nullable=False)
    travel_style = Column(String(255), nullable=True)
    recommended_destination = Column(String(255), nullable=True)
    explanation = Column(Text, nullable=True)
    weather_summary = Column(String(500), nullable=True)
    errors = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="agent_runs")
    tool_logs = relationship("ToolCallLog", back_populates="agent_run", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AgentRun(user_id='{self.user_id}', destination='{self.recommended_destination}')>"


class ToolCallLog(Base):
    """Log of tool invocations during agent runs."""
    
    __tablename__ = "tool_call_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), nullable=False, index=True)
    tool_name = Column(String(255), nullable=False)
    tool_input = Column(JSON, nullable=False)
    tool_output = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    agent_run = relationship("AgentRun", back_populates="tool_logs")
    
    def __repr__(self):
        return f"<ToolCallLog(agent_run_id='{self.agent_run_id}', tool='{self.tool_name}')>"


class Destination(Base):
    """Destination with metadata for RAG system."""
    
    __tablename__ = "destinations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)  # e.g., adventure, luxury, cultural, relaxation, budget
    description = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)  # Wikivoyage, blog, tourism board, etc.
    source_url = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    embeddings = relationship("DestinationEmbedding", back_populates="destination", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Destination(name='{self.name}', category='{self.category}')>"


class DestinationEmbedding(Base):
    """Embeddings for destinations using pgvector."""
    
    __tablename__ = "destination_embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id"), nullable=False, index=True)
    embedding = Column(VECTOR(1536), nullable=False)  # OpenAI embeddings are 1536 dimensions
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    destination = relationship("Destination", back_populates="embeddings")
    
    def __repr__(self):
        return f"<DestinationEmbedding(destination_id='{self.destination_id}')>"
