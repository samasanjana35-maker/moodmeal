# MILESTONE Frontend (Phase 7)

Next.js App Router frontend for the restaurant recommendation system. Calls the Phase 6 FastAPI backend.

## Prerequisites

- Node.js 18+
- Backend API running (`python -m backend` on port 8000)

## Setup

```bash
cd frontend
cp .env.local.example .env.local
npm install
```

## Run

```bash
# Terminal 1 — backend
cd .. && python -m backend

# Terminal 2 — frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Phase 6 API base URL |

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Development server on :3000 |
| `npm run build` | Production build |
| `npm run start` | Production server |
