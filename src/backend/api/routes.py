import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from backend.api.schemas import HealthResponse, OptionsResponse, RecommendationRequest
from backend.api.service import get_recommendations
from phase2.builder import PreferenceValidationError
from phase2.options import get_form_options

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
  return HealthResponse()


@router.get("/options", response_model=OptionsResponse)
def options() -> OptionsResponse:
  cities, areas, cuisines, budgets, cravings = get_form_options()
  return OptionsResponse(
    cities=cities,
    areas=areas,
    cuisines=cuisines,
    locations=cities + areas,
    budgets=budgets,
    cravings=cravings,
  )


@router.post("/recommendations")
def recommendations(body: RecommendationRequest) -> Dict[str, Any]:
  try:
    return get_recommendations(body)
  except PreferenceValidationError:
    raise
  except Exception as exc:
    logger.exception("Recommendation pipeline failed")
    raise HTTPException(
      status_code=500,
      detail="Recommendation pipeline failed.",
    ) from exc
