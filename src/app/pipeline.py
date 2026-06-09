from typing import Optional

from phase0.config.settings import Settings, get_settings
from phase0.models.preferences import UserPreferences
from phase1.pipeline import get_restaurants
from phase2.input import collect_preferences
from phase3 import run_integration
from phase4 import generate_recommendations
from phase5 import format_pipeline_result


def run_pipeline(
  settings: Optional[Settings] = None,
  preferences: Optional[UserPreferences] = None,
) -> dict:
  """Run the end-to-end recommendation pipeline."""
  settings = settings or get_settings()

  restaurants = get_restaurants(settings)
  preferences = preferences or collect_preferences()
  integration = run_integration(restaurants, preferences, settings)

  if integration.empty_state:
    return format_pipeline_result(empty_state=integration.empty_state)

  recommendation_result = generate_recommendations(
    integration.prompt,
    integration.candidates,
    settings=settings,
    top_n=settings.top_n,
  )

  return format_pipeline_result(
    recommendations=recommendation_result.recommendations,
    relaxed_constraints=integration.relaxed_constraints,
    fallback_used=recommendation_result.fallback_used,
    fallback_message=recommendation_result.fallback_message,
  )
