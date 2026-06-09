from typing import List, Optional

from phase0.models.recommendation import Recommendation
from phase5.models import DisplayRecommendation, PipelineDisplayResponse

MISSING_EXPLANATION = "Explanation unavailable for this recommendation."


def format_recommendation(item: Recommendation) -> DisplayRecommendation:
  """Map one Recommendation to a display card with safe defaults."""
  explanation = (item.explanation or "").strip() or MISSING_EXPLANATION
  cuisines = ", ".join(item.restaurant.cuisines) if item.restaurant.cuisines else "—"

  return DisplayRecommendation(
    rank=item.rank,
    name=item.restaurant.name,
    cuisine=cuisines,
    rating=item.restaurant.rating,
    estimated_cost=item.restaurant.cost,
    area=item.restaurant.area,
    explanation=explanation,
  )


def format_response(recommendations: List[Recommendation]) -> dict:
  """Map recommendations to a JSON-serializable success response."""
  display_items = [format_recommendation(item) for item in recommendations]
  return PipelineDisplayResponse(
    status="success",
    count=len(display_items),
    recommendations=display_items,
  ).model_dump()


def format_pipeline_result(
  recommendations: Optional[List[Recommendation]] = None,
  empty_state: Optional[dict] = None,
  relaxed_constraints: Optional[List[str]] = None,
  fallback_used: bool = False,
  fallback_message: Optional[str] = None,
) -> dict:
  """Build the final pipeline response for API, CLI, or web rendering."""
  if empty_state:
    return PipelineDisplayResponse(
      status=empty_state.get("status", "no_matches"),
      message=empty_state.get("message"),
      suggestions=empty_state.get("suggestions") or [],
      recommendations=[],
    ).model_dump()

  display_items = [format_recommendation(item) for item in recommendations or []]
  return PipelineDisplayResponse(
    status="success",
    count=len(display_items),
    recommendations=display_items,
    relaxed_constraints=relaxed_constraints or [],
    fallback_used=fallback_used,
    fallback_message=fallback_message,
  ).model_dump()
