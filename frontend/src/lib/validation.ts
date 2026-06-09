import type { PreferenceFormData } from "./types";

const BUDGET_MIN = 100;
const BUDGET_MAX = 50000;

export function validatePreferences(data: PreferenceFormData): string[] {
  const errors: string[] = [];

  if (!data.location.trim()) {
    errors.push("Area is required.");
  }

  if (!Number.isFinite(data.budget)) {
    errors.push(`Budget must be a number between ₹${BUDGET_MIN} and ₹${BUDGET_MAX}.`);
  } else if (data.budget < BUDGET_MIN || data.budget > BUDGET_MAX) {
    errors.push(`Budget must be between ₹${BUDGET_MIN} and ₹${BUDGET_MAX}.`);
  }

  if (data.min_rating < 0 || data.min_rating > 5) {
    errors.push("Minimum rating must be between 0 and 5.");
  }

  return errors;
}

export function formatBudget(amount: number): string {
  return `₹${amount.toLocaleString("en-IN")}`;
}
