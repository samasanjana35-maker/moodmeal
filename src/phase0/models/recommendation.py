from pydantic import BaseModel, Field

from phase0.models.restaurant import Restaurant


class Recommendation(BaseModel):
  """Final output shape: restaurant facts plus AI-generated explanation."""

  restaurant: Restaurant
  explanation: str
  rank: int = Field(ge=1)
