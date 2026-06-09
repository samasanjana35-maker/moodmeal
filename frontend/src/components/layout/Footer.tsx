import { BrandLogo } from "@/components/layout/BrandLogo";

export function Footer() {
  return (
    <footer className="border-t border-gray-100 bg-white">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <div className="flex flex-col items-center gap-4 text-center">
          <BrandLogo size="lg" />
          <p className="text-sm text-gray-500">
            AI-powered restaurant picks · explanations by Groq
          </p>
          <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-600">
            <a href="#" className="hover:text-zomato">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-zomato">
              Terms of Service
            </a>
            <a href="#" className="hover:text-zomato">
              Help
            </a>
          </div>
          <p className="text-xs text-gray-400">
            © {new Date().getFullYear()} moodmeal. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
