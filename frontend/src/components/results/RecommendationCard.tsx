import type { DisplayRecommendation } from "@/lib/types";
import { getPlaceholderImage } from "@/lib/placeholders";

interface RecommendationCardProps {
  item: DisplayRecommendation;
}

export function RecommendationCard({ item }: RecommendationCardProps) {
  const image = getPlaceholderImage(item.name, item.rank);
  const isTopPick = item.rank === 1;
  const cuisineLabel = item.cuisine.split(",")[0]?.trim() || "Restaurant";

  return (
    <article className="group relative min-h-[420px] overflow-hidden rounded-2xl sm:min-h-[460px]">
      <img
        src={image}
        alt={item.name}
        className="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-105"
      />
      <div className="absolute inset-0 bg-gradient-to-b from-black/55 via-black/35 to-black/75" />

      <div className="absolute left-4 right-4 top-4 flex flex-wrap items-start justify-between gap-2">
        <div className="flex flex-wrap gap-2">
          {isTopPick && (
            <span className="rounded-md bg-zomato px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide text-white">
              Top pick
            </span>
          )}
          <span className="rounded-md bg-black/50 px-2.5 py-1 text-[10px] font-semibold text-white backdrop-blur-sm">
            {cuisineLabel}
          </span>
        </div>
        {item.rating != null && (
          <span className="rounded-md bg-black/50 px-2.5 py-1 text-xs font-bold text-white backdrop-blur-sm">
            ★ {item.rating}
          </span>
        )}
      </div>

      <div className="absolute inset-x-4 top-[4.5rem] bottom-16 flex flex-col justify-center">
        <h3 className="text-xl font-bold leading-tight text-white sm:text-2xl">
          {item.name}
        </h3>

        <div className="mt-3 rounded-xl border border-white/15 bg-black/50 p-4 backdrop-blur-md">
          <p className="text-[10px] font-bold uppercase tracking-wider text-zomato-light">
            AI explanation
          </p>
          <p className="mt-2 line-clamp-5 text-sm leading-relaxed text-white/95">
            {item.explanation}
          </p>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 flex flex-wrap items-center gap-3 p-4 text-sm text-white/90">
        {item.estimated_cost && (
          <span className="font-semibold text-white">{item.estimated_cost}</span>
        )}
        {item.area && <span className="text-white/80">📍 {item.area}</span>}
      </div>
    </article>
  );
}
