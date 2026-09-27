# PocketSmart AI — Real-World Ready

PocketSmart AI is a FastAPI + Jinja2 budget-planning assistant for **Home Interior, Party and Jewelry** planning.

## What was changed

The original repository already had the FastAPI architecture, authentication, SQLite history, Gemini integration and a demo catalog. The important limitation was that the catalog was explicitly mocked.

This version adds a **live recommendation adapter**:

- Optional Serper Google Shopping integration for live product/search results in India.
- Live result links and prices are carried into the recommendation cards.
- Gemini remains optional: without a Gemini key, live results still work.
- If live search is not configured or temporarily fails, the app safely falls back to the bundled demo catalog.
- `/health` and `/api/system/status` show whether live and AI modes are enabled.
- The existing login, dashboard, history and three planners remain intact.

## Architecture

```text
Browser (HTML/CSS/JS)
        |
        v
FastAPI + Jinja2
  |       |        |
 Auth   Planners  History
          |
          v
 Recommendation Service
      |          |
      |          +--> Gemini (optional)
      |
      +--> Live Shopping Adapter (optional Serper)
      |
      +--> Demo Catalog fallback
          |
          v
 SQLite
```

## Run locally

Python 3.11+:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

Create an account first.

## Enable live recommendations

Put the following in `.env`:

```env
SERPAPI_API_KEY=your_serper_key
LIVE_RECOMMENDATIONS=true
```

The application uses Google's Shopping results through Serper's API and requests India-localized results (`gl=in`).

**Important:** a third-party search API is an adapter, not an official Amazon/Flipkart/IKEA API. For commercial production, replace `app/services/live_catalog.py` with official/authorized partner APIs or affiliate feeds where available. Never scrape sites in violation of their terms.

## Enable Gemini

```env
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-3.8-flash
```

Gemini is used to interpret and structure recommendations. Jewelry can additionally pass the uploaded outfit image to the multimodal model.

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Main routes

- `GET /health`
- `GET /api/system/status`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/session-info`
- `POST /api/planners/home`
- `POST /api/planners/party`
- `POST /api/planners/jewelry`
- `GET /api/history`
- `GET /api/recommendations/{id}`

## Production checklist

Before public deployment:

1. Set a strong random `SECRET_KEY`.
2. Use PostgreSQL or another managed database instead of local SQLite.
3. Serve through HTTPS.
4. Restrict `CORS_ORIGINS` to the real frontend origin.
5. Keep API keys only in server-side environment variables.
6. Add rate limiting and monitoring.
7. Use official/authorized commerce APIs or affiliate feeds for each provider where possible.
8. Treat live prices/availability as time-sensitive and verify them on the provider page.
