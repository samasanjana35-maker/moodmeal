import json

import pytest

from phase0.config.settings import Settings
from phase0.models.restaurant import Restaurant
import phase1.pipeline as pipeline_module


@pytest.fixture(autouse=True)
def reset_store():
  pipeline_module._store = None
  yield
  pipeline_module._store = None


def test_load_restaurants_uses_bundled_without_hf(tmp_path):
  bundled_path = tmp_path / "bundled.json"
  restaurant = Restaurant(
    name="Bundled Spot",
    location="Bangalore",
    area="Indiranagar",
    cuisines=["South Indian"],
    cost="₹500 for two",
    budget_tier="low",
    rating=4.0,
  )
  bundled_path.write_text(json.dumps([restaurant.model_dump()]), encoding="utf-8")

  settings = Settings(
    bundled_dataset_path=str(bundled_path),
    prefer_bundled_dataset=True,
    use_dataset_cache=False,
  )

  loaded = pipeline_module.load_restaurants(settings=settings)
  assert len(loaded) == 1
  assert loaded[0].name == "Bundled Spot"
