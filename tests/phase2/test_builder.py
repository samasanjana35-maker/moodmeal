import pytest

from phase2.builder import PreferenceValidationError, build_preferences
from phase2.validator import validate_raw_preferences


def test_build_preferences_success():
  prefs = build_preferences(
    {
      "location": "Bangalore",
      "budget": 2000,
      "cuisine": "Italian",
      "min_rating": 4.0,
      "extras": "family-friendly",
    }
  )
  assert prefs.location == "Bangalore"
  assert prefs.budget == 2000
  assert prefs.cuisine == "Italian"


def test_validate_missing_location():
  errors = validate_raw_preferences({"location": "", "budget": 500})
  assert "Location is required." in errors


def test_build_preferences_invalid_budget():
  with pytest.raises(PreferenceValidationError) as exc_info:
    build_preferences({"location": "Bangalore", "budget": "cheap"})
  assert any("Budget must be" in error for error in exc_info.value.errors)
