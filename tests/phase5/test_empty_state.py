from phase5.empty_state import build_empty_state, is_empty_state


def test_build_empty_state():
  result = build_empty_state("No restaurants found.")
  assert result["status"] == "no_matches"
  assert result["message"] == "No restaurants found."
  assert len(result["suggestions"]) > 0


def test_is_empty_state():
  assert is_empty_state({"status": "no_matches"}) is True
  assert is_empty_state({"status": "success"}) is False
