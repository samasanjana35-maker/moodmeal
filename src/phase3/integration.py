from dataclasses import dataclass, field
from typing import List, Optional

from phase0.config.settings import Settings
from phase0.models.preferences import UserPreferences
from phase0.models.restaurant import Restaurant
from phase3.fallback import FilterResult, build_empty_state, filter_restaurants
from phase3.prompt import build_prompt


@dataclass
class IntegrationResult:
  candidates: List[Restaurant]
  prompt: Optional[str] = None
  empty_state: Optional[dict] = None
  relaxed_constraints: List[str] = field(default_factory=list)


def run_integration(
  restaurants: List[Restaurant],
  prefs: UserPreferences,
  settings: Settings,
) -> IntegrationResult:
  """Run Phase 3 filtering and prompt construction."""
  filter_result = filter_restaurants(restaurants, prefs, settings)

  if not filter_result.candidates:
    return IntegrationResult(
      candidates=[],
      empty_state=build_empty_state(prefs, settings),
    )

  prompt = build_prompt(prefs, filter_result.candidates, settings)
  return IntegrationResult(
    candidates=filter_result.candidates,
    prompt=prompt,
    relaxed_constraints=filter_result.relaxed_constraints,
  )
