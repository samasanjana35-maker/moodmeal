interface BrandLogoProps {
  className?: string;
  size?: "sm" | "md" | "lg" | "xl";
}

const SIZE = {
  sm: "text-2xl",
  md: "text-4xl sm:text-5xl",
  lg: "text-5xl sm:text-6xl",
  xl: "text-5xl sm:text-6xl lg:text-7xl",
} as const;

export function BrandLogo({ className = "", size = "md" }: BrandLogoProps) {
  return (
    <span
      className={`font-moodmeal font-bold lowercase tracking-tight text-zomato ${SIZE[size]} ${className}`}
    >
      moodmeal
    </span>
  );
}
