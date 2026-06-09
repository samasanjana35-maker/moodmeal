from phase1.preprocessor import (
  classify_budget,
  extract_city,
  parse_cost,
  parse_cuisines,
  parse_rating,
)


def test_parse_rating_from_fraction():
  assert parse_rating("4.1/5") == 4.1


def test_parse_rating_invalid_returns_none():
  assert parse_rating("NEW") is None


def test_parse_cost():
  amount, display = parse_cost("800")
  assert amount == 800
  assert display == "₹800 for two"


def test_classify_budget_tiers():
  assert classify_budget(300) == "low"
  assert classify_budget(800) == "medium"
  assert classify_budget(1500) == "high"


def test_parse_cuisines_splits_on_commas():
  assert parse_cuisines("North Indian, Chinese") == ["North Indian", "Chinese"]


def test_extract_city_from_url():
  city = extract_city(
    address=None,
    url="https://www.zomato.com/bangalore/jalsa-banashankari",
  )
  assert city == "Bangalore"
