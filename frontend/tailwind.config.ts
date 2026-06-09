import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        zomato: {
          DEFAULT: "#CB202D",
          dark: "#A81B26",
          light: "#E23744",
        },
        surface: "#FAFAFA",
        ink: "#1C1C1C",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        moodmeal: ["var(--font-moodmeal)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 8px 32px rgba(0, 0, 0, 0.12)",
      },
    },
  },
  plugins: [],
};

export default config;
