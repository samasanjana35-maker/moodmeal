"""Load pre-processed restaurants bundled in the repo (Streamlit Cloud fallback)."""

import json
from pathlib import Path
from typing import List, Optional

from phase0.models.restaurant import Restaurant


def load_bundled_restaurants(path: Path) -> Optional[List[Restaurant]]:
  """Load processed restaurants from a committed JSON bundle."""
  if not path.exists():
    return None

  try:
    payload = json.loads(path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError):
    return None

  if not isinstance(payload, list) or not payload:
    return None

  try:
    return [Restaurant.model_validate(item) for item in payload]
  except ValueError:
    return None
