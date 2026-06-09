from dataclasses import dataclass, field
from typing import List, Optional

from phase0.config.settings import Settings
from phase0.models.preferences import UserPreferences
from phase0.models.restaurant import Restaurant
from phase3.filter import RelaxFlags, apply_filters
from phase3.selector import select_candidates


def _relaxation_steps(prefs: UserPreferences) -> List[tuple[RelaxFlags, str]]:
  """Build relaxation order. Never drop an explicit cuisine preference."""
  steps: List[tuple[RelaxFlags, str]] = [
    ({"cravings"}, "cravings"),
  ]
  if not prefs.cuisine:
    steps.append(({"cuisine"}, "cuisine"))
  steps.extend(
    [
      ({"budget"}, "budget"),
      ({"min_rating"}, "minimum rating"),
    ]
  )
  final_flags: RelaxFlags = {"budget", "min_rating"}
  if not prefs.cuisine:
    final_flags.add("cuisine")
  steps.append((final_flags, "all constraints"))
  return steps


@dataclass
class FilterResult:
  candidates: List[Restaurant]
  relaxed_constraints: List[str] = field(default_factory=list)


def _filter_with_relaxation(
  restaurants: List[Restaurant],
  prefs: UserPreferences,
  settings: Settings,
) -> FilterResult:
  """Filter restaurants with optional progressive relaxation when no matches are found."""
  strict_matches = apply_filters(restaurants, prefs)
  if strict_matches:
    return FilterResult(
      candidates=select_candidates(strict_matches, settings.candidate_limit),
    )

  if not settings.enable_filter_relaxation:
    return FilterResult(candidates=[])

  accumulated: RelaxFlags = set()
  relaxed_labels: List[str] = []

  for step_flags, step_label in _relaxation_steps(prefs):
    accumulated |= step_flags
    matches = apply_filters(restaurants, prefs, relax=accumulated)
    if matches:
      relaxed_labels.append(step_label)
      return FilterResult(
        candidates=select_candidates(matches, settings.candidate_limit),
        relaxed_constraints=relaxed_labels,
      )

  return FilterResult(candidates=[])


def _infer_city_for_location(
  location: str,
  restaurants: List[Restaurant],
) -> Optional[str]:
  """Resolve the parent city when the user searched by neighborhood/area."""
  query = location.strip().lower()
  if not query:
    return None

  cities = {restaurant.location.strip() for restaurant in restaurants if restaurant.location}
  if query in {city.lower() for city in cities}:
    for city in cities:
      if city.lower() == query:
        return city

  for restaurant in restaurants:
    area = (restaurant.area or "").strip().lower()
    if area == query and restaurant.location:
      return restaurant.location.strip()

  return None


def _merge_area_and_city_candidates(
  area_candidates: List[Restaurant],
  city_candidates: List[Restaurant],
  area_name: str,
  limit: int,
) -> List[Restaurant]:
  """Keep neighborhood picks first, then fill from the wider city search."""
  area_key = area_name.strip().lower()
  seen = set()
  ordered: List[Restaurant] = []

  for restaurant in area_candidates:
    key = restaurant.name.strip().lower()
    if key in seen:
      continue
    seen.add(key)
    ordered.append(restaurant)

  in_area = [
    restaurant
    for restaurant in city_candidates
    if (restaurant.area or "").strip().lower() == area_key
    and restaurant.name.strip().lower() not in seen
  ]
  out_of_area = [
    restaurant
    for restaurant in city_candidates
    if (restaurant.area or "").strip().lower() != area_key
    and restaurant.name.strip().lower() not in seen
  ]

  for restaurant in in_area + out_of_area:
    key = restaurant.name.strip().lower()
    if key in seen:
      continue
    seen.add(key)
    ordered.append(restaurant)
    if len(ordered) >= limit:
      break

  return ordered[:limit]


def filter_restaurants(
  restaurants: List[Restaurant],
  prefs: UserPreferences,
  settings: Settings,
) -> FilterResult:
  """Filter restaurants and broaden to city-wide search when an area is too sparse."""
  area_result = _filter_with_relaxation(restaurants, prefs, settings)

  if len(area_result.candidates) >= settings.top_n:
    return area_result

  city = _infer_city_for_location(prefs.location, restaurants)
  if not city or city.strip().lower() == prefs.location.strip().lower():
    return area_result

  city_prefs = prefs.model_copy(update={"location": city})
  city_result = _filter_with_relaxation(restaurants, city_prefs, settings)
  if not city_result.candidates:
    return area_result

  merged = _merge_area_and_city_candidates(
    area_result.candidates,
    city_result.candidates,
    prefs.location,
    settings.candidate_limit,
  )
  if len(merged) <= len(area_result.candidates):
    return area_result

  relaxed = list(area_result.relaxed_constraints or city_result.relaxed_constraints)
  if f"location (expanded to {city})" not in relaxed:
    relaxed.append(f"location (expanded to {city})")
  for label in city_result.relaxed_constraints:
    if label not in relaxed:
      relaxed.append(label)

  return FilterResult(candidates=merged, relaxed_constraints=relaxed)


def build_empty_state(prefs: UserPreferences, settings: Settings) -> dict:
  """Build a helpful empty-state response when filtering returns zero candidates."""
  suggestions = [
    f"Try a different area (searched: {prefs.location})",
    "Relax your budget constraint",
    "Lower the minimum rating",
    "Remove or broaden cuisine preference",
    "Clear specific cravings or pick fewer options",
  ]

  if not settings.enable_filter_relaxation:
    suggestions.append("Enable filter relaxation to broaden the search automatically")

  return {
    "status": "no_matches",
    "message": f"No restaurants found matching preferences in {prefs.location}.",
    "suggestions": suggestions,
    "recommendations": [],
  }
