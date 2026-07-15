from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "JobMatch AI"
    
    # AI Infrastructure Settings
    AI_PROVIDER: str = "openai"
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL_NAME: str = "gpt-4o"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 1500

    class Config:
        env_file = ".env"

settings = Settings()
