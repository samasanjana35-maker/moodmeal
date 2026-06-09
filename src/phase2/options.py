from functools import lru_cache
from typing import List, Tuple

from phase0.models.preferences import DEFAULT_BUDGET_OPTIONS, DEFAULT_CRAVING_OPTIONS
from phase1.pipeline import get_restaurants


@lru_cache(maxsize=1)
def get_form_options() -> Tuple[List[str], List[str], List[str], List[int], List[str]]:
  """Load city, area, cuisine, budget, and craving options for forms."""
  restaurants = get_restaurants()

  cities = sorted({restaurant.location for restaurant in restaurants})
  areas = sorted(
    {restaurant.area for restaurant in restaurants if restaurant.area}
  )

  cuisine_set = set()
  for restaurant in restaurants:
    cuisine_set.update(restaurant.cuisines)

  cuisines = sorted(cuisine_set)
  budgets = list(DEFAULT_BUDGET_OPTIONS)
  cravings = list(DEFAULT_CRAVING_OPTIONS)
  return cities, areas, cuisines, budgets, cravings
