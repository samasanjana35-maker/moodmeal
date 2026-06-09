import pytest

from phase0.fixtures.mock_data import MOCK_RESTAURANTS
from phase0.models.preferences import UserPreferences


@pytest.fixture
def sample_preferences() -> UserPreferences:
  return UserPreferences(
    location="Bangalore",
    budget=1000,
    cuisine="Italian",
    min_rating=4.0,
  )


@pytest.fixture
def mock_restaurants():
  return MOCK_RESTAURANTS.copy()
