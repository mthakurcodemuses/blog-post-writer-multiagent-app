import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    MODEL_NAME: str = "gpt-3.5-turbo"
    MAX_REVISIONS: int = 2
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()
