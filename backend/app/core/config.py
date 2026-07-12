from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JobMatch AI"
    # Future: API keys for LLM integration will go here
    # OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
