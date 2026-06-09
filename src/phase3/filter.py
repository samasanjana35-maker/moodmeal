from typing import List, Optional, Set

from phase0.models.preferences import UserPreferences
from phase0.models.restaurant import Restaurant
from phase1.preprocessor import parse_cost

RelaxFlags = Set[str]


def apply_filters(
  restaurants: List[Restaurant],
  prefs: UserPreferences,
  relax: Optional[RelaxFlags] = None,
) -> List[Restaurant]:
  """Apply hard constraints and return all matching restaurants (unordered)."""
  relax = relax or set()
  return [
    restaurant
    for restaurant in restaurants
    if matches_preferences(restaurant, prefs, relax=relax)
  ]


def matches_preferences(
  restaurant: Restaurant,
  prefs: UserPreferences,
  relax: Optional[RelaxFlags] = None,
) -> bool:
  """Return True when a restaurant satisfies all active preference constraints."""
  relax = relax or set()

  if not _matches_location(restaurant, prefs):
    return False
  if "min_rating" not in relax and not _matches_rating(restaurant, prefs):
    return False
  if "budget" not in relax and not _matches_budget(restaurant, prefs):
    return False
  if "cuisine" not in relax and not _matches_cuisine(restaurant, prefs):
    return False
  if "cravings" not in relax and not _matches_cravings(restaurant, prefs):
    return False
  return True


def _matches_location(restaurant: Restaurant, prefs: UserPreferences) -> bool:
  queries = _location_queries(prefs.location)
  city = restaurant.location.strip().lower()
  area = (restaurant.area or "").strip().lower()
  return any(query == city or query == area for query in queries)


def _location_queries(location: str) -> Set[str]:
  """Normalize location input — supports city, area, or 'City, Area' text."""
  raw = location.strip().lower()
  if not raw:
    return set()

  queries = {raw}
  if "," in raw:
    queries.update(part.strip() for part in raw.split(",") if part.strip())
  return queries


def _matches_rating(restaurant: Restaurant, prefs: UserPreferences) -> bool:
  if prefs.min_rating <= 0:
    return True
  if restaurant.rating is None:
    return False
  return restaurant.rating >= prefs.min_rating


def _matches_budget(restaurant: Restaurant, prefs: UserPreferences) -> bool:
  cost_amount = _restaurant_cost_amount(restaurant)
  if cost_amount is None:
    return True
  return cost_amount <= prefs.budget


def _restaurant_cost_amount(restaurant: Restaurant) -> Optional[int]:
  if not restaurant.cost:
    return None
  amount, _ = parse_cost(restaurant.cost)
  return amount


def _matches_cuisine(restaurant: Restaurant, prefs: UserPreferences) -> bool:
  if not prefs.cuisine:
    return True

  requested = _normalize_cuisine_request(prefs.cuisine)
  if not requested:
    return True

  restaurant_cuisines = [item.lower() for item in restaurant.cuisines]
  for cuisine in requested:
    if cuisine in restaurant_cuisines:
      return True
    if any(cuisine in restaurant_cuisine for restaurant_cuisine in restaurant_cuisines):
      return True
  return False


def _matches_cravings(restaurant: Restaurant, prefs: UserPreferences) -> bool:
  if not prefs.cravings:
    return True

  haystack = " ".join(restaurant.cuisines).lower() + " " + restaurant.name.lower()
  for craving in prefs.cravings:
    token = craving.strip().lower()
    if not token:
      continue
    if token in haystack:
      return True
    if all(part in haystack for part in token.split() if len(part) > 2):
      return True
  return False


def _normalize_cuisine_request(cuisine) -> Set[str]:
  if isinstance(cuisine, str):
    value = cuisine.strip().lower()
    return {value} if value else set()
  return {item.strip().lower() for item in cuisine if item.strip()}
