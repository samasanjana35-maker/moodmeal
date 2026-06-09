from typing import List, Tuple

from phase0.models.restaurant import Restaurant


def select_candidates(restaurants: List[Restaurant], limit: int) -> List[Restaurant]:
  """Rank, deduplicate, and cap the candidate set for LLM prompting."""
  if limit <= 0:
    return []

  deduped = _deduplicate(restaurants)
  ranked = sorted(deduped, key=_ranking_key, reverse=True)
  return ranked[:limit]


def _deduplicate(restaurants: List[Restaurant]) -> List[Restaurant]:
  seen = set()
  unique: List[Restaurant] = []

  for restaurant in restaurants:
    key = (
      restaurant.name.strip().lower(),
      restaurant.location.strip().lower(),
      (restaurant.area or "").strip().lower(),
    )
    if key in seen:
      continue
    seen.add(key)
    unique.append(restaurant)

  return unique


def _ranking_key(restaurant: Restaurant) -> Tuple[float, str]:
  rating = restaurant.rating if restaurant.rating is not None else -1.0
  return (rating, restaurant.name.lower())
