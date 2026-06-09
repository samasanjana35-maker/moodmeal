"use client";

import { useCallback, useEffect, useState } from "react";
import { ApiError, fetchOptions, fetchRecommendations } from "@/lib/api";
import type {
  AppState,
  FormOptions,
  PipelineResponse,
  PreferenceFormData,
} from "@/lib/types";
import {
  DEFAULT_OPTIONS,
  mergeFormOptions,
  normalizeFormAgainstOptions,
} from "@/lib/defaultOptions";
import { validatePreferences } from "@/lib/validation";
import { EmptyState } from "@/components/results/EmptyState";
import { ErrorAlert } from "@/components/results/ErrorAlert";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { HeroSection } from "@/components/layout/HeroSection";
import { LoadingState } from "@/components/results/LoadingState";
import { ResultsSection } from "@/components/results/ResultsSection";

const DEFAULT_FORM: PreferenceFormData = {
  location: "Indiranagar",
  budget: 2000,
  cuisine: "any",
  cravings: [],
  min_rating: 3.5,
  extras: "",
};

export function HomePage() {
  const [options, setOptions] = useState<FormOptions>(DEFAULT_OPTIONS);
  const [optionsError, setOptionsError] = useState<string | null>(null);
  const [form, setForm] = useState<PreferenceFormData>(DEFAULT_FORM);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [appState, setAppState] = useState<AppState>("idle");
  const [result, setResult] = useState<PipelineResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [lastSubmitted, setLastSubmitted] = useState<PreferenceFormData | null>(
    null,
  );

  const loadOptions = useCallback(async () => {
    try {
      const data = await fetchOptions();
      const merged = mergeFormOptions(data);
      setOptions(merged);
      setOptionsError(null);
      setForm((current) => normalizeFormAgainstOptions(current, merged));
    } catch (error) {
      setOptions(DEFAULT_OPTIONS);
      const message =
        error instanceof ApiError
          ? error.message
          : "Backend unavailable — showing default areas and cuisines. Start the API with: python -m backend";
      setOptionsError(message);
    }
  }, []);

  useEffect(() => {
    loadOptions();
  }, [loadOptions]);

  async function submitRecommendations() {
    const errors = validatePreferences(form);
    setValidationErrors(errors);
    if (errors.length > 0) {
      return;
    }

    setAppState("loading");
    setErrorMessage(null);
    setResult(null);
    setLastSubmitted({ ...form });

    try {
      const response = await fetchRecommendations(form);
      setResult(response);
      setAppState(
        response.status === "no_matches" ? "no_matches" : "success",
      );
      document
        .getElementById("results")
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      setAppState("error");
      setErrorMessage(
        error instanceof ApiError
          ? error.message
          : "Something went wrong. Please try again.",
      );
    }
  }

  function resetResults() {
    setAppState("idle");
    setResult(null);
    setErrorMessage(null);
    setValidationErrors([]);
    setLastSubmitted(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const showResults =
    appState === "success" &&
    result &&
    lastSubmitted &&
    result.status === "success";
  const showEmpty =
    appState === "no_matches" && result && result.status === "no_matches";
  const preferencesChanged =
    lastSubmitted !== null &&
    (form.location !== lastSubmitted.location ||
      form.cuisine !== lastSubmitted.cuisine ||
      form.budget !== lastSubmitted.budget ||
      form.min_rating !== lastSubmitted.min_rating ||
      form.extras !== lastSubmitted.extras ||
      JSON.stringify(form.cravings) !== JSON.stringify(lastSubmitted.cravings));

  return (
    <div className="flex min-h-screen flex-col bg-white">
      <Header />

      <HeroSection
        options={options}
        form={form}
        errors={validationErrors}
        disabled={appState === "loading"}
        onChange={setForm}
        onSubmit={submitRecommendations}
      />

      {optionsError && (
        <div className="mx-auto w-full max-w-3xl px-4 pt-4 sm:px-6">
          <ErrorAlert message={optionsError} onRetry={loadOptions} />
        </div>
      )}

      <div id="results">
        {appState === "loading" && <LoadingState />}

        {appState === "error" && errorMessage && (
          <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
            <ErrorAlert message={errorMessage} onRetry={submitRecommendations} />
          </div>
        )}

        {showResults && preferencesChanged && (
          <div className="mx-auto max-w-6xl px-4 pt-6 sm:px-6">
            <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
              Preferences changed — click <strong>Get recommendations</strong> to
              update your results.
            </div>
          </div>
        )}

        {showResults && !preferencesChanged && (
          <ResultsSection
            result={result}
            preferences={lastSubmitted}
            onNewSearch={resetResults}
          />
        )}

        {showEmpty && (
          <EmptyState
            result={result}
            onAdjust={resetResults}
            onStartOver={() => {
              setForm(DEFAULT_FORM);
              resetResults();
            }}
          />
        )}
      </div>

      <Footer />
    </div>
  );
}
