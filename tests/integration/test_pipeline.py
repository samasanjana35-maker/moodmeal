from app.pipeline import run_pipeline
from phase0.config.settings import Settings
from phase0.models.preferences import UserPreferences


def test_run_pipeline_with_preferences():
  preferences = UserPreferences(
    location="Bangalore",
    budget=1000,
    cuisine="Italian",
    min_rating=4.0,
  )
  result = run_pipeline(Settings(), preferences=preferences)
  assert result["status"] == "success"
  assert result["count"] > 0
