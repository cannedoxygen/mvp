import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    SPORTSDATAIO_API_KEY: Optional[str] = None
    ODDS_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    WEATHER_API_KEY: Optional[str] = None
    
    # OpenAI settings
    OPENAI_MODEL: str = "gpt-4"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./baseball_betting.db"
    
    # API settings
    API_PREFIX: str = "/api/v1"
    API_DEBUG: bool = False
    
    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour in seconds
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # Environment
    ENV: str = "development"
    
    # Model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Create global settings object
settings = Settings()