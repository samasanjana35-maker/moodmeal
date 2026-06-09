import json
import sys
from typing import Any, Dict, TextIO


def render_response(result: Dict[str, Any], stream: TextIO = sys.stdout) -> None:
  """Print the pipeline response as formatted JSON for CLI/API consumers."""
  print(json.dumps(result, indent=2), file=stream)


def render_recommendations(result: Dict[str, Any], stream: TextIO = sys.stdout) -> None:
  """Human-readable CLI output for successful recommendations."""
  if result.get("status") != "success":
    render_response(result, stream=stream)
    return

  if result.get("fallback_used"):
    print(result.get("fallback_message", ""), file=stream)
    print(file=stream)

  for item in result.get("recommendations") or []:
    print(f"#{item.get('rank')} {item.get('name')}", file=stream)
    if item.get("area"):
      print(f"   Area: {item.get('area')}", file=stream)
    print(f"   Rating: {item.get('rating', '—')} | Cost: {item.get('estimated_cost', '—')}", file=stream)
    print(f"   Cuisine: {item.get('cuisine', '—')}", file=stream)
    print(f"   Why: {item.get('explanation', '—')}", file=stream)
    print(file=stream)
