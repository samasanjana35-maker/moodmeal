#!/usr/bin/env python3
"""Copy processed restaurants into data/bundled/ for Streamlit Cloud deployment."""

from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = PROJECT_ROOT / "data" / "cache" / "restaurants.json"
BUNDLED_PATH = PROJECT_ROOT / "data" / "bundled" / "restaurants.json"


def main() -> int:
  if not CACHE_PATH.exists():
    print(
      "No cache found. Run `python -m phase1` once locally to warm the dataset, "
      "then re-run this script.",
      file=sys.stderr,
    )
    return 1

  BUNDLED_PATH.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(CACHE_PATH, BUNDLED_PATH)
  print(f"Bundled {BUNDLED_PATH} ({BUNDLED_PATH.stat().st_size:,} bytes)")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
