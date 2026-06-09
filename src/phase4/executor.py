import time
from typing import Optional

from phase0.config.settings import Settings
from phase4.client import GroqAPIError, GroqClient


def execute_prompt(prompt: str, settings: Settings) -> str:
  """Execute an LLM prompt with retries for transient Groq failures."""
  client = GroqClient(settings)
  last_error: Optional[Exception] = None
  max_attempts = settings.llm_max_retries + 1

  for attempt in range(1, max_attempts + 1):
    try:
      return client.complete(prompt)
    except GroqAPIError as exc:
      last_error = exc
      if attempt >= max_attempts or not _is_retryable(str(exc)):
        raise
      time.sleep(2 ** attempt)

  raise GroqAPIError(str(last_error))


def _is_retryable(message: str) -> bool:
  lowered = message.lower()
  return any(token in lowered for token in ("429", "rate limit", "timeout", "503", "502", "500"))
