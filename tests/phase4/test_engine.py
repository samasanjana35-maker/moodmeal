import json
from unittest.mock import patch

from phase0.config.settings import Settings
from phase0.models.restaurant import Restaurant
from phase4.client import GroqAPIError
from phase4.engine import generate_recommendations


def _candidates():
  return [
    Restaurant(name="Onesta", location="Bangalore", cuisines=["Italian"], rating=4.6),
    Restaurant(name="Truffles", location="Bangalore", cuisines=["Italian"], rating=4.3),
  ]


def test_generate_recommendations_uses_fallback_without_api_key():
  settings = Settings(groq_api_key=None, top_n=2)
  result = generate_recommendations("prompt", _candidates(), settings=settings)

  assert result.fallback_used is True
  assert len(result.recommendations) == 2
  assert result.recommendations[0].restaurant.name == "Onesta"


@patch("phase4.engine.execute_prompt")
def test_generate_recommendations_parses_groq_response(mock_execute):
  mock_execute.return_value = json.dumps(
    {
      "recommendations": [
        {"rank": 1, "name": "Truffles", "explanation": "Best Italian fit."},
      ]
    }
  )
  settings = Settings(groq_api_key="test-key", top_n=2)

  result = generate_recommendations("prompt", _candidates(), settings=settings)

  assert result.fallback_used is False
  assert result.recommendations[0].restaurant.name == "Truffles"
  assert "Italian" in result.recommendations[0].explanation or result.recommendations[0].explanation


@patch("phase4.engine.execute_prompt", side_effect=GroqAPIError("429 rate limit"))
def test_generate_recommendations_falls_back_on_api_error(mock_execute):
  settings = Settings(groq_api_key="test-key", top_n=1)
  result = generate_recommendations("prompt", _candidates(), settings=settings)

  assert result.fallback_used is True
  assert len(result.recommendations) == 1
