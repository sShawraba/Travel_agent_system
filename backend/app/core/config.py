from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # LLM & LangSmith
    google_api_key: str
    langchain_api_key: str
    langchain_tracing_v2: bool = True
    langsmith_project: str = "travel-ai-agent"
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/travel_ai"
    
    # Auth
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
