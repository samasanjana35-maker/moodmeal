"""Run backend API: python -m backend"""

import uvicorn

from phase0.config.settings import get_settings


def main() -> int:
  settings = get_settings()
  uvicorn.run(
    "backend.api.main:app",
    host=settings.api_host,
    port=settings.api_port,
    reload=True,
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
