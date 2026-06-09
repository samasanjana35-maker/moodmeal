from typing import Any, Dict, List, Optional

from phase0.models.preferences import BUDGET_MAX, BUDGET_MIN


def validate_raw_preferences(data: Dict[str, Any]) -> List[str]:
  """Return human-readable validation errors for raw form input."""
  errors: List[str] = []

  location = _as_text(data.get("location"))
  if not location:
    errors.append("Location is required.")

  budget_error = _validate_budget(data.get("budget"))
  if budget_error:
    errors.append(budget_error)

  min_rating_error = _validate_min_rating(data.get("min_rating"))
  if min_rating_error:
    errors.append(min_rating_error)

  return errors


def _validate_budget(value: Any) -> Optional[str]:
  if value is None or value == "":
    return "Budget is required."

  try:
    amount = int(value)
  except (TypeError, ValueError):
    return f"Budget must be a number between ₹{BUDGET_MIN:,} and ₹{BUDGET_MAX:,}."

  if amount < BUDGET_MIN or amount > BUDGET_MAX:
    return f"Budget must be between ₹{BUDGET_MIN:,} and ₹{BUDGET_MAX:,}."

  return None


def _validate_min_rating(value: Any) -> Optional[str]:
  if value is None or value == "":
    return None

  try:
    rating = float(value)
  except (TypeError, ValueError):
    return "Minimum rating must be a number."

  if rating < 0 or rating > 5:
    return "Minimum rating must be between 0 and 5."

  return None


def _as_text(value: Any) -> str:
  if value is None:
    return ""
  return str(value).strip()
