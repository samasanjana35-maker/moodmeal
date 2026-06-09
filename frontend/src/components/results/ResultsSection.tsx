import type { PipelineResponse, PreferenceFormData } from "@/lib/types";
import { Notices } from "@/components/results/Notices";
import { TrendingSection } from "@/components/results/TrendingSection";

interface ResultsSectionProps {
  result: PipelineResponse;
  preferences: PreferenceFormData;
  onNewSearch: () => void;
}

export function ResultsSection({
  result,
  preferences,
  onNewSearch,
}: ResultsSectionProps) {
  const recommendations = result.recommendations ?? [];

  return (
    <section className="bg-surface">
      <div className="mx-auto max-w-6xl px-4 pt-6 sm:px-6">
        <div className="flex justify-end">
          <button
            type="button"
            onClick={onNewSearch}
            className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm transition hover:border-zomato hover:text-zomato"
          >
            New search
          </button>
        </div>
        <Notices result={result} />
      </div>

      <TrendingSection
        location={preferences.location}
        cuisine={preferences.cuisine}
        recommendations={recommendations}
      />
    </section>
  );
}
