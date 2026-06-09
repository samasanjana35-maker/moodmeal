"""FastAPI backend entry: uvicorn backend.api.main:app --reload --port 8000"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.errors import register_exception_handlers
from backend.api.routes import router
from backend.api.schemas import HealthResponse
from phase0.config.settings import get_settings


def create_app() -> FastAPI:
  settings = get_settings()
  application = FastAPI(
    title="Restaurant Recommendation API",
    description="Phase 6 backend for the Zomato-style AI recommendation system",
    version="1.0.0",
  )

  application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  register_exception_handlers(application)
  application.include_router(router)

  @application.get("/health", response_model=HealthResponse, tags=["health"])
  def root_health() -> HealthResponse:
    return HealthResponse()

  return application


app = create_app()
