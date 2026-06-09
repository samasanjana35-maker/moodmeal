import type { FormOptions, PreferenceFormData } from "@/lib/types";

export const DEFAULT_BUDGETS = [500, 800, 1000, 1500, 2000, 3000, 5000];

export const FALLBACK_AREAS = [
  "Indiranagar",
  "Koramangala",
  "Jayanagar",
  "Whitefield",
  "Marathahalli",
  "Bellandur",
  "Hsr",
  "Btm",
  "Jp Nagar",
  "Mg Road",
  "Brigade Road",
  "Hebbal",
  "Banashankari",
  "Malleshwaram",
  "Electronic City",
];

export const FALLBACK_CUISINES = [
  "North Indian",
  "South Indian",
  "Chinese",
  "Italian",
  "Continental",
  "Mughlai",
  "Biryani",
  "Cafe",
  "Fast Food",
  "Desserts",
  "Bakery",
  "Street Food",
  "Thai",
  "Japanese",
  "Mexican",
];

export const DEFAULT_OPTIONS: FormOptions = {
  cities: ["Bangalore"],
  areas: FALLBACK_AREAS,
  locations: ["Bangalore", ...FALLBACK_AREAS],
  cuisines: FALLBACK_CUISINES,
  budgets: DEFAULT_BUDGETS,
  cravings: [
    "Spicy",
    "Butter Chicken",
    "Biryani",
    "Pizza",
    "Dosa",
    "Momos",
  ],
};

export function getAreaOptions(options: FormOptions): string[] {
  if (options.areas.length > 0) {
    return options.areas;
  }
  return options.locations.filter((loc) => !options.cities.includes(loc));
}

export function mergeFormOptions(api: Partial<FormOptions>): FormOptions {
  return {
    cities:
      api.cities && api.cities.length > 0
        ? api.cities
        : DEFAULT_OPTIONS.cities,
    areas:
      api.areas && api.areas.length > 0 ? api.areas : DEFAULT_OPTIONS.areas,
    locations:
      api.locations && api.locations.length > 0
        ? api.locations
        : DEFAULT_OPTIONS.locations,
    cuisines:
      api.cuisines && api.cuisines.length > 0
        ? api.cuisines
        : DEFAULT_OPTIONS.cuisines,
    budgets:
      api.budgets && api.budgets.length > 0
        ? api.budgets
        : DEFAULT_OPTIONS.budgets,
    cravings:
      api.cravings && api.cravings.length > 0
        ? api.cravings
        : DEFAULT_OPTIONS.cravings,
  };
}

export function normalizeFormAgainstOptions(
  form: PreferenceFormData,
  options: FormOptions,
): PreferenceFormData {
  const areaOptions = getAreaOptions(options);

  let location = form.location.trim();
  if (!location || !areaOptions.includes(location)) {
    location = areaOptions[0] ?? "";
  }

  let cuisine = form.cuisine;
  if (cuisine !== "any" && !options.cuisines.includes(cuisine)) {
    cuisine = "any";
  }

  return { ...form, location, cuisine };
}
