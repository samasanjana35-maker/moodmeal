import type {
  FormOptions,
  PipelineResponse,
  PreferenceFormData,
  RecommendationRequest,
} from "./types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function toRequestBody(data: PreferenceFormData): RecommendationRequest {
  const body: RecommendationRequest = {
    location: data.location.trim(),
    budget: data.budget,
    min_rating: data.min_rating,
  };

  if (data.cuisine && data.cuisine !== "any") {
    body.cuisine = data.cuisine;
  }

  if (data.cravings.length > 0) {
    body.cravings = data.cravings;
  }

  const extras = data.extras.trim();
  if (extras) {
    body.extras = extras;
  }

  return body;
}

async function parseError(response: Response): Promise<ApiError> {
  let detail: unknown;
  try {
    detail = await response.json();
  } catch {
    detail = undefined;
  }

  if (response.status === 422) {
    const errors = Array.isArray((detail as { detail?: unknown })?.detail)
      ? ((detail as { detail: string[] }).detail).join(" ")
      : "Invalid request.";
    return new ApiError(errors, 422, detail);
  }

  if (response.status >= 500) {
    return new ApiError(
      "Something went wrong. Please try again.",
      response.status,
      detail,
    );
  }

  return new ApiError(
    "Unable to reach the recommendation service.",
    response.status,
    detail,
  );
}

export async function fetchOptions(): Promise<FormOptions> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);

  let response: Response;
  try {
    response = await fetch(`${API_URL}/api/v1/options`, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }

  if (!response.ok) {
    throw await parseError(response);
  }

  return response.json();
}

export async function fetchRecommendations(
  data: PreferenceFormData,
): Promise<PipelineResponse> {
  const response = await fetch(`${API_URL}/api/v1/recommendations`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(toRequestBody(data)),
  });

  if (!response.ok) {
    throw await parseError(response);
  }

  return response.json();
}

export function getApiUrl(): string {
  return API_URL;
}
