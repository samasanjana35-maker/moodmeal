from phase0.config.settings import Settings
from phase0.models.preferences import UserPreferences
from phase0.models.restaurant import Restaurant
from phase3.filter import apply_filters, matches_preferences
from phase3.fallback import filter_restaurants
from phase3.selector import select_candidates


def test_filter_restaurants_matches_location_and_cuisine(sample_preferences, mock_restaurants):
  settings = Settings()
  result = filter_restaurants(mock_restaurants, sample_preferences, settings)
  assert len(result.candidates) == 1
  assert result.candidates[0].name == "Truffles"


def test_filter_restaurants_no_match(sample_preferences, mock_restaurants):
  sample_preferences.location = "Goa"
  settings = Settings()
  result = filter_restaurants(mock_restaurants, sample_preferences, settings)
  assert result.candidates == []


def test_filter_matches_cravings_against_cuisine():
  restaurant = Restaurant(
    name="Biryani House",
    location="Bangalore",
    cuisines=["Biryani", "North Indian"],
    cost="₹600 for two",
    rating=4.3,
  )
  prefs = UserPreferences(location="Bangalore", budget=1000, cravings=["Biryani"])
  assert matches_preferences(restaurant, prefs)


def test_filter_excludes_restaurants_above_budget():
  restaurant = Restaurant(
    name="Premium Place",
    location="Bangalore",
    cuisines=["Italian"],
    cost="₹2,500 for two",
    budget_tier="high",
    rating=4.5,
  )
  prefs = UserPreferences(location="Bangalore", budget=2000, cuisine="Italian")
  assert not matches_preferences(restaurant, prefs)


def test_cuisine_partial_match():
  restaurant = Restaurant(
    name="Pizza Place",
    location="Bangalore",
    cuisines=["Italian", "Pizza"],
    cost="₹700 for two",
    budget_tier="medium",
    rating=4.2,
  )
  prefs = UserPreferences(location="Bangalore", budget=1000, cuisine="Pizza")
  assert matches_preferences(restaurant, prefs)


def test_unknown_cost_is_included():
  restaurant = Restaurant(
    name="Mystery Cafe",
    location="Bangalore",
    cuisines=["Cafe"],
    budget_tier=None,
    rating=4.0,
  )
  prefs = UserPreferences(location="Bangalore", budget=500, cuisine="Cafe")
  assert matches_preferences(restaurant, prefs)


def test_select_candidates_caps_and_sorts():
  restaurants = [
    Restaurant(name="B", location="Bangalore", rating=4.0),
    Restaurant(name="A", location="Bangalore", rating=4.5),
    Restaurant(name="C", location="Bangalore", rating=3.5),
  ]
  selected = select_candidates(restaurants, limit=2)
  assert [item.name for item in selected] == ["A", "B"]


def test_filter_matches_comma_separated_city_area():
  restaurants = [
    Restaurant(
      name="Bellandur Bistro",
      location="Bangalore",
      area="Bellandur",
      cuisines=["Indian"],
      cost="₹1,500 for two",
      budget_tier="high",
      rating=4.2,
    ),
  ]
  prefs = UserPreferences(
    location="Bangalore, Bellandur",
    budget=2000,
    min_rating=4.0,
  )
  results = apply_filters(restaurants, prefs)
  assert len(results) == 1
  assert results[0].name == "Bellandur Bistro"


def test_filter_matches_area_when_location_is_neighborhood():
  restaurants = [
    Restaurant(
      name="Bellandur Bistro",
      location="Bangalore",
      area="Bellandur",
      cuisines=["Indian"],
      cost="₹1,500 for two",
      budget_tier="high",
      rating=4.2,
    ),
    Restaurant(
      name="Other Place",
      location="Bangalore",
      area="Koramangala",
      cuisines=["Indian"],
      cost="₹1,800 for two",
      budget_tier="high",
      rating=4.5,
    ),
  ]
  prefs = UserPreferences(location="Bellandur", budget=2000, min_rating=4.0)
  results = apply_filters(restaurants, prefs)
  assert len(results) == 1
  assert results[0].name == "Bellandur Bistro"


def test_filter_expands_sparse_area_to_city():
  restaurants = [
    Restaurant(
      name="Local Chinese",
      location="Bangalore",
      area="Koramangala",
      cuisines=["Chinese"],
      cost="₹800 for two",
      rating=3.8,
    ),
    Restaurant(
      name="City Chinese One",
      location="Bangalore",
      area="Indiranagar",
      cuisines=["Chinese"],
      cost="₹900 for two",
      rating=4.5,
    ),
    Restaurant(
      name="City Chinese Two",
      location="Bangalore",
      area="Jayanagar",
      cuisines=["Chinese"],
      cost="₹700 for two",
      rating=4.3,
    ),
  ]
  settings = Settings(top_n=5, candidate_limit=10)
  prefs = UserPreferences(
    location="Koramangala",
    budget=2000,
    cuisine="Chinese",
    min_rating=3.5,
  )
  result = filter_restaurants(restaurants, prefs, settings)
  assert len(result.candidates) == 3
  assert any("expanded to Bangalore" in item for item in result.relaxed_constraints)
  assert result.candidates[0].name == "Local Chinese"


def test_filter_order_independent():
  restaurants = [
    Restaurant(name="One", location="Bangalore", cuisines=["Italian"], cost="₹800 for two", budget_tier="medium", rating=4.2),
    Restaurant(name="Two", location="Delhi", cuisines=["Italian"], cost="₹900 for two", budget_tier="medium", rating=4.8),
  ]
  prefs = UserPreferences(location="Bangalore", budget=1000, cuisine="Italian", min_rating=4.0)
  assert [item.name for item in apply_filters(restaurants, prefs)] == ["One"]
