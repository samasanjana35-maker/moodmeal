from phase0.models.preferences import UserPreferences
from phase0.models.restaurant import Restaurant

MOCK_RESTAURANTS: list[Restaurant] = [
  Restaurant(
    name="Barbeque Nation",
    location="Bangalore",
    cuisines=["North Indian", "BBQ"],
    cost="₹1,600 for two",
    budget_tier="high",
    rating=4.5,
  ),
  Restaurant(
    name="Truffles",
    location="Bangalore",
    cuisines=["American", "Italian"],
    cost="₹800 for two",
    budget_tier="medium",
    rating=4.3,
  ),
  Restaurant(
    name="Karim's",
    location="Delhi",
    cuisines=["Mughlai", "North Indian"],
    cost="₹600 for two",
    budget_tier="low",
    rating=4.2,
  ),
  Restaurant(
    name="Bukhara",
    location="Delhi",
    cuisines=["North Indian"],
    cost="₹4,000 for two",
    budget_tier="high",
    rating=4.6,
  ),
]

MOCK_PREFERENCES = UserPreferences(
  location="Bangalore",
  budget=1000,
  cuisine="Italian",
  min_rating=4.0,
  extras="family-friendly",
)
