import logging
from typing import List, Optional

from phase0.config.settings import Settings, get_settings
from phase0.models.restaurant import Restaurant
from phase1.bundled import load_bundled_restaurants
from phase1.extractor import extract_fields
from phase1.loader import DatasetLoadError, load_raw_records
from phase1.preprocessor import preprocess_records
from phase1.store import RestaurantStore

logger = logging.getLogger(__name__)

_store: Optional[RestaurantStore] = None


def get_restaurants(settings: Optional[Settings] = None, refresh: bool = False) -> List[Restaurant]:
  """Return cleaned restaurants, loading from cache or Hugging Face as needed."""
  return load_restaurants(settings=settings, refresh=refresh)


def load_restaurants(settings: Optional[Settings] = None, refresh: bool = False) -> List[Restaurant]:
  """Load, preprocess, and cache the restaurant dataset."""
  settings = settings or get_settings()
  store = _get_store(settings)

  if refresh:
    store.clear()

  cached = store.load()
  if cached:
    return cached

  if settings.prefer_bundled_dataset:
    bundled = load_bundled_restaurants(settings.resolve_bundled_dataset_path())
    if bundled:
      logger.info(
        "Loaded %s restaurants from bundled dataset at %s",
        len(bundled),
        settings.resolve_bundled_dataset_path(),
      )
      store.save(bundled)
      return bundled

  try:
    raw_records = load_raw_records(settings)
  except DatasetLoadError:
    bundled = load_bundled_restaurants(settings.resolve_bundled_dataset_path())
    if bundled:
      logger.warning(
        "Remote dataset unavailable; using bundled fallback at %s",
        settings.resolve_bundled_dataset_path(),
      )
      store.save(bundled)
      return bundled
    raise

  if not raw_records:
    raise DatasetLoadError(
      f"Dataset '{settings.dataset_id}' returned zero records. "
      "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation"
    )

  extracted = [extract_fields(row) for row in raw_records]
  restaurants = preprocess_records(extracted)

  if not restaurants:
    raise DatasetLoadError(
      f"No valid restaurants remained after preprocessing '{settings.dataset_id}'."
    )

  store.save(restaurants)
  return restaurants


def _get_store(settings: Settings) -> RestaurantStore:
  global _store
  if _store is None:
    cache_path = settings.resolve_cache_path() if settings.use_dataset_cache else None
    _store = RestaurantStore(cache_path=cache_path)
  return _store
