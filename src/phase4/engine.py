from dataclasses import dataclass, field
from typing import List, Optional

from phase0.config.settings import Settings, get_settings
from phase0.models.recommendation import Recommendation
from phase0.models.restaurant import Restaurant
from phase4.client import GroqAPIError
from phase4.executor import execute_prompt
from phase4.fallback import FALLBACK_MESSAGE, generate_fallback_recommendations, pad_recommendations
from phase4.guardrails import apply_guardrails
from phase4.parser import ParseError, parse_llm_response


@dataclass
class RecommendationResult:
  recommendations: List[Recommendation]
  fallback_used: bool = False
  fallback_message: Optional[str] = None
  summary: Optional[str] = None


def generate_recommendations(
  prompt: str,
  candidates: List[Restaurant],
  settings: Optional[Settings] = None,
  top_n: Optional[int] = None,
) -> RecommendationResult:
  """Send the prompt to Groq, parse the response, and return ranked recommendations."""
  settings = settings or get_settings()
  limit = top_n or settings.top_n

  if not candidates:
    return RecommendationResult(recommendations=[])

  if not settings.groq_api_key:
    return RecommendationResult(
      recommendations=generate_fallback_recommendations(candidates, limit),
      fallback_used=True,
      fallback_message=FALLBACK_MESSAGE,
    )

  try:
    raw_response = execute_prompt(prompt, settings)
    parsed_items = parse_llm_response(raw_response)
    recommendations = apply_guardrails(parsed_items, candidates)
    recommendations = pad_recommendations(recommendations, candidates, limit)

    if not recommendations:
      raise ParseError("No recommendations survived guardrails.")

    return RecommendationResult(recommendations=recommendations[:limit])

  except (GroqAPIError, ParseError):
    return RecommendationResult(
      recommendations=generate_fallback_recommendations(candidates, limit),
      fallback_used=True,
      fallback_message=FALLBACK_MESSAGE,
    )
