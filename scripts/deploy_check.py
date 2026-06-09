#!/usr/bin/env python3
"""Pre-deploy smoke check for Phase 8 (Streamlit)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
  errors: list[str] = []

  streamlit_entry = ROOT / "streamlit_app.py"
  web_app = ROOT / "src" / "phase2" / "web.py"
  if not streamlit_entry.exists():
    errors.append(f"Missing Streamlit Cloud entry: {streamlit_entry}")
  if not web_app.exists():
    errors.append(f"Missing Streamlit UI: {web_app}")

  requirements = ROOT / "requirements.txt"
  if not requirements.exists():
    errors.append("Missing requirements.txt for Streamlit Cloud")

  config = ROOT / ".streamlit" / "config.toml"
  if not config.exists():
    errors.append("Missing .streamlit/config.toml")

  settings = None
  try:
    from phase8.bootstrap import bootstrap_environment
    from phase0.config.settings import get_settings

    bootstrap_environment()
    settings = get_settings()
    if not settings.groq_api_key:
      print("WARN: GROQ_API_KEY not set — deploy will use rating fallback")
  except Exception as exc:
    errors.append(f"Bootstrap failed: {exc}")

  cache = (
    settings.resolve_cache_path()
    if settings is not None
    else ROOT / "data/cache/restaurants.json"
  )
  if not cache.exists():
    print(
      "WARN: No dataset cache — first Cloud request will download from Hugging Face. "
      "Run: python -m phase1"
    )
  else:
    print(f"OK: Dataset cache found ({cache})")

  if errors:
    for item in errors:
      print(f"ERROR: {item}")
    return 1

  print("OK: Phase 8 deploy check passed")
  print("Run locally: python -m phase8")
  print("Streamlit Cloud main file: streamlit_app.py")
  return 0


if __name__ == "__main__":
  sys.exit(main())
