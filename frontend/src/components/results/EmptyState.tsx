import type { PipelineResponse } from "@/lib/types";

interface EmptyStateProps {
  result: PipelineResponse;
  onAdjust: () => void;
  onStartOver: () => void;
}

export function EmptyState({ result, onAdjust, onStartOver }: EmptyStateProps) {
  const suggestions = result.suggestions ?? [];

  return (
    <section className="mx-auto max-w-2xl px-4 py-12 sm:px-6">
      <div className="rounded-2xl border border-gray-100 bg-white p-8 text-center shadow-card">
        <p className="text-5xl" aria-hidden>
          🍽️
        </p>
        <h2 className="mt-4 text-xl font-bold text-ink">
          No restaurants matched your preferences
        </h2>
        <p className="mt-2 text-sm text-gray-600">
          {result.message ||
            "We couldn't find spots with your current filters."}
        </p>

        {suggestions.length > 0 && (
          <div className="mx-auto mt-6 max-w-md rounded-xl border border-gray-100 bg-surface p-4 text-left">
            <p className="text-sm font-semibold text-ink">Try:</p>
            <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-gray-600">
              {suggestions.map((suggestion) => (
                <li key={suggestion}>{suggestion}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-6 flex flex-col justify-center gap-3 sm:flex-row">
          <button
            type="button"
            onClick={onAdjust}
            className="rounded-lg bg-zomato px-5 py-2.5 text-sm font-bold text-white hover:bg-zomato-dark"
          >
            Adjust preferences
          </button>
          <button
            type="button"
            onClick={onStartOver}
            className="rounded-lg border border-gray-200 px-5 py-2.5 text-sm font-medium text-gray-700 hover:border-zomato hover:text-zomato"
          >
            Start over
          </button>
        </div>
      </div>
    </section>
  );
}
