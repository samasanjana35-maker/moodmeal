"""Launch Streamlit deploy app: python -m phase8"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
  web_app = Path(__file__).resolve().parents[1] / "phase2" / "web.py"
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
