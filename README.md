# DDoS Live Map

DDoS Live Map is a local-first prototype for ingesting IP abuse intelligence, scoring potential DDoS activity, and visualizing events on a real-time map UI.

## What it does

- Fetches blacklist data from AbuseIPDB
- Normalizes and aggregates source IP signals into attack events
- Scores events with rule-based logic plus a logistic regression model
- Serves events over FastAPI (REST + WebSocket)
- Renders live attack markers and arcs in a React/Vite frontend

## Project status

This is an active prototype intended for local development and experimentation. Data is currently kept in memory and there is no persistence layer yet.

## Tech stack

- **Backend:** Python 3.13, FastAPI, scikit-learn
- **Frontend:** React, Vite, D3, react-simple-maps
- **Ingestion:** AbuseIPDB API + requests

## Repository structure

```text
backend/      FastAPI app and in-memory state
ingestion/    AbuseIPDB fetch worker
features/     Data normalization logic
events/       Signal aggregation and event model
scoring/      Risk scoring and labels
ml/           Feature extraction and model helpers
geo/          IP geolocation lookup
frontend/     React map UI
data/raw/     Sample and fetched raw data
```

## Prerequisites

- Python 3.13+
- Node.js 18+ and npm
- `uv` for Python dependency management (recommended)

## Local setup

1. Install backend dependencies:

   ```bash
   uv sync
   ```

2. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. Create your local env file:

   ```bash
   cp .env.example .env
   ```

4. Set your AbuseIPDB key in `.env`:

   ```bash
   ABUSEIPDB_API_KEY=your-real-key
   ```

## Running the app

Start the backend:

```bash
uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal, start the frontend:

```bash
cd frontend
npm run dev
```

Then open `http://127.0.0.1:5173`.

## Ingestion

To fetch fresh blacklist data from AbuseIPDB:

```bash
uv run python ingestion/abuseipdb_worker.py
```

The worker writes timestamped JSON files to `data/raw/` (or `OUTPUT_DIR` if configured).

## API endpoints

- `GET /events` — returns current in-memory events
- `WS /ws/events` — streams newly appended events
