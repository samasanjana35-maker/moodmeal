from typing import Any, Dict, List, Optional

from phase0.fixtures.mock_data import MOCK_PREFERENCES
from phase0.models.preferences import UserPreferences
from phase2.builder import build_preferences
from phase2.validator import validate_raw_preferences


def collect_preferences(data: Optional[Dict[str, Any]] = None) -> UserPreferences:
  """Build preferences from form data, or return mock data for the dev harness."""
  if data is None:
    return MOCK_PREFERENCES.model_copy()
  return build_preferences(data)


def validate_preferences(data: Dict[str, Any]) -> List[str]:
  """Validate raw preference input without building the model."""
  return validate_raw_preferences(data)
