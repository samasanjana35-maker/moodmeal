"""Dev CLI harness — runs the pipeline with mock input.

Primary user input is the basic web UI (Phase 2). Use this module only for
local development and automated tests.
"""

import sys

from bootstrap_path import ensure_src_on_path

ensure_src_on_path()

from app.pipeline import run_pipeline
from phase0.config.settings import get_settings
from phase5 import render_response


def main() -> int:
  settings = get_settings()
  result = run_pipeline(settings)
  render_response(result)

  if result.get("status") == "no_matches":
    return 1
  return 0


if __name__ == "__main__":
  sys.exit(main())
