import type { Metadata } from "next";
import { Comfortaa, Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const comfortaa = Comfortaa({
  subsets: ["latin"],
  weight: ["700"],
  variable: "--font-moodmeal",
});

export const metadata: Metadata = {
  title: "moodmeal — Restaurant Recommendations",
  description:
    "Find your perfect meal with AI-curated recommendations based on reviews and local insights.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${comfortaa.variable} min-h-screen font-sans antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
