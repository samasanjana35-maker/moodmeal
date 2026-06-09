import io

from phase5.cli import render_recommendations, render_response


def test_render_response_outputs_json():
  buffer = io.StringIO()
  render_response({"status": "success", "count": 0, "recommendations": []}, stream=buffer)
  assert '"status": "success"' in buffer.getvalue()


def test_render_recommendations_human_readable():
  buffer = io.StringIO()
  result = {
    "status": "success",
    "recommendations": [
      {
        "rank": 1,
        "name": "Truffles",
        "area": "Bellandur",
        "rating": 4.3,
        "estimated_cost": "₹800 for two",
        "cuisine": "Italian",
        "explanation": "Great pasta.",
      }
    ],
  }
  render_recommendations(result, stream=buffer)
  output = buffer.getvalue()
  assert "#1 Truffles" in output
  assert "Great pasta." in output
