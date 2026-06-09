from typing import Any, Dict, Optional

from phase0.config.settings import Settings, get_settings
from phase2.builder import build_preferences
from app.pipeline import run_pipeline

from backend.api.schemas import RecommendationRequest


def get_recommendations(
  body: RecommendationRequest,
  settings: Optional[Settings] = None,
) -> Dict[str, Any]:
  """Validate request, run pipeline, return formatted JSON."""
  preferences = build_preferences(body.model_dump(mode="json"))
  return run_pipeline(settings or get_settings(), preferences=preferences)
