# backend/app/core/config.py

from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = "Memora OS"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
