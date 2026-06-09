import type { DisplayRecommendation } from "@/lib/types";
import { RESTAURANT_DISPLAY_COUNT } from "@/lib/placeholders";
import { RecommendationCard } from "@/components/results/RecommendationCard";

interface TrendingSectionProps {
  location?: string;
  cuisine?: string;
  recommendations?: DisplayRecommendation[];
}

export function TrendingSection({
  location = "Bangalore",
  cuisine = "any",
  recommendations,
}: TrendingSectionProps) {
  if (!recommendations?.length) {
    return null;
  }

  const items = recommendations.slice(0, RESTAURANT_DISPLAY_COUNT);

  return (
    <section className="mx-auto max-w-[1400px] px-4 py-12 sm:px-6">
      <SectionHeader location={location} cuisine={cuisine} count={items.length} />
      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {items.map((item) => (
          <RecommendationCard key={`${item.rank}-${item.name}`} item={item} />
        ))}
      </div>
    </section>
  );
}

function SectionHeader({
  location,
  cuisine,
  count = RESTAURANT_DISPLAY_COUNT,
}: {
  location: string;
  cuisine: string;
  count?: number;
}) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div>
        <h2 className="text-2xl font-bold text-ink sm:text-3xl">
          Top {count} picks in {location}
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          {cuisine && cuisine !== "any"
            ? `${cuisine} · AI-curated restaurants from moodmeal`
            : "AI-curated restaurants with explanations from moodmeal"}
        </p>
      </div>
    </div>
  );
}
