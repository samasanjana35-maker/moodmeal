"""Phase 8 — Streamlit deployment (Cloud + self-hosted)."""

from phase8.bootstrap import bootstrap_environment, get_deployment_mode
from phase8.client import fetch_recommendations_via_api

__all__ = [
  "bootstrap_environment",
  "fetch_recommendations_via_api",
  "get_deployment_mode",
]
