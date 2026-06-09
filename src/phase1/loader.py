import time
from typing import Any, Dict, List, Optional

from datasets import load_dataset

from phase0.config.settings import Settings

DATASET_URL = "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


class DatasetLoadError(RuntimeError):
  """Raised when the Hugging Face dataset cannot be loaded."""


def load_raw_records(settings: Settings) -> List[Dict[str, Any]]:
  """Fetch raw restaurant records from Hugging Face with retries."""
  last_error: Optional[Exception] = None

  for attempt in range(1, MAX_RETRIES + 1):
    try:
      dataset = load_dataset(settings.dataset_id, split=settings.dataset_split)
      return [dict(row) for row in dataset]
    except Exception as exc:
      last_error = exc
      if attempt < MAX_RETRIES:
        time.sleep(RETRY_DELAY_SECONDS * attempt)

  message = (
    f"Failed to load dataset '{settings.dataset_id}' after {MAX_RETRIES} attempts. "
    f"See {DATASET_URL}"
  )
  raise DatasetLoadError(message) from last_error
