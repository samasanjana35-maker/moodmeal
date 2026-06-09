import sys

from bootstrap_path import ensure_src_on_path


def test_ensure_src_on_path_adds_src_directory():
  src = ensure_src_on_path()
  assert str(src) in sys.path
  import app.pipeline  # noqa: F401 — must resolve after bootstrap
