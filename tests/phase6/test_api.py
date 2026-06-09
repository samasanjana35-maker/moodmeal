from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.api.main import create_app


@pytest.fixture
def client():
  return TestClient(create_app())


def test_root_health(client):
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json() == {"status": "ok"}


def test_api_v1_health(client):
  response = client.get("/api/v1/health")
  assert response.status_code == 200
  assert response.json() == {"status": "ok"}


def test_options_returns_locations_and_cuisines(client):
  response = client.get("/api/v1/options")
  assert response.status_code == 200
  payload = response.json()
  assert "cities" in payload
  assert "areas" in payload
  assert "locations" in payload
  assert "cuisines" in payload
  assert isinstance(payload["areas"], list)
  assert isinstance(payload["cuisines"], list)
  assert len(payload["areas"]) > 0
  assert "Bellandur" in payload["areas"]
  assert "budgets" in payload
  assert 2000 in payload["budgets"]
  assert "cravings" in payload
  assert "Biryani" in payload["cravings"]


def test_recommendations_missing_location_returns_422(client):
  response = client.post("/api/v1/recommendations", json={"budget": 500})
  assert response.status_code == 422


def test_recommendations_invalid_budget_returns_422(client):
  response = client.post(
    "/api/v1/recommendations",
    json={"location": "Bangalore", "budget": 10},
  )
  assert response.status_code == 422


def test_recommendations_blank_location_returns_422(client):
  response = client.post(
    "/api/v1/recommendations",
    json={"location": "   ", "budget": 1000},
  )
  assert response.status_code == 422
  assert "detail" in response.json()


@patch("backend.api.service.run_pipeline")
def test_recommendations_success_shape(mock_pipeline, client):
  mock_pipeline.return_value = {
    "status": "success",
    "count": 1,
    "recommendations": [
      {
        "rank": 1,
        "name": "Test Restaurant",
        "cuisine": "Indian",
        "rating": 4.5,
        "estimated_cost": "₹500 for two",
        "area": "Bellandur",
        "explanation": "Great food.",
      }
    ],
    "fallback_used": False,
    "relaxed_constraints": [],
  }

  response = client.post(
    "/api/v1/recommendations",
    json={
      "location": "Bellandur",
      "budget": 2000,
      "cuisine": "Indian",
      "min_rating": 4.0,
    },
  )

  assert response.status_code == 200
  payload = response.json()
  assert payload["status"] == "success"
  assert payload["count"] == 1
  assert payload["recommendations"][0]["name"] == "Test Restaurant"
  mock_pipeline.assert_called_once()


@patch("backend.api.service.run_pipeline")
def test_recommendations_no_matches_returns_200(mock_pipeline, client):
  mock_pipeline.return_value = {
    "status": "no_matches",
    "message": "No restaurants found.",
    "suggestions": ["Try a different location"],
    "recommendations": [],
  }

  response = client.post(
    "/api/v1/recommendations",
    json={"location": "Goa", "budget": 500},
  )

  assert response.status_code == 200
  assert response.json()["status"] == "no_matches"


@patch("backend.api.service.run_pipeline", side_effect=RuntimeError("boom"))
def test_recommendations_pipeline_failure_returns_500(mock_pipeline, client):
  response = client.post(
    "/api/v1/recommendations",
    json={"location": "Bangalore", "budget": 1000},
  )

  assert response.status_code == 500
  assert response.json()["detail"] == "Recommendation pipeline failed."


def test_cors_allows_streamlit_origin(client):
  response = client.options(
    "/api/v1/recommendations",
    headers={
      "Origin": "http://localhost:8501",
      "Access-Control-Request-Method": "POST",
    },
  )
  assert response.status_code == 200
  assert response.headers.get("access-control-allow-origin") == "http://localhost:8501"
