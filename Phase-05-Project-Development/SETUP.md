# PocketSmart AI

Complete FastAPI + Jinja2 implementation of the supplied PocketSmart AI documentation.

## Included
- Home Interior, Party, and Jewelry planners
- Optional outfit image upload for Jewelry
- Gemini multimodal integration using the current Google GenAI Python SDK
- Structured AI output with Pydantic
- Demo provider catalog for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO-style sources
- Register/login/logout with HttpOnly JWT cookie
- Recommendation history
- Responsive frontend
- AI fallback mode so the app works without an API key
- Pytest API tests

## Source-document decisions
The supplied document mixes Flask and FastAPI wording. Its later architecture explicitly specifies FastAPI, `main.py`, Jinja2, authentication, history and the three planner APIs, so this build follows that FastAPI architecture. The document's Gemini 1.5 Flash Pro reference is historical; `GEMINI_MODEL` is configurable and defaults to a currently documented Flash model.

The catalog is deliberately mocked: it does not scrape websites and does not claim live price or availability. Replace `app/catalog.py` with official/authorized provider APIs for production commerce data.

## Run in VS Code
Python 3.11+ is recommended.

Windows PowerShell:
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. Create an account first. If `GEMINI_API_KEY` is empty, fallback recommendations still work.
`SERPAPI_API_KEY` is empty, fallback recommendations still work.

## Test
`pytest -q`

## Main APIs
`GET /health`, `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/session-info`, `GET /api/auth/session-data`, `POST /api/planners/home`, `POST /api/planners/party`, `POST /api/planners/jewelry`, `GET /api/recommendations/{id}`, `GET /api/history`, `GET /api/history/{id}`.