export interface PreferenceFormData {
  location: string;
  budget: number;
  cuisine: string;
  cravings: string[];
  min_rating: number;
  extras: string;
}

export interface RecommendationRequest {
  location: string;
  budget: number;
  cuisine?: string;
  cravings?: string[];
  min_rating: number;
  extras?: string;
}

export interface DisplayRecommendation {
  rank: number;
  name: string;
  cuisine: string;
  rating: number | null;
  estimated_cost: string | null;
  area: string | null;
  explanation: string;
}

export interface PipelineResponse {
  status: "success" | "no_matches" | string;
  count?: number;
  message?: string;
  suggestions?: string[];
  recommendations?: DisplayRecommendation[];
  fallback_used?: boolean;
  fallback_message?: string;
  relaxed_constraints?: string[];
}

export interface FormOptions {
  cities: string[];
  areas: string[];
  locations: string[];
  cuisines: string[];
  budgets: number[];
  cravings: string[];
}

export type AppState = "idle" | "loading" | "success" | "no_matches" | "error";
