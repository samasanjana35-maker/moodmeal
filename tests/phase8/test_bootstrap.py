import os

import pytest

from phase8.bootstrap import bootstrap_environment, get_deployment_mode, get_backend_url


def test_get_deployment_mode_defaults_to_monolith(monkeypatch):
  monkeypatch.delenv("DEPLOYMENT_MODE", raising=False)
  monkeypatch.delenv("BACKEND_URL", raising=False)
  assert get_deployment_mode() == "monolith"


def test_get_deployment_mode_split_when_backend_url_set(monkeypatch):
  monkeypatch.delenv("DEPLOYMENT_MODE", raising=False)
  monkeypatch.setenv("BACKEND_URL", "http://localhost:8000")
  assert get_deployment_mode() == "split"
  assert get_backend_url() == "http://localhost:8000"


def test_bootstrap_environment_reads_env(monkeypatch):
  monkeypatch.setenv("GROQ_API_KEY", "test-key")
  bootstrap_environment()
  from phase0.config.settings import get_settings

  assert get_settings().groq_api_key == "test-key"
