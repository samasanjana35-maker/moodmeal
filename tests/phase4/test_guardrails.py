from phase0.models.restaurant import Restaurant
from phase4.guardrails import apply_guardrails


def test_apply_guardrails_drops_hallucinated_names():
  candidates = [
    Restaurant(name="Truffles", location="Bangalore", cuisines=["Italian"], rating=4.3),
  ]
  parsed = [
    {"name": "Truffles", "explanation": "Real match."},
    {"name": "Fake Place", "explanation": "Hallucinated."},
  ]

  result = apply_guardrails(parsed, candidates)
  assert len(result) == 1
  assert result[0].restaurant.name == "Truffles"


def test_apply_guardrails_case_insensitive_match():
  candidates = [
    Restaurant(name="Barbeque Nation", location="Bangalore", cuisines=["BBQ"], rating=4.5),
  ]
  parsed = [{"name": "barbeque nation", "explanation": "BBQ night."}]

  result = apply_guardrails(parsed, candidates)
  assert result[0].restaurant.name == "Barbeque Nation"


def test_apply_guardrails_deduplicates_names():
  candidates = [
    Restaurant(name="Truffles", location="Bangalore", cuisines=["Italian"], rating=4.3),
  ]
  parsed = [
    {"name": "Truffles", "explanation": "First"},
    {"name": "truffles", "explanation": "Duplicate"},
  ]

  result = apply_guardrails(parsed, candidates)
  assert len(result) == 1
