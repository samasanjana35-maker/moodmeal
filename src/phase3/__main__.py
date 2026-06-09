"""Run Phase 3 integration standalone: python -m phase3"""

import json
import sys

from phase0.config.settings import get_settings
from phase1.pipeline import get_restaurants
from phase2.input import collect_preferences
from phase3.integration import run_integration


def main() -> int:
  settings = get_settings()
  preferences = collect_preferences()
  restaurants = get_restaurants(settings)
  result = run_integration(restaurants, preferences, settings)

  if result.empty_state:
    print(json.dumps(result.empty_state, indent=2))
    return 1

  summary = {
    "candidate_count": len(result.candidates),
    "relaxed_constraints": result.relaxed_constraints,
    "prompt_preview": result.prompt[:500] + "..." if result.prompt else None,
  }
  print(json.dumps(summary, indent=2))
  return 0


if __name__ == "__main__":
  sys.exit(main())
