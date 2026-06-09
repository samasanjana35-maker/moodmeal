from typing import Any, Dict, Optional

RAW_NAME_KEY = "name"
RAW_URL_KEY = "url"
RAW_ADDRESS_KEY = "address"
RAW_AREA_KEY = "location"
RAW_CUISINES_KEY = "cuisines"
RAW_COST_KEY = "approx_cost(for two people)"
RAW_RATE_KEY = "rate"


def extract_fields(row: Dict[str, Any]) -> Dict[str, Optional[str]]:
  """Map a raw dataset row to intermediate string fields."""
  return {
    "name": _clean_text(row.get(RAW_NAME_KEY)),
    "url": _clean_text(row.get(RAW_URL_KEY)),
    "address": _clean_text(row.get(RAW_ADDRESS_KEY)),
    "area": _clean_text(row.get(RAW_AREA_KEY)),
    "cuisines": _clean_text(row.get(RAW_CUISINES_KEY)),
    "cost": _clean_text(row.get(RAW_COST_KEY)),
    "rate": _clean_text(row.get(RAW_RATE_KEY)),
  }


def _clean_text(value: Any) -> Optional[str]:
  if value is None:
    return None
  text = str(value).strip()
  return text or None
