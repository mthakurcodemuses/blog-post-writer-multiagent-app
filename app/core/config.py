from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    MODEL_NAME: str = "gpt-3.5-turbo"
    MAX_REVISIONS: int = 2
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    UI_PORT: int = 5000

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()

settings = get_settings()