from typing import Any, Dict, List, Optional

from phase0.models.recommendation import Recommendation
from phase0.models.restaurant import Restaurant


def apply_guardrails(
  parsed_items: List[Dict[str, Any]],
  candidates: List[Restaurant],
) -> List[Recommendation]:
  """Keep only recommendations that map to the candidate set."""
  lookup = _build_candidate_lookup(candidates)
  recommendations: List[Recommendation] = []
  seen_names = set()

  for item in parsed_items:
    restaurant = _resolve_restaurant(item["name"], lookup)
    if restaurant is None:
      continue

    key = restaurant.name.strip().lower()
    if key in seen_names:
      continue
    seen_names.add(key)

    recommendations.append(
      Recommendation(
        restaurant=restaurant,
        explanation=item.get("explanation") or "Recommended based on your preferences.",
        rank=len(recommendations) + 1,
      )
    )

  return recommendations


def _build_candidate_lookup(
  candidates: List[Restaurant],
) -> Dict[str, Restaurant]:
  lookup: Dict[str, Restaurant] = {}
  for restaurant in candidates:
    lookup[restaurant.name.strip().lower()] = restaurant
  return lookup


def _resolve_restaurant(
  name: str,
  lookup: Dict[str, Restaurant],
) -> Optional[Restaurant]:
  normalized = name.strip().lower()
  if normalized in lookup:
    return lookup[normalized]

  exact_matches = [
    restaurant
    for key, restaurant in lookup.items()
    if key == normalized
  ]
  if len(exact_matches) == 1:
    return exact_matches[0]

  partial_matches = [
    restaurant
    for key, restaurant in lookup.items()
    if normalized in key or key in normalized
  ]
  if len(partial_matches) == 1:
    return partial_matches[0]

  return None
