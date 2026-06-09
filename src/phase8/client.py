"""HTTP client for split deployment — Streamlit UI calling Phase 6 API."""

from typing import Any, Dict, Optional

import urllib.error
import urllib.request
import json

from phase0.models.preferences import UserPreferences


class BackendAPIError(RuntimeError):
  """Raised when the recommendation API returns an error."""

  def __init__(self, message: str, status_code: Optional[int] = None) -> None:
    self.status_code = status_code
    super().__init__(message)


def _preferences_to_body(prefs: UserPreferences) -> Dict[str, Any]:
  body: Dict[str, Any] = {
    "location": prefs.location,
    "budget": prefs.budget,
    "min_rating": prefs.min_rating,
  }
  if prefs.cuisine:
    body["cuisine"] = prefs.cuisine
  if prefs.cravings:
    body["cravings"] = prefs.cravings
  if prefs.extras:
    body["extras"] = prefs.extras
  return body


def fetch_recommendations_via_api(
  preferences: UserPreferences,
  backend_url: str,
  timeout_seconds: float = 60.0,
) -> Dict[str, Any]:
  """POST preferences to Phase 6 and return the pipeline JSON response."""
  url = f"{backend_url.rstrip('/')}/api/v1/recommendations"
  payload = json.dumps(_preferences_to_body(preferences)).encode("utf-8")
  request = urllib.request.Request(
    url,
    data=payload,
    headers={
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    method="POST",
  )

  try:
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
      return json.loads(response.read().decode("utf-8"))
  except urllib.error.HTTPError as exc:
    detail = exc.read().decode("utf-8", errors="replace")
    raise BackendAPIError(
      f"Recommendation API failed ({exc.code}): {detail}",
      status_code=exc.code,
    ) from exc
  except urllib.error.URLError as exc:
    raise BackendAPIError(
      f"Could not reach recommendation API at {backend_url}. "
      "Check BACKEND_URL and that the API is running.",
    ) from exc
