import type { PipelineResponse } from "@/lib/types";

interface NoticesProps {
  result: PipelineResponse;
}

export function Notices({ result }: NoticesProps) {
  const relaxed = result.relaxed_constraints ?? [];

  if (!relaxed.length && !result.fallback_used) {
    return null;
  }

  return (
    <div className="mt-4 space-y-3">
      {relaxed.length > 0 && (
        <div
          className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900"
          role="status"
        >
          Filters were relaxed to find results: {relaxed.join(", ")}
        </div>
      )}

      {result.fallback_used && (
        <div
          className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-900"
          role="status"
        >
          {result.fallback_message ||
            "Showing rating-based fallback recommendations."}
        </div>
      )}
    </div>
  );
}
