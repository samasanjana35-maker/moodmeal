"""Streamlit web UI — Phase 8 deploy target (Streamlit Community Cloud)."""

from bootstrap_path import ensure_src_on_path

ensure_src_on_path()

import streamlit as st

from phase8.bootstrap import bootstrap_environment, get_backend_url, get_deployment_mode
from phase8.client import BackendAPIError, fetch_recommendations_via_api
from app.pipeline import run_pipeline
from phase0.config.settings import get_settings
from phase0.models.preferences import DEFAULT_BUDGET_OPTIONS
from phase2.builder import PreferenceValidationError, build_preferences
from phase2.options import get_form_options


@st.cache_data(show_spinner="Loading areas and cuisines…")
def _load_form_options() -> dict:
  cities, areas, cuisines, budgets, cravings = get_form_options()
  return {
    "cities": cities,
    "areas": areas or cities,
    "cuisines": cuisines,
    "budgets": budgets or DEFAULT_BUDGET_OPTIONS,
    "cravings": cravings,
  }


def _run_recommendations(preferences) -> dict:
  mode = get_deployment_mode()
  if mode == "split":
    backend_url = get_backend_url()
    if not backend_url:
      raise BackendAPIError(
        "Split deployment requires BACKEND_URL in secrets or environment.",
      )
    return fetch_recommendations_via_api(preferences, backend_url)

  return run_pipeline(get_settings(), preferences=preferences)


def main() -> None:
  bootstrap_environment()

  st.set_page_config(
    page_title="moodmeal — Restaurant Recommendations",
    page_icon="🍽️",
    layout="centered",
  )

  options = _load_form_options()
  mode = get_deployment_mode()

  st.title("moodmeal")
  st.caption("Tell us your mood and our AI will pick the perfect spot for you.")

  with st.sidebar:
    st.markdown("### Deployment")
    st.caption(f"Mode: **{mode}**")
    if mode == "split":
      st.caption(f"API: `{get_backend_url() or 'not set'}`")
    settings = get_settings()
    if not settings.groq_api_key and mode == "monolith":
      st.warning("GROQ_API_KEY not set — using rating-based fallback.")

  with st.form("preferences_form"):
    st.subheader("Your preferences")

    city = st.selectbox(
      "City",
      options=options["cities"] or ["Bangalore"],
      disabled=len(options["cities"]) <= 1,
    )

    location = st.selectbox(
      "Area *",
      options=options["areas"],
      index=0,
      help="Neighborhood to search in",
    )

    budget = st.selectbox(
      "Budget (₹) *",
      options=options["budgets"],
      index=options["budgets"].index(2000)
      if 2000 in options["budgets"]
      else 0,
      format_func=lambda value: f"₹{value:,}",
    )

    cuisine = st.selectbox(
      "Cuisine",
      options=["Any"] + options["cuisines"],
      help="Leave as Any to include all cuisines",
    )

    selected_cravings = st.multiselect(
      "Specific cravings",
      options=options["cravings"],
      help="Optional dish or flavor preferences",
    )

    min_rating = st.slider(
      "Minimum rating",
      min_value=3.0,
      max_value=5.0,
      value=3.5,
      step=0.1,
    )

    extras = st.text_area(
      "Additional preferences",
      placeholder="e.g. family-friendly, quick service, outdoor seating",
      help="Optional free-text preferences passed to the AI ranker",
    )

    submitted = st.form_submit_button("Get recommendations", type="primary")

  if not submitted:
    return

  raw_input = {
    "location": location or city,
    "budget": budget,
    "cuisine": None if cuisine == "Any" else cuisine,
    "cravings": selected_cravings or None,
    "min_rating": min_rating,
    "extras": extras,
  }

  try:
    preferences = build_preferences(raw_input)
  except PreferenceValidationError as exc:
    for error in exc.errors:
      st.error(error)
    return

  try:
    with st.spinner("Finding restaurants…"):
      result = _run_recommendations(preferences)
  except BackendAPIError as exc:
    st.error(str(exc))
    return
  except Exception:
    st.error("Something went wrong while generating recommendations.")
    return

  from phase5.renderer import render_results

  render_results(result)


if __name__ == "__main__":
  main()
