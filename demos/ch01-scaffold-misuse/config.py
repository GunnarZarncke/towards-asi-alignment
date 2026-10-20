"""Cached configuration for the Chapter 1 FastAPI demo."""

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from the repository environment file."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    debug: bool = False
    posthog_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("POSTHOG_API_KEY", "POSTHOG_PROJECT_TOKEN"),
    )
    posthog_host: str | None = None
    posthog_privacy_mode: bool = True


@lru_cache
def get_settings() -> Settings:
    """Get the cached application settings."""
    return Settings()
