"""Run Phase 1 ingestion standalone: python -m phase1"""

import json
import sys

from phase0.config.settings import get_settings
from phase1.pipeline import get_restaurants


def main() -> int:
  settings = get_settings()
  restaurants = get_restaurants(settings=settings)

  summary = {
    "dataset_id": settings.dataset_id,
    "total_restaurants": len(restaurants),
    "sample": restaurants[0].model_dump() if restaurants else None,
    "cities": sorted({restaurant.location for restaurant in restaurants}),
  }
  print(json.dumps(summary, indent=2))
  return 0


if __name__ == "__main__":
  sys.exit(main())
