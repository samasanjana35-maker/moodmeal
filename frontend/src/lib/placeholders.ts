const FOOD_IMAGES = [
  "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=800&q=80",
];

export function getPlaceholderImage(seed: string, index = 0): string {
  let hash = 0;
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash + seed.charCodeAt(i) * (i + 1)) % FOOD_IMAGES.length;
  }
  return FOOD_IMAGES[(hash + index) % FOOD_IMAGES.length];
}

export const TRENDING_PLACEHOLDERS = [
  {
    name: "The Gilded Fork",
    cuisine: "Modern Indian",
    badge: "Top pick",
    description:
      "Perfect for a celebratory dinner — bold spices, elegant plating, and a cozy vibe that matches your mood.",
    image: FOOD_IMAGES[0],
    rating: 4.9,
    reviews: "2.1k reviews",
  },
  {
    name: "Botanica Brews",
    cuisine: "Cafe",
    badge: "Open now",
    description:
      "Relaxed cafe with artisan coffee and light bites — ideal when you want something casual but memorable.",
    image: FOOD_IMAGES[1],
    rating: 4.8,
    reviews: "1.2k reviews",
  },
  {
    name: "Lumina Grill",
    cuisine: "Premium Steaks",
    description:
      "Smoky grills and premium cuts in a dimly lit setting — great for date night or a special craving.",
    image: FOOD_IMAGES[2],
    rating: 4.7,
    reviews: "980 reviews",
  },
  {
    name: "Umi Sushi",
    cuisine: "Japanese",
    description:
      "Fresh sashimi and creative rolls — a top pick if you're craving clean flavours and precise cooking.",
    image: FOOD_IMAGES[3],
    rating: 4.6,
    reviews: "760 reviews",
  },
  {
    name: "Spice Route Kitchen",
    cuisine: "North Indian",
    description:
      "Comfort classics done right — butter chicken, naan, and rich curries that hit the spot every time.",
    image: FOOD_IMAGES[4],
    rating: 4.5,
    reviews: "1.5k reviews",
  },
];

export const RESTAURANT_DISPLAY_COUNT = 5;
