import json
import re
from typing import Any, Dict, List


class ParseError(ValueError):
  """Raised when the LLM response cannot be parsed."""


def parse_llm_response(raw_text: str) -> List[Dict[str, Any]]:
  """Extract recommendation objects from Groq JSON output."""
  payload = _load_json_payload(raw_text)
  items = payload.get("recommendations")

  if not isinstance(items, list):
    raise ParseError("LLM response is missing a 'recommendations' list.")

  parsed: List[Dict[str, Any]] = []
  for item in items:
    if not isinstance(item, dict):
      continue
    name = str(item.get("name", "")).strip()
    if not name:
      continue
    parsed.append(
      {
        "name": name,
        "rank": item.get("rank"),
        "explanation": str(item.get("explanation", "")).strip()
        or "Recommended based on your preferences.",
      }
    )

  if not parsed:
    raise ParseError("LLM response did not contain any valid recommendations.")

  return _sort_by_rank(parsed)


def _load_json_payload(raw_text: str) -> Dict[str, Any]:
  try:
    payload = json.loads(raw_text)
    if isinstance(payload, dict):
      return payload
  except json.JSONDecodeError:
    pass

  match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
  if not match:
    raise ParseError("No JSON object found in LLM response.")

  try:
    payload = json.loads(match.group())
  except json.JSONDecodeError as exc:
    raise ParseError("Malformed JSON in LLM response.") from exc

  if not isinstance(payload, dict):
    raise ParseError("LLM JSON payload must be an object.")
  return payload


def _sort_by_rank(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
  def sort_key(item: Dict[str, Any]) -> tuple:
    rank = item.get("rank")
    try:
      return (0, int(rank))
    except (TypeError, ValueError):
      return (1, item["name"].lower())

  return sorted(items, key=sort_key)
