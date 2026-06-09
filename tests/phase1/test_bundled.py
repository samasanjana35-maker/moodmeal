import json

from phase0.models.restaurant import Restaurant
from phase1.bundled import load_bundled_restaurants


def test_load_bundled_restaurants_returns_none_when_missing(tmp_path):
  assert load_bundled_restaurants(tmp_path / "missing.json") is None


def test_load_bundled_restaurants_parses_valid_payload(tmp_path):
  payload = [
    Restaurant(
      name="Test Cafe",
      location="Bangalore",
      area="Indiranagar",
      cuisines=["Italian"],
      cost="₹600 for two",
      budget_tier="medium",
      rating=4.2,
    ).model_dump()
  ]
  path = tmp_path / "restaurants.json"
  path.write_text(json.dumps(payload), encoding="utf-8")

  loaded = load_bundled_restaurants(path)
  assert loaded is not None
  assert len(loaded) == 1
  assert loaded[0].name == "Test Cafe"
