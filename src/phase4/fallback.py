from typing import List, Optional

from phase0.models.recommendation import Recommendation
from phase0.models.restaurant import Restaurant

FALLBACK_MESSAGE = (
  "AI recommendations are temporarily unavailable. Showing top-rated matches instead."
)


def generate_fallback_recommendations(
  candidates: List[Restaurant],
  top_n: int,
  message: Optional[str] = None,
) -> List[Recommendation]:
  """Rule-based ranking when Groq is unavailable or returns unusable output."""
  ranked = sorted(
    candidates,
    key=lambda restaurant: restaurant.rating or 0.0,
    reverse=True,
  )

  return [
    Recommendation(
      restaurant=restaurant,
      explanation=message or FALLBACK_MESSAGE,
      rank=index,
    )
    for index, restaurant in enumerate(ranked[:top_n], start=1)
  ]


def pad_recommendations(
  recommendations: List[Recommendation],
  candidates: List[Restaurant],
  top_n: int,
) -> List[Recommendation]:
  """Fill remaining slots with highest-rated candidates not already recommended."""
  if len(recommendations) >= top_n:
    return recommendations[:top_n]

  used_names = {item.restaurant.name.strip().lower() for item in recommendations}
  remaining = [
    restaurant
    for restaurant in sorted(
      candidates,
      key=lambda item: item.rating or 0.0,
      reverse=True,
    )
    if restaurant.name.strip().lower() not in used_names
  ]

  padded = list(recommendations)
  for restaurant in remaining:
    if len(padded) >= top_n:
      break
    padded.append(
      Recommendation(
        restaurant=restaurant,
        explanation="Added based on rating to complete your top picks.",
        rank=len(padded) + 1,
      )
    )
  return padded
