from phase0.models.recommendation import Recommendation
from phase0.models.restaurant import Restaurant
from phase5.formatter import format_pipeline_result, format_recommendation, format_response


def test_format_recommendation_includes_all_fields():
  item = Recommendation(
    restaurant=Restaurant(
      name="Truffles",
      location="Bangalore",
      area="Bellandur",
      cuisines=["Italian", "American"],
      cost="₹800 for two",
      rating=4.3,
    ),
    explanation="Great Italian spot.",
    rank=1,
  )
  display = format_recommendation(item)
  assert display.name == "Truffles"
  assert display.cuisine == "Italian, American"
  assert display.rating == 4.3
  assert display.estimated_cost == "₹800 for two"
  assert display.area == "Bellandur"
  assert display.explanation == "Great Italian spot."


def test_format_recommendation_handles_missing_explanation():
  item = Recommendation(
    restaurant=Restaurant(name="Test", location="Bangalore"),
    explanation="",
    rank=1,
  )
  display = format_recommendation(item)
  assert display.explanation == "Explanation unavailable for this recommendation."


def test_format_pipeline_result_success():
  item = Recommendation(
    restaurant=Restaurant(name="A", location="Bangalore", cuisines=["Indian"], rating=4.0),
    explanation="Nice place.",
    rank=1,
  )
  result = format_pipeline_result(
    recommendations=[item],
    relaxed_constraints=["cuisine"],
    fallback_used=True,
    fallback_message="Fallback",
  )
  assert result["status"] == "success"
  assert result["count"] == 1
  assert result["relaxed_constraints"] == ["cuisine"]
  assert result["fallback_used"] is True


def test_format_pipeline_result_empty_state():
  result = format_pipeline_result(
    empty_state={"status": "no_matches", "message": "No luck", "suggestions": ["Try again"]},
  )
  assert result["status"] == "no_matches"
  assert result["message"] == "No luck"
  assert result["recommendations"] == []


def test_format_response_backward_compatible():
  item = Recommendation(
    restaurant=Restaurant(name="A", location="Bangalore", cuisines=["Indian"], rating=4.0),
    explanation="Good.",
    rank=1,
  )
  result = format_response([item])
  assert result["status"] == "success"
  assert result["recommendations"][0]["name"] == "A"
