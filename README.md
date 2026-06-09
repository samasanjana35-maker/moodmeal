# MILESTONE

AI-powered restaurant recommendation system (Zomato dataset + Groq LLM).

## Project layout

```
MILESTONE/
├── src/                    # Python backend
│   ├── phase0/             # Shared models & config
│   ├── phase1/             # Data ingestion
│   ├── phase2/             # Input validation & Streamlit (legacy UI)
│   ├── phase3/             # Filter & prompt integration
│   ├── phase4/             # Groq recommendation engine
│   ├── phase5/             # Response formatting
│   ├── app/                # Pipeline orchestrator
│   ├── backend/            # FastAPI REST API (Phase 6)
│   └── phase8/             # Streamlit deployment (Phase 8)
├── .streamlit/             # Streamlit Cloud config + secrets example
├── frontend/               # Next.js web app (Phase 7)
├── requirements.txt        # Streamlit Community Cloud dependencies
├── tests/                  # pytest suite
├── scripts/                # Dev utilities
├── docs/                   # Documentation & design assets
└── data/cache/             # Restaurant JSON cache (generated)
```

## Quick start

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Data (first time)
python -m phase1

# Backend API
python -m backend

# Frontend (separate terminal)
cd frontend && npm install && npm run dev

# Streamlit deploy app (Phase 8)
python -m phase8
```

- API: http://localhost:8000/docs
- Web UI (Next.js): http://localhost:3000
- Streamlit (Phase 8): http://localhost:8501

## Deploy (Phase 8 — Streamlit Cloud)

```bash
# Pre-deploy check
python scripts/deploy_check.py

# Warm dataset cache (recommended before first Cloud deploy)
python -m phase1

# Run locally
python -m phase8
```

**Streamlit Community Cloud settings:**

| Setting | Value |
|---------|-------|
| Main file | `src/phase2/web.py` |
| Python | 3.9+ |
| Install | `pip install -r requirements.txt` or `pip install -e .` |

Add secrets from [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) (`GROQ_API_KEY` required for AI explanations).

**Split mode** (optional): set `DEPLOYMENT_MODE=split` and `BACKEND_URL` in secrets when API runs on a separate host.

## Documentation

| Doc | Path |
|-----|------|
| Problem statement | [docs/requirements/problemstatement.md](docs/requirements/problemstatement.md) |
| Architecture | [docs/architecture/architecture.md](docs/architecture/architecture.md) |
| Edge cases | [docs/requirements/edge-cases.md](docs/requirements/edge-cases.md) |
| UI design prompt | [docs/design/frontend-ui-prompt.md](docs/design/frontend-ui-prompt.md) |

## Tests

```bash
pytest
```
