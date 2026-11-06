from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RealEstate AI API"
    environment: str = "local"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://reai:reai_dev_password@localhost:5432/reai"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    model_config = SettingsConfigDict(env_file=".env", env_prefix="REAI_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
