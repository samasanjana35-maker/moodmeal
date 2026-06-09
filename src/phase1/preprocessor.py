import re
from typing import Dict, List, Optional, Tuple

from phase0.models.restaurant import Restaurant

CITY_ALIASES = {
  "bangalore": "Bangalore",
  "bengaluru": "Bangalore",
  "banglore": "Bangalore",
  "bengalore": "Bangalore",
  "delhi": "Delhi",
  "new delhi": "Delhi",
}

BUDGET_LOW_MAX = 400
BUDGET_MEDIUM_MAX = 1000

COST_FIELD = "cost"
NAME_FIELD = "name"
URL_FIELD = "url"
ADDRESS_FIELD = "address"
AREA_FIELD = "area"
CUISINES_FIELD = "cuisines"
RATE_FIELD = "rate"


def preprocess_record(fields: Dict[str, Optional[str]]) -> Optional[Restaurant]:
  """Normalize one extracted record into a Restaurant, or None if invalid."""
  name = fields.get(NAME_FIELD)
  if not name:
    return None

  city = extract_city(
    address=fields.get(ADDRESS_FIELD),
    url=fields.get(URL_FIELD),
    area=fields.get(AREA_FIELD),
  )
  if not city:
    return None

  area = _normalize_area(fields.get(AREA_FIELD))
  cuisines = parse_cuisines(fields.get(CUISINES_FIELD))
  cost_value, cost_display = parse_cost(fields.get(COST_FIELD))
  budget_tier = classify_budget(cost_value)
  rating = parse_rating(fields.get(RATE_FIELD))

  return Restaurant(
    name=name,
    location=city,
    area=area,
    cuisines=cuisines,
    cost=cost_display,
    budget_tier=budget_tier,
    rating=rating,
  )


def preprocess_records(rows: List[Dict[str, Optional[str]]]) -> List[Restaurant]:
  """Normalize and deduplicate a batch of extracted records."""
  deduped: Dict[Tuple[str, str, str], Restaurant] = {}

  for row in rows:
    restaurant = preprocess_record(row)
    if restaurant is None:
      continue

    key = (
      restaurant.name.lower(),
      restaurant.location.lower(),
      (restaurant.area or "").lower(),
    )
    existing = deduped.get(key)
    if existing is None or _rating_value(restaurant.rating) > _rating_value(existing.rating):
      deduped[key] = restaurant

  return list(deduped.values())


def extract_city(
  address: Optional[str],
  url: Optional[str] = None,
  area: Optional[str] = None,
) -> Optional[str]:
  """Derive a canonical city name from URL, address, or dataset context."""
  city_from_url = _extract_city_from_url(url)
  if city_from_url:
    return city_from_url

  if address:
    lower_address = address.lower()
    for alias, canonical in sorted(CITY_ALIASES.items(), key=lambda item: -len(item[0])):
      if alias in lower_address:
        return canonical

  if area:
    normalized_area = area.strip().lower()
    if normalized_area in CITY_ALIASES:
      return CITY_ALIASES[normalized_area]

  if address or url or area:
    return "Bangalore"

  return None


def _extract_city_from_url(url: Optional[str]) -> Optional[str]:
  if not url:
    return None

  lower_url = url.lower()
  for alias, canonical in CITY_ALIASES.items():
    if f"/{alias}/" in lower_url or f"{alias}?" in lower_url:
      return canonical
    if alias in lower_url and canonical == "Bangalore":
      return canonical
  return None


def _normalize_area(value: Optional[str]) -> Optional[str]:
  if not value:
    return None
  area = value.strip()
  return _title_case_city(area) if area else None


def parse_cuisines(value: Optional[str]) -> List[str]:
  if not value:
    return []

  parts = re.split(r"[,/|]", value)
  cuisines: List[str] = []
  seen = set()

  for part in parts:
    cuisine = part.strip()
    if not cuisine:
      continue
    key = cuisine.lower()
    if key not in seen:
      seen.add(key)
      cuisines.append(cuisine)

  return cuisines


def parse_cost(value: Optional[str]) -> Tuple[Optional[int], Optional[str]]:
  if not value:
    return None, None

  match = re.search(r"\d+", value.replace(",", ""))
  if not match:
    return None, None

  amount = int(match.group())
  return amount, f"₹{amount:,} for two"


def classify_budget(cost_value: Optional[int]) -> Optional[str]:
  if cost_value is None:
    return None
  if cost_value <= BUDGET_LOW_MAX:
    return "low"
  if cost_value <= BUDGET_MEDIUM_MAX:
    return "medium"
  return "high"


def parse_rating(value: Optional[str]) -> Optional[float]:
  if not value:
    return None

  match = re.search(r"(\d+(?:\.\d+)?)", value)
  if not match:
    return None

  rating = float(match.group(1))
  if rating < 0 or rating > 5:
    return None
  return rating


def _rating_value(rating: Optional[float]) -> float:
  return rating if rating is not None else -1.0


def _title_case_city(value: str) -> str:
  return " ".join(word.capitalize() for word in value.split())
