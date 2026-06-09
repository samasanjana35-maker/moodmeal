"""Streamlit Community Cloud entry point — run from repository root.

Set this file as the main script path in Streamlit Cloud (not src/app/main.py).
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
  sys.path.insert(0, str(_SRC))

from phase2.web import main

main()
