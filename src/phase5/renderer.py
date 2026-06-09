"""Streamlit renderer for Phase 5 output display."""

from typing import Any, Dict

import streamlit as st

from phase5.empty_state import is_empty_state


def render_results(result: Dict[str, Any]) -> None:
  """Render pipeline results in the Streamlit web UI."""
  if is_empty_state(result):
    _render_empty_state(result)
    return

  if result.get("status") != "success":
    st.error("Something went wrong while generating recommendations.")
    return

  _render_notices(result)
  recommendations = result.get("recommendations") or []
  st.success(f"Found {len(recommendations)} recommendation(s)")

  for item in recommendations:
    _render_recommendation_card(item)


def _render_empty_state(result: Dict[str, Any]) -> None:
  st.warning(result.get("message", "No restaurants matched your preferences."))
  suggestions = result.get("suggestions") or []
  if suggestions:
    st.markdown("**Try:**")
    for suggestion in suggestions:
      st.markdown(f"- {suggestion}")


def _render_notices(result: Dict[str, Any]) -> None:
  relaxed = result.get("relaxed_constraints") or []
  if relaxed:
    labels = ", ".join(relaxed)
    st.warning(f"Filters were relaxed to find results: {labels}")

  if result.get("fallback_used"):
    st.info(
      result.get(
        "fallback_message",
        "Showing rating-based fallback recommendations.",
      )
    )


def _render_recommendation_card(item: Dict[str, Any]) -> None:
  with st.container(border=True):
    rank = item.get("rank", "—")
    name = item.get("name", "Unknown")
    st.markdown(f"### #{rank} — {name}")

    area = item.get("area")
    if area:
      st.caption(f"📍 {area}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rating", item.get("rating") if item.get("rating") is not None else "—")
    col2.metric("Cost", item.get("estimated_cost") or "—")
    col3.metric("Cuisine", _shorten(item.get("cuisine") or "—", 18))

    st.markdown(f"**Cuisine:** {item.get('cuisine') or '—'}")
    st.markdown(f"**Why this pick:** {item.get('explanation') or '—'}")


def _shorten(value: str, max_len: int) -> str:
  if len(value) <= max_len:
    return value
  return value[: max_len - 1] + "…"
