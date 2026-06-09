from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
  """Application configuration loaded from environment or .env file."""

  model_config = SettingsConfigDict(
    env_file=str(ENV_FILE) if ENV_FILE.exists() else ".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )

  dataset_id: str = "ManikaSaini/zomato-restaurant-recommendation"
  dataset_split: str = "train"
  data_cache_dir: str = "data/cache"
  use_dataset_cache: bool = True
  groq_api_key: Optional[str] = None
  llm_model: str = "llama-3.3-70b-versatile"
  llm_max_retries: int = Field(default=2, ge=0)
  llm_timeout_seconds: float = Field(default=30.0, gt=0)
  top_n: int = Field(default=5, ge=1)
  candidate_limit: int = Field(default=30, ge=1)
  enable_filter_relaxation: bool = True
  backend_url: Optional[str] = None
  deployment_mode: str = "monolith"
  api_host: str = "0.0.0.0"
  api_port: int = Field(default=8000, ge=1, le=65535)
  cors_origins: str = (
    "http://localhost:8501,http://127.0.0.1:8501,"
    "http://localhost:3000,http://127.0.0.1:3000"
  )

  def cors_origins_list(self) -> list:
    origins = [item.strip() for item in self.cors_origins.split(",") if item.strip()]
    return origins or ["*"]

  def resolve_cache_path(self) -> Path:
    return Path(self.data_cache_dir) / "restaurants.json"

  @field_validator("top_n", "candidate_limit", mode="before")
  @classmethod
  def coerce_positive_int(cls, value: object, info) -> int:
    if value is None:
      return 5 if info.field_name == "top_n" else 30
    try:
      parsed = int(value)
    except (TypeError, ValueError):
      return 5 if info.field_name == "top_n" else 30
    return max(parsed, 1)


@lru_cache
def get_settings() -> Settings:
  return Settings()


def refresh_settings() -> Settings:
  """Clear cached settings after secrets/env change (Phase 8 deploy)."""
  get_settings.cache_clear()
  return get_settings()
