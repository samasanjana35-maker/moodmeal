"""Run Phase 4 recommendation engine standalone: python -m phase4"""

import json
import sys

from phase0.config.settings import get_settings
from phase1.pipeline import get_restaurants
from phase2.input import collect_preferences
from phase3 import run_integration
from phase4 import generate_recommendations


def main() -> int:
  settings = get_settings()
  preferences = collect_preferences()
  integration = run_integration(get_restaurants(settings), preferences, settings)

  if integration.empty_state:
    print(json.dumps(integration.empty_state, indent=2))
    return 1

  result = generate_recommendations(
    integration.prompt,
    integration.candidates,
    settings=settings,
  )

  payload = {
    "fallback_used": result.fallback_used,
    "fallback_message": result.fallback_message,
    "count": len(result.recommendations),
    "recommendations": [
      {
        "rank": item.rank,
        "name": item.restaurant.name,
        "rating": item.restaurant.rating,
        "explanation": item.explanation,
      }
      for item in result.recommendations
    ],
  }
  print(json.dumps(payload, indent=2))
  return 0


if __name__ == "__main__":
  sys.exit(main())
