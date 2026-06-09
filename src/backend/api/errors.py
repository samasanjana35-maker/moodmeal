from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from phase2.builder import PreferenceValidationError


def register_exception_handlers(app: FastAPI) -> None:
  @app.exception_handler(PreferenceValidationError)
  async def preference_validation_handler(
    _request: Request,
    exc: PreferenceValidationError,
  ) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.errors})
