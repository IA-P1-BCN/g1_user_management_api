"""Application settings, loaded from the environment and validated once."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Required fields make startup fail fast when missing."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str
    database_url: str


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings instance (validated on first use)."""
    return Settings()
