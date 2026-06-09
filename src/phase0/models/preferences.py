from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator

BUDGET_MIN = 100
BUDGET_MAX = 50000
DEFAULT_BUDGET_OPTIONS = [500, 800, 1000, 1500, 2000, 3000, 5000]
DEFAULT_CRAVING_OPTIONS = [
  "Spicy",
  "Butter Chicken",
  "Biryani",
  "Pizza",
  "Dosa",
  "Momos",
  "Kebab",
  "Paneer",
  "Chinese",
  "South Indian",
  "North Indian",
  "Desserts",
  "Street Food",
  "BBQ",
  "Seafood",
]


class UserPreferences(BaseModel):
  """Typed user input for restaurant search."""

  location: str
  budget: int = Field(
    ...,
    ge=BUDGET_MIN,
    le=BUDGET_MAX,
    description="Maximum budget in INR",
  )
  cuisine: Optional[Union[str, List[str]]] = None
  cravings: Optional[List[str]] = None
  min_rating: float = Field(default=0.0, ge=0.0, le=5.0)
  extras: Optional[str] = None

  @field_validator("location")
  @classmethod
  def location_not_blank(cls, value: str) -> str:
    normalized = value.strip()
    if not normalized:
      raise ValueError("location is required")
    return normalized

  @field_validator("budget", mode="before")
  @classmethod
  def coerce_budget(cls, value: object) -> int:
    if isinstance(value, bool):
      raise ValueError("budget must be a number")
    try:
      amount = int(value)
    except (TypeError, ValueError) as exc:
      raise ValueError("budget must be a number") from exc
    return amount

  @field_validator("cuisine", mode="before")
  @classmethod
  def normalize_cuisine(
    cls, value: Optional[Union[str, List[str]]]
  ) -> Optional[Union[str, List[str]]]:
    if value is None:
      return None
    if isinstance(value, str):
      stripped = value.strip()
      return stripped or None
    return [item.strip() for item in value if item.strip()] or None

  @field_validator("cravings", mode="before")
  @classmethod
  def normalize_cravings(cls, value: Optional[Union[str, List[str]]]) -> Optional[List[str]]:
    if value is None:
      return None
    if isinstance(value, str):
      value = [value]
    cleaned = [str(item).strip() for item in value if str(item).strip()]
    return cleaned or None
