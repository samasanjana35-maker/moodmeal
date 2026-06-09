from typing import Optional

from groq import Groq

from phase0.config.settings import Settings


class GroqAPIError(RuntimeError):
  """Raised when the Groq API returns an error."""


class GroqClient:
  """Thin wrapper around the Groq chat completions API."""

  def __init__(self, settings: Settings) -> None:
    if not settings.groq_api_key:
      raise GroqAPIError(
        "GROQ_API_KEY is not set. Add it to your .env file to enable AI recommendations."
      )
    self._client = Groq(api_key=settings.groq_api_key, timeout=settings.llm_timeout_seconds)
    self._model = settings.llm_model

  def complete(self, prompt: str) -> str:
    """Send a prompt to Groq and return the assistant message content."""
    try:
      response = self._client.chat.completions.create(
        model=self._model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},
      )
    except Exception as exc:
      raise GroqAPIError(str(exc)) from exc

    content: Optional[str] = response.choices[0].message.content
    if not content or not content.strip():
      raise GroqAPIError("Groq returned an empty response.")
    return content.strip()
