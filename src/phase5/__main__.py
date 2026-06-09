"""Run Phase 5 display demo: python -m phase5"""

import sys

from app.pipeline import run_pipeline
from phase0.config.settings import get_settings
from phase5.cli import render_recommendations


def main() -> int:
  result = run_pipeline(get_settings())
  render_recommendations(result)
  return 1 if result.get("status") == "no_matches" else 0


if __name__ == "__main__":
  sys.exit(main())
