import pytest

from phase0.models.preferences import UserPreferences


def test_user_preferences_valid():
  prefs = UserPreferences(location="Bangalore", budget=1000)
  assert prefs.budget == 1000


def test_user_preferences_rejects_blank_location():
  with pytest.raises(ValueError):
    UserPreferences(location="  ", budget=1000)


def test_user_preferences_rejects_low_budget():
  with pytest.raises(ValueError):
    UserPreferences(location="Bangalore", budget=50)
