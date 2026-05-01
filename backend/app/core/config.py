from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    google_api_key: str
    langchain_api_key: str
    langchain_tracing_v2: bool = True
    langsmith_project: str = "travel-ai-agent"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
