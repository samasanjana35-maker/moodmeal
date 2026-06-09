"""Load Streamlit Cloud secrets and deployment settings before the pipeline runs."""

import os
from typing import Literal, Optional

DeploymentMode = Literal["monolith", "split"]

_SECRET_KEYS = (
  "GROQ_API_KEY",
  "LLM_MODEL",
  "USE_DATASET_CACHE",
  "DATA_CACHE_DIR",
  "BACKEND_URL",
  "DEPLOYMENT_MODE",
)


def _read_streamlit_secrets() -> dict:
  try:
    import streamlit as st
  except ImportError:
    return {}

  try:
    return dict(st.secrets)
  except Exception:
    return {}


def _apply_secret(key: str, value: object) -> None:
  if value is None:
    return
  text = str(value).strip()
  if text:
    os.environ.setdefault(key, text)


def bootstrap_environment() -> None:
  """Map Streamlit secrets and deployment env vars into ``os.environ``.

  Call once at app startup before ``get_settings()`` is first used.
  """
  for key in _SECRET_KEYS:
    env_value = os.environ.get(key)
    if env_value:
      continue
    secrets = _read_streamlit_secrets()
    if key in secrets:
      _apply_secret(key, secrets[key])

  from phase0.config.settings import refresh_settings

  refresh_settings()


def get_deployment_mode() -> DeploymentMode:
  """Return ``monolith`` (in-process pipeline) or ``split`` (HTTP API)."""
  mode = os.environ.get("DEPLOYMENT_MODE", "monolith").strip().lower()
  backend_url = os.environ.get("BACKEND_URL", "").strip()
  if mode == "split" or backend_url:
    return "split"
  return "monolith"


def get_backend_url() -> Optional[str]:
  url = os.environ.get("BACKEND_URL", "").strip().rstrip("/")
  return url or None
