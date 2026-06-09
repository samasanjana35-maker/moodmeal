import csv
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from datasets import load_dataset

from phase0.config.settings import Settings

logger = logging.getLogger(__name__)

DATASET_URL = "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation"


class DatasetLoadError(RuntimeError):
  """Raised when the restaurant dataset cannot be loaded from any source."""


def load_raw_records(settings: Settings) -> List[Dict[str, Any]]:
  """Load raw records — local bundle first, then Hugging Face with retries."""
  local_path = settings.resolve_local_raw_dataset_path()
  if local_path.exists():
    logger.info("Loading raw dataset from local file: %s", local_path)
    return _load_local_raw_records(local_path)

  return _load_hf_records(settings)


def _load_local_raw_records(path: Path) -> List[Dict[str, Any]]:
  suffix = path.suffix.lower()
  if suffix == ".json":
    return _load_raw_json(path)
  if suffix == ".csv":
    return _load_raw_csv(path)
  if suffix == ".parquet":
    return _load_raw_parquet(path)
  raise DatasetLoadError(f"Unsupported local dataset format: {path.suffix}")


def _load_raw_json(path: Path) -> List[Dict[str, Any]]:
  try:
    payload = json.loads(path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as exc:
    raise DatasetLoadError(f"Failed to read local JSON dataset: {path}") from exc

  if not isinstance(payload, list):
    raise DatasetLoadError(f"Local JSON dataset must be a list of records: {path}")
  return [dict(row) for row in payload]


def _load_raw_csv(path: Path) -> List[Dict[str, Any]]:
  try:
    with path.open(encoding="utf-8", newline="") as handle:
      return [dict(row) for row in csv.DictReader(handle)]
  except OSError as exc:
    raise DatasetLoadError(f"Failed to read local CSV dataset: {path}") from exc


def _load_raw_parquet(path: Path) -> List[Dict[str, Any]]:
  try:
    import pyarrow.parquet as pq
  except ImportError as exc:
    raise DatasetLoadError(
      "Parquet fallback requires pyarrow. Use JSON/CSV or install pyarrow."
    ) from exc

  try:
    table = pq.read_table(path)
    return table.to_pylist()
  except Exception as exc:
    raise DatasetLoadError(f"Failed to read local Parquet dataset: {path}") from exc


def _configure_hf_auth(settings: Settings) -> None:
  token = (settings.hf_token or os.environ.get("HF_TOKEN") or "").strip()
  if not token:
    return

  try:
    from huggingface_hub import login

    login(token=token, add_to_git_credential=False)
    logger.info("Authenticated with Hugging Face Hub.")
  except Exception as exc:
    logger.warning("Hugging Face login failed: %s", exc)


def _load_hf_records(settings: Settings) -> List[Dict[str, Any]]:
  _configure_hf_auth(settings)
  os.environ.setdefault(
    "HF_HUB_DOWNLOAD_TIMEOUT",
    str(int(settings.dataset_load_timeout_seconds)),
  )

  last_error: Optional[Exception] = None
  max_retries = settings.dataset_max_retries

  for attempt in range(1, max_retries + 1):
    try:
      logger.info(
        "Loading Hugging Face dataset '%s' (attempt %s/%s)",
        settings.dataset_id,
        attempt,
        max_retries,
      )
      dataset = load_dataset(
        settings.dataset_id,
        split=settings.dataset_split,
        download_mode="reuse_dataset_if_exists",
      )
      records = [dict(row) for row in dataset]
      if records:
        return records
      raise DatasetLoadError(
        f"Dataset '{settings.dataset_id}' returned zero records."
      )
    except Exception as exc:
      last_error = exc
      logger.warning("Hugging Face load attempt %s failed: %s", attempt, exc)
      if attempt < max_retries:
        delay = settings.dataset_retry_base_seconds * attempt
        time.sleep(delay)

  bundled_hint = settings.resolve_bundled_dataset_path()
  message = (
    f"Failed to load dataset '{settings.dataset_id}' after {max_retries} attempts. "
    f"See {DATASET_URL}. "
    f"For deployment, commit bundled data at {bundled_hint} "
    "or set HF_TOKEN in secrets if the dataset requires authentication."
  )
  raise DatasetLoadError(message) from last_error
