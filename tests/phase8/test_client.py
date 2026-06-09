import json
from unittest.mock import MagicMock, patch

import pytest

from phase0.models.preferences import UserPreferences
from phase8.client import BackendAPIError, fetch_recommendations_via_api


def test_fetch_recommendations_via_api_success():
  prefs = UserPreferences(location="Indiranagar", budget=2000, min_rating=3.5)
  payload = {"status": "success", "count": 1, "recommendations": []}
  response = MagicMock()
  response.read.return_value = json.dumps(payload).encode("utf-8")
  response.__enter__ = MagicMock(return_value=response)
  response.__exit__ = MagicMock(return_value=False)

  with patch("phase8.client.urllib.request.urlopen", return_value=response):
    result = fetch_recommendations_via_api(prefs, "http://localhost:8000")

  assert result["status"] == "success"


def test_fetch_recommendations_via_api_http_error():
  import urllib.error

  prefs = UserPreferences(location="Indiranagar", budget=2000)
  error = urllib.error.HTTPError(
    url="http://localhost:8000/api/v1/recommendations",
    code=500,
    msg="Server Error",
    hdrs=None,
    fp=MagicMock(read=MagicMock(return_value=b'{"detail":"fail"}')),
  )

  with patch("phase8.client.urllib.request.urlopen", side_effect=error):
    with pytest.raises(BackendAPIError) as exc_info:
      fetch_recommendations_via_api(prefs, "http://localhost:8000")

  assert exc_info.value.status_code == 500
