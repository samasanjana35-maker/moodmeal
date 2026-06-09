export function LoadingState() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-12 sm:px-6" aria-live="polite" aria-busy="true">
      <div className="flex items-center justify-center gap-3 py-6">
        <span className="inline-block h-5 w-5 animate-spin rounded-full border-2 border-zomato border-t-transparent" />
        <p className="text-sm font-medium text-gray-700">
          Finding restaurants for you...
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 lg:grid-rows-2">
        <div className="min-h-[320px] animate-pulse rounded-2xl bg-gray-200 lg:row-span-2" />
        <div className="min-h-[180px] animate-pulse rounded-2xl bg-gray-200" />
        <div className="min-h-[180px] animate-pulse rounded-2xl bg-gray-200" />
        <div className="min-h-[180px] animate-pulse rounded-2xl bg-gray-200 sm:col-span-2 lg:col-span-1" />
      </div>
    </section>
  );
}
