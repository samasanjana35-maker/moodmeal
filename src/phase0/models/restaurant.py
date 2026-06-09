from typing import List, Optional

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
  """Normalized restaurant record from the dataset."""

  name: str
  location: str
  area: Optional[str] = None
  cuisines: List[str] = Field(default_factory=list)
  cost: Optional[str] = None
  budget_tier: Optional[str] = None
  rating: Optional[float] = None
