import json
from pathlib import Path
from typing import List, Optional

from phase0.models.restaurant import Restaurant


class RestaurantStore:
  """In-memory store with optional JSON cache on disk."""

  def __init__(self, cache_path: Optional[Path] = None) -> None:
    self._cache_path = cache_path
    self._restaurants: Optional[List[Restaurant]] = None

  def load(self) -> Optional[List[Restaurant]]:
    if self._restaurants is not None:
      return self._restaurants

    if self._cache_path and self._cache_path.exists():
      self._restaurants = self._read_cache(self._cache_path)
      return self._restaurants

    return None

  def save(self, restaurants: List[Restaurant]) -> None:
    self._restaurants = restaurants
    if self._cache_path:
      self._cache_path.parent.mkdir(parents=True, exist_ok=True)
      payload = [restaurant.model_dump() for restaurant in restaurants]
      self._cache_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

  def get(self) -> List[Restaurant]:
    if self._restaurants is None:
      raise RuntimeError("Restaurant store is empty. Call save() or load() first.")
    return self._restaurants

  def clear(self) -> None:
    self._restaurants = None
    if self._cache_path and self._cache_path.exists():
      self._cache_path.unlink()

  @staticmethod
  def _read_cache(cache_path: Path) -> List[Restaurant]:
    try:
      payload = json.loads(cache_path.read_text(encoding="utf-8"))
      return [Restaurant.model_validate(item) for item in payload]
    except (json.JSONDecodeError, OSError, ValueError):
      cache_path.unlink(missing_ok=True)
      return []
