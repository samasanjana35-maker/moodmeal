from typing import List, Optional

from pydantic import BaseModel, Field

from phase0.models.preferences import BUDGET_MAX, BUDGET_MIN


class HealthResponse(BaseModel):
  status: str = "ok"


class OptionsResponse(BaseModel):
  cities: List[str]
  areas: List[str]
  cuisines: List[str]
  locations: List[str]
  budgets: List[int]
  cravings: List[str]


class RecommendationRequest(BaseModel):
  location: str
  budget: int = Field(..., ge=BUDGET_MIN, le=BUDGET_MAX)
  cuisine: Optional[str] = None
  cravings: Optional[List[str]] = None
  min_rating: float = Field(default=0.0, ge=0.0, le=5.0)
  extras: Optional[str] = None


class ErrorResponse(BaseModel):
  detail: str
