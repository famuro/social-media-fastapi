from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    app_name: str = "Social Media API"
    environment: str = "development"
    database_url: str

    jwt_secret_key: SecretStr = Field(min_length=64)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.

    Using lru_cache prevents repeatedly reading environment
    variables throughout the lifetime of the application.
    """

    return Settings()


settings: Settings = get_settings()
