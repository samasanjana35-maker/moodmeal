#!/usr/bin/env python3
"""Live Phase 4 example: Bellandur, high budget (~₹2000), rating 4.0+, top 5."""

import json
import sys

from phase0.config.settings import get_settings
from phase0.models.preferences import UserPreferences
from phase1.pipeline import get_restaurants
from phase3 import run_integration
from phase4 import generate_recommendations


def main() -> int:
  prefs = UserPreferences(
    location="Bellandur",
    budget=2000,
    min_rating=4.0,
  )
  settings = get_settings()
  settings = settings.model_copy(update={"top_n": 5})

  if not settings.groq_api_key:
    print("Error: GROQ_API_KEY is not set. Add it to .env and retry.", file=sys.stderr)
    return 1

  restaurants = get_restaurants(settings)
  integration = run_integration(restaurants, prefs, settings)

  if integration.empty_state:
    print(json.dumps(integration.empty_state, indent=2))
    return 1

  print(f"Filtered {len(integration.candidates)} candidates in Bellandur (rating ≥ 4.0, budget ≤ ₹2000)\n")

  result = generate_recommendations(
    integration.prompt,
    integration.candidates,
    settings=settings,
    top_n=5,
  )

  if result.fallback_used:
    print(f"Note: {result.fallback_message}\n")

  output = {
    "query": {
      "location": "Bellandur",
      "budget": 2000,
      "min_rating": 4.0,
      "top_n": 5,
    },
    "fallback_used": result.fallback_used,
    "recommendations": [
      {
        "rank": item.rank,
        "name": item.restaurant.name,
        "area": item.restaurant.area,
        "rating": item.restaurant.rating,
        "estimated_cost": item.restaurant.cost,
        "cuisine": ", ".join(item.restaurant.cuisines),
        "explanation": item.explanation,
      }
      for item in result.recommendations
    ],
  }
  print(json.dumps(output, indent=2))
  return 0


if __name__ == "__main__":
  sys.exit(main())
