import { BrandLogo } from "@/components/layout/BrandLogo";

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-100 bg-white">
      <div className="mx-auto flex max-w-6xl justify-center px-4 py-5 sm:px-6 sm:py-6">
        <BrandLogo size="xl" />
      </div>
    </header>
  );
}
