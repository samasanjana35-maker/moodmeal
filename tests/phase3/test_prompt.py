import json

from phase0.config.settings import Settings
from phase0.models.preferences import UserPreferences
from phase0.models.restaurant import Restaurant
from phase3.prompt import build_prompt


def test_build_prompt_includes_system_user_candidates_and_task():
  prefs = UserPreferences(location="Bangalore", budget=1000, cuisine="Italian")
  candidates = [
    Restaurant(
      name='Cafe "Delight"',
      location="Bangalore",
      cuisines=["Italian"],
      cost="₹800 for two",
      rating=4.3,
    )
  ]
  settings = Settings(top_n=3)

  prompt = build_prompt(prefs, candidates, settings)

  assert "You are a helpful restaurant recommendation assistant" in prompt
  assert "Do NOT merely restate rating" in prompt
  assert "Make every explanation unique" in prompt
  assert "USER PREFERENCES:" in prompt
  assert "CANDIDATES" in prompt
  assert "Rank the top 1 restaurants" in prompt
  assert "Cafe" in prompt and "Delight" in prompt


def test_build_prompt_rejects_empty_candidates():
  prefs = UserPreferences(location="Bangalore", budget=500)
  try:
    build_prompt(prefs, [], Settings())
    assert False, "expected ValueError"
  except ValueError:
    pass


def test_build_prompt_serializes_valid_json_sections():
  prefs = UserPreferences(location="Bangalore", budget=500, extras="family-friendly")
  candidates = [Restaurant(name="Test", location="Bangalore", cuisines=["Indian"], rating=4.0)]
  prompt = build_prompt(prefs, candidates, Settings(top_n=1))

  preferences_block = prompt.split("USER PREFERENCES:\n", 1)[1].split("\n\nCANDIDATES", 1)[0]
  candidates_block = prompt.split("CANDIDATES (recommend only from this list):\n", 1)[1].split("\n\nTASK:", 1)[0]

  json.loads(preferences_block)
  json.loads(candidates_block)
