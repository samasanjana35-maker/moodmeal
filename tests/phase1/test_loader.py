import json
from unittest.mock import MagicMock, patch

import pytest

from phase0.config.settings import Settings
from phase1.loader import DatasetLoadError, load_raw_records


def test_load_raw_records_from_local_json(tmp_path):
  records = [{"name": "Cafe", "location": "Indiranagar", "rate": "4.0/5"}]
  path = tmp_path / "raw_records.json"
  path.write_text(json.dumps(records), encoding="utf-8")

  settings = Settings(
    local_raw_dataset_path=str(path),
    dataset_max_retries=1,
  )

  loaded = load_raw_records(settings)
  assert loaded == records


def test_load_raw_records_retries_hf_then_raises(tmp_path):
  settings = Settings(
    local_raw_dataset_path=str(tmp_path / "missing.json"),
    dataset_max_retries=2,
    dataset_retry_base_seconds=0.01,
  )

  with patch("phase1.loader.load_dataset", side_effect=ConnectionError("timeout")):
    with pytest.raises(DatasetLoadError) as exc_info:
      load_raw_records(settings)

  message = str(exc_info.value)
  assert "after 2 attempts" in message
  assert "data/bundled/restaurants.json" in message


def test_configure_hf_auth_calls_login(monkeypatch):
  monkeypatch.setenv("HF_TOKEN", "hf_test_token")

  mock_login = MagicMock()
  with patch("huggingface_hub.login", mock_login, create=True):
    from phase1.loader import _configure_hf_auth

    _configure_hf_auth(Settings(hf_token=None))

  mock_login.assert_called_once_with(token="hf_test_token", add_to_git_credential=False)
