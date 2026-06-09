from phase0.config.settings import Settings
from phase0.models.preferences import UserPreferences
from phase0.models.restaurant import Restaurant
from phase3.integration import run_integration


def test_run_integration_returns_empty_state_when_no_matches():
  prefs = UserPreferences(location="Goa", budget=500)
  restaurants = [
    Restaurant(name="Local", location="Bangalore", cuisines=["Indian"], budget_tier="low", rating=4.0),
  ]
  result = run_integration(restaurants, prefs, Settings(enable_filter_relaxation=False))
  assert result.empty_state is not None
  assert result.empty_state["status"] == "no_matches"
  assert result.prompt is None


def test_run_integration_builds_prompt_for_matches():
  prefs = UserPreferences(location="Bangalore", budget=1000, cuisine="Italian", min_rating=4.0)
  restaurants = [
    Restaurant(name="Truffles", location="Bangalore", cuisines=["Italian"], budget_tier="medium", rating=4.3),
  ]
  result = run_integration(restaurants, prefs, Settings())
  assert result.empty_state is None
  assert result.prompt is not None
  assert len(result.candidates) == 1
