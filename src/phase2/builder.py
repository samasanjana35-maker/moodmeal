from typing import Any, Dict, List, Optional, Union

from phase0.models.preferences import UserPreferences
from phase2.validator import validate_raw_preferences


class PreferenceValidationError(ValueError):
  """Raised when user preference input fails validation."""

  def __init__(self, errors: List[str]) -> None:
    self.errors = errors
    super().__init__("; ".join(errors))


def build_preferences(data: Dict[str, Any]) -> UserPreferences:
  """Validate raw input and construct a UserPreferences object."""
  errors = validate_raw_preferences(data)
  if errors:
    raise PreferenceValidationError(errors)

  cuisine = _normalize_cuisine(data.get("cuisine"))
  cravings = _normalize_cravings(data.get("cravings"))
  extras = _as_optional_text(data.get("extras"))
  min_rating = float(data.get("min_rating") or 0.0)

  return UserPreferences(
    location=str(data["location"]).strip(),
    budget=int(data["budget"]),
    cuisine=cuisine,
    cravings=cravings,
    min_rating=min_rating,
    extras=extras,
  )


def _normalize_cuisine(value: Any) -> Optional[Union[str, List[str]]]:
  if value is None:
    return None

  if isinstance(value, list):
    cleaned = [str(item).strip() for item in value if str(item).strip()]
    return cleaned or None

  text = str(value).strip()
  return text or None


def _normalize_cravings(value: Any) -> Optional[List[str]]:
  if value is None:
    return None
  if isinstance(value, list):
    cleaned = [str(item).strip() for item in value if str(item).strip()]
    return cleaned or None
  text = str(value).strip()
  return [text] if text else None


def _as_optional_text(value: Any) -> Optional[str]:
  if value is None:
    return None
  text = str(value).strip()
  return text or None
