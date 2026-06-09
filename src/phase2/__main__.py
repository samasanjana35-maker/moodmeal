"""Launch the Phase 2 web UI: python -m phase2"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
  web_app = Path(__file__).resolve().parent / "web.py"
  command = [
    sys.executable,
    "-m",
    "streamlit",
    "run",
    str(web_app),
    "--server.headless",
    "true",
  ]
  return subprocess.call(command)


if __name__ == "__main__":
  sys.exit(main())
