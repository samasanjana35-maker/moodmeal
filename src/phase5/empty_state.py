from typing import List, Optional

from phase5.models import PipelineDisplayResponse

DEFAULT_SUGGESTIONS = [
  "Try a different location",
  "Relax your budget constraint",
  "Lower the minimum rating",
  "Remove or broaden cuisine preference",
]


def build_empty_state(message: str, suggestions: Optional[List[str]] = None) -> dict:
  """Build a no-matches response payload."""
  return PipelineDisplayResponse(
    status="no_matches",
    message=message,
    suggestions=suggestions or DEFAULT_SUGGESTIONS,
    recommendations=[],
  ).model_dump()


def is_empty_state(result: dict) -> bool:
  return result.get("status") == "no_matches"
