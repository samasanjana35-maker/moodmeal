"""Add ``src/`` to ``sys.path`` so ``app``, ``phase0``, etc. resolve on Streamlit Cloud."""

import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parent


def ensure_src_on_path() -> Path:
  """Insert the ``src`` directory at the front of ``sys.path`` if needed."""
  root = str(_SRC_ROOT)
  if root not in sys.path:
    sys.path.insert(0, root)
  return _SRC_ROOT
