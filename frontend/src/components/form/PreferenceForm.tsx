"use client";

import { getAreaOptions } from "@/lib/defaultOptions";
import type { FormOptions, PreferenceFormData } from "@/lib/types";
import { formatBudget } from "@/lib/validation";
import {
  CuisineIcon,
  NoteIcon,
  PinIcon,
  SparkleIcon,
  StarIcon,
  WalletIcon,
} from "@/components/ui/icons";

interface PreferenceFormProps {
  options: FormOptions;
  values: PreferenceFormData;
  errors: string[];
  disabled?: boolean;
  onChange: (values: PreferenceFormData) => void;
  onSubmit: () => void;
}

const SELECT_CLASS =
  "w-full cursor-pointer rounded-lg border border-gray-200 bg-white px-3 py-2.5 text-sm text-gray-900 focus:border-zomato focus:outline-none focus:ring-2 focus:ring-zomato/20 disabled:cursor-not-allowed disabled:opacity-60";

function FieldLabel({
  icon,
  children,
}: {
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <span className="mb-1.5 flex items-center gap-1.5 text-sm font-semibold text-gray-800">
      {icon}
      {children}
    </span>
  );
}

export function PreferenceForm({
  options,
  values,
  errors,
  disabled = false,
  onChange,
  onSubmit,
}: PreferenceFormProps) {
  const areaOptions = getAreaOptions(options);
  const selectedArea = areaOptions.includes(values.location)
    ? values.location
    : "";
  const selectedCuisine =
    values.cuisine === "any" || options.cuisines.includes(values.cuisine)
      ? values.cuisine
      : "any";

  function update<K extends keyof PreferenceFormData>(
    key: K,
    value: PreferenceFormData[K],
  ) {
    onChange({ ...values, [key]: value });
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    onSubmit();
  }

  const locationError = errors.find(
    (e) =>
      e.toLowerCase().includes("area") ||
      e.toLowerCase().includes("location"),
  );
  const sliderFill = ((values.min_rating - 3) / 2) * 100;

  return (
    <form
      onSubmit={handleSubmit}
      className="relative z-10 overflow-visible rounded-2xl bg-white p-6 shadow-card sm:p-8"
    >
      <div className="grid gap-5 overflow-visible sm:grid-cols-2">
        <div className="overflow-visible sm:col-span-1">
          <FieldLabel icon={<PinIcon />}>City</FieldLabel>
          <select
            disabled={disabled}
            value={options.cities[0] ?? "Bangalore"}
            className={`${SELECT_CLASS} bg-gray-50 text-gray-700`}
          >
            {options.cities.map((city) => (
              <option key={`city-${city}`} value={city}>
                {city}
              </option>
            ))}
          </select>
        </div>

        <div className="overflow-visible sm:col-span-1">
          <FieldLabel icon={<PinIcon />}>Area</FieldLabel>
          <select
            required
            disabled={disabled || areaOptions.length === 0}
            value={selectedArea}
            onChange={(e) => update("location", e.target.value)}
            className={`${SELECT_CLASS} ${
              locationError ? "border-red-400" : ""
            }`}
          >
            <option value="" disabled>
              Select area
            </option>
            {areaOptions.map((area) => (
              <option key={`area-${area}`} value={area}>
                {area}
              </option>
            ))}
          </select>
          {locationError && (
            <p className="mt-1.5 flex items-center gap-1 text-xs font-medium text-red-500">
              <span aria-hidden>⚠</span> {locationError}
            </p>
          )}
        </div>

        <div className="overflow-visible sm:col-span-1">
          <FieldLabel icon={<CuisineIcon />}>Cuisine</FieldLabel>
          <select
            disabled={disabled || options.cuisines.length === 0}
            value={selectedCuisine}
            onChange={(e) => update("cuisine", e.target.value)}
            className={SELECT_CLASS}
          >
            <option value="any">Any cuisine</option>
            {options.cuisines.map((cuisine) => (
              <option key={`cuisine-${cuisine}`} value={cuisine}>
                {cuisine}
              </option>
            ))}
          </select>
        </div>

        <div className="overflow-visible sm:col-span-1">
          <FieldLabel icon={<WalletIcon />}>Budget</FieldLabel>
          <select
            required
            disabled={disabled}
            value={values.budget}
            onChange={(e) => update("budget", Number(e.target.value))}
            className={SELECT_CLASS}
          >
            {options.budgets.map((amount) => (
              <option key={amount} value={amount}>
                {formatBudget(amount)}
              </option>
            ))}
          </select>
        </div>

        <div className="overflow-visible sm:col-span-1">
          <FieldLabel icon={<StarIcon />}>Minimum Rating</FieldLabel>
          <div className="pt-1">
            <input
              type="range"
              min={3}
              max={5}
              step={0.1}
              disabled={disabled}
              value={Math.max(values.min_rating, 3)}
              onChange={(e) => update("min_rating", Number(e.target.value))}
              style={
                {
                  "--fill": `${Math.max(0, Math.min(100, sliderFill))}%`,
                } as React.CSSProperties
              }
              className="rating-slider w-full disabled:opacity-60"
            />
            <div className="mt-1 flex justify-between text-xs text-gray-500">
              <span>3.0</span>
              <span className="font-semibold text-zomato">
                {Math.max(values.min_rating, 3).toFixed(1)}+
              </span>
              <span>5.0</span>
            </div>
          </div>
        </div>

        <div className="sm:col-span-2">
          <FieldLabel icon={<CuisineIcon />}>Specific Cravings</FieldLabel>
          <p className="mb-2 text-xs text-gray-500">
            Optional — pick what you&apos;re in the mood for
          </p>
          <div className="flex flex-wrap gap-2">
            {options.cravings.map((craving) => {
              const selected = values.cravings.includes(craving);
              return (
                <button
                  key={craving}
                  type="button"
                  disabled={disabled}
                  onClick={() => {
                    const next = selected
                      ? values.cravings.filter((item) => item !== craving)
                      : [...values.cravings, craving];
                    update("cravings", next);
                  }}
                  className={`rounded-full border px-3 py-1.5 text-sm font-medium transition disabled:opacity-60 ${
                    selected
                      ? "border-zomato bg-zomato text-white"
                      : "border-gray-200 bg-white text-gray-700 hover:border-zomato/50"
                  }`}
                >
                  {craving}
                </button>
              );
            })}
          </div>
        </div>

        <div className="sm:col-span-2">
          <FieldLabel icon={<NoteIcon />}>Additional Preferences</FieldLabel>
          <textarea
            rows={3}
            disabled={disabled}
            value={values.extras}
            onChange={(e) => update("extras", e.target.value)}
            placeholder="e.g. Quiet for business meetings, outdoor seating with a view, pet-friendly..."
            className="w-full resize-none rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-900 placeholder:text-gray-400 focus:border-zomato focus:outline-none focus:ring-2 focus:ring-zomato/20 disabled:opacity-60"
          />
        </div>
      </div>

      {errors.filter(
        (e) =>
          !e.toLowerCase().includes("area") &&
          !e.toLowerCase().includes("location"),
      ).length > 0 && (
        <div
          className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
          role="alert"
        >
          <ul className="list-inside list-disc space-y-1">
            {errors
              .filter(
                (e) =>
                  !e.toLowerCase().includes("area") &&
                  !e.toLowerCase().includes("location"),
              )
              .map((error) => (
                <li key={error}>{error}</li>
              ))}
          </ul>
        </div>
      )}

      <button
        type="submit"
        disabled={disabled}
        className="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-zomato px-4 py-3.5 text-sm font-bold text-white transition hover:bg-zomato-dark focus:outline-none focus:ring-2 focus:ring-zomato focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
      >
        <SparkleIcon />
        Get recommendations
      </button>
    </form>
  );
}
