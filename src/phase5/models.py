from typing import List, Optional

from pydantic import BaseModel, Field


class DisplayRecommendation(BaseModel):
  """User-facing recommendation card — facts from dataset, explanation from LLM."""

  rank: int = Field(ge=1)
  name: str
  cuisine: str
  rating: Optional[float] = None
  estimated_cost: Optional[str] = None
  area: Optional[str] = None
  explanation: Optional[str] = None


class PipelineDisplayResponse(BaseModel):
  """Normalized API/CLI response for the full pipeline."""

  status: str
  count: int = 0
  recommendations: List[DisplayRecommendation] = Field(default_factory=list)
  message: Optional[str] = None
  suggestions: List[str] = Field(default_factory=list)
  relaxed_constraints: List[str] = Field(default_factory=list)
  fallback_used: bool = False
  fallback_message: Optional[str] = None
