# Frontend UI Prompt — Google Stitch (Next.js)

Use the prompt below in [Google Stitch](https://stitch.withgoogle.com/) to generate UI mockups and screen images for the **MILESTONE** restaurant recommendation app. The implementation target is **Next.js** (App Router) talking to a **FastAPI** backend.

---

## Quick copy — paste into Google Stitch

```
Design a modern, mobile-first restaurant recommendation web app called "MILESTONE" (Zomato-inspired but original branding). Target framework: Next.js 14+ with App Router, TypeScript, and Tailwind CSS. Generate high-fidelity UI screens for desktop and mobile.

PRODUCT SUMMARY
AI-powered restaurant finder for Indian cities (primarily Bangalore). Users set preferences; the backend returns ranked restaurants with AI-written explanations. Tone: helpful, trustworthy, food-forward — not a clone of Zomato red, use a fresh palette (deep coral #E85D4C or warm amber accent, off-white background #FAFAF8, dark text #1A1A1A, subtle gray borders).

SCREENS TO GENERATE (separate artboards)

1) HOME / SEARCH — empty state
- Top: logo "MILESTONE" + tagline "Find your next meal, explained by AI"
- Hero: soft illustration or food photography strip (subtle, not cluttered)
- Preference form card (centered, max-width ~640px):
  • Location — searchable dropdown (e.g. Bangalore, Bellandur)
  • Budget — segmented control: Low | Medium | High
  • Cuisine — dropdown with "Any cuisine" default
  • Minimum rating — slider 0.0 to 5.0 with star icons
  • Additional preferences — multiline text placeholder: "family-friendly, quick service, outdoor seating"
  • Primary CTA button: "Get recommendations" (full width on mobile)
- Footer: "Powered by Zomato dataset · AI explanations by Groq"
- Show inline validation error example under Location: "Location is required" (red, small)

2) LOADING STATE
- Same layout as screen 1 but form disabled
- Skeleton cards below OR centered spinner with text "Finding restaurants for you..."
- Subtle progress shimmer on 3 placeholder recommendation cards

3) RESULTS — success (5 recommendations)
- Sticky summary bar: "5 recommendations in Bellandur" + chip "High budget" + chip "4.0+ rating"
- Optional info banner (light blue): "Showing rating-based fallback recommendations" 
- Optional warning banner (amber): "Filters were relaxed: cuisine"
- Vertical list of recommendation cards, ranked #1–#5:
  Each card contains:
  • Rank badge (#1 gold accent, others neutral)
  • Restaurant name (bold, large)
  • Area pin icon + neighborhood (e.g. Bellandur)
  • Row of metrics: ⭐ 4.6 rating | ₹1,800 for two | Cuisine tags
  • Section "Why this pick" with 2–3 lines of AI explanation in slightly muted body text
  • Subtle card shadow, rounded-xl, hover state on desktop
- Example restaurants for realism: Chili's American Grill & Bar, Bombay Brasserie, MoMo Cafe, Nook, The Irish House
- Floating "New search" secondary button or top nav link

4) EMPTY STATE — no matches
- Illustration: empty plate or map pin with question mark
- Headline: "No restaurants matched your preferences"
- Body: "We couldn't find spots in Goa with your current filters."
- Bulleted suggestions card: "Try a different location", "Lower minimum rating", "Choose Any cuisine", "Switch to Medium budget"
- CTA: "Adjust preferences" (primary) + "Start over" (ghost)

5) ERROR STATE
- Toast or inline alert: "Something went wrong. Please try again."
- Retry button
- Optional: "Backend unavailable" for API connection failures

DESIGN SYSTEM
- Typography: Inter or Plus Jakarta Sans; clear hierarchy (H1 32px, card title 20px, body 15px)
- Components: shadcn/ui style — clean inputs, rounded-lg, focus rings
- Icons: Lucide-style line icons (map pin, star, rupee/currency, utensils)
- Spacing: generous padding, 16px mobile / 24px desktop gutters
- Dark mode variant (optional second pass): same screens with dark bg #0F0F0F

NEXT.JS IMPLEMENTATION NOTES (for developer handoff)
- Pages: / (search), /results (or same page with results section)
- Form submits POST to /api/v1/recommendations via Next.js fetch to backend URL
- GET /api/v1/options populates location and cuisine dropdowns on load
- States: idle | loading | success | no_matches | error
- Responsive: single column mobile; results grid optional 2-col on large desktop
- Accessibility: labels on all inputs, 44px touch targets, WCAG AA contrast

DELIVERABLES
Generate all 5 screens at 1440×900 (desktop) and 390×844 (mobile). Keep visual language consistent across artboards. Show realistic Indian restaurant data and rupee pricing (₹). No lorem ipsum in explanations — use natural recommendation copy.
```

---

## Screen checklist

| # | Screen | User state | Key elements |
|---|--------|------------|--------------|
| 1 | Home / search | First visit | Preference form, CTA |
| 2 | Loading | After submit | Spinner, disabled form |
| 3 | Results | API `status: success` | Ranked cards, metrics, AI explanation |
| 4 | Empty | API `status: no_matches` | Message, suggestions, adjust CTA |
| 5 | Error | API `500` or network fail | Alert, retry |

---

## Data the UI must display

### Form fields (maps to API request)

| Field | UI control | API field | Required |
|-------|------------|-----------|----------|
| Location | Searchable select | `location` | Yes |
| Budget | Segmented / select | `budget` (`low` \| `medium` \| `high`) | Yes |
| Cuisine | Select | `cuisine` (omit if "Any") | No |
| Min rating | Slider 0–5 | `min_rating` | No |
| Extras | Textarea | `extras` | No |

### Recommendation card (maps to API response)

| UI label | API field | Example |
|----------|-----------|---------|
| Rank | `rank` | `1` |
| Name | `name` | `Chili's American Grill & Bar` |
| Area | `area` | `Bellandur` |
| Rating | `rating` | `4.6` |
| Cost | `estimated_cost` | `₹1,800 for two` |
| Cuisine | `cuisine` | `American, Tex-Mex, Burger, BBQ` |
| Why this pick | `explanation` | AI-generated paragraph |

### Banners (conditional)

| Condition | Banner type | Copy source |
|-----------|-------------|-------------|
| `fallback_used: true` | Info (blue) | `fallback_message` |
| `relaxed_constraints` non-empty | Warning (amber) | `"Filters were relaxed: …"` |
| `status: no_matches` | Empty state | `message` + `suggestions[]` |

---

## Backend API reference (for Stitch context)

Base URL: `http://localhost:8000` (dev)

```
GET  /api/v1/options          → { locations: string[], cuisines: string[] }
POST /api/v1/recommendations  → success | no_matches JSON (see architecture.md)
```

Full contract: [architecture.md](../architecture/architecture.md#api-contract-backend).

---

## Optional Stitch follow-up prompts

After the first generation, refine individual screens:

**Mobile results refinement**
```
Refine the MILESTONE results screen for mobile only (390px). Stack metric chips vertically. Make rank badge smaller. Ensure "Why this pick" text is readable at 15px. Keep primary coral accent.
```

**Dark mode**
```
Generate dark mode versions of all 5 MILESTONE screens. Background #0F0F0F, cards #1A1A1A, accent coral #E85D4C, text #F5F5F5.
```

**Component library**
```
From the MILESTONE designs, extract a mini design system page: buttons (primary, secondary, ghost), inputs, select, slider, recommendation card, alert banners, empty state. Next.js + Tailwind + shadcn/ui style.
```

---

## Related documents

- [Problem statement](../requirements/problemstatement.md) — product requirements
- [Architecture](../architecture/architecture.md) — Phase 7 frontend, API contract
- [Edge cases](../requirements/edge-cases.md) — empty state, fallback, validation UX
