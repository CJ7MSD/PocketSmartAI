## Run in VS Code
Python 3.11+ is recommended.

Copy `.env.example` to `.env` and add your own API keys. if
`GEMINI_API_KEY` is empty, fallback recommendations still work.
`SERPAPI_API_KEY` is empty, fallback recommendations still work.

Windows PowerShell:
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. Create an account first.

## Test
`pytest -q`

## Main APIs
`GET /health`, `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/session-info`, `GET /api/auth/session-data`, `POST /api/planners/home`, `POST /api/planners/party`, `POST /api/planners/jewelry`, `GET /api/recommendations/{id}`, `GET /api/history`, `GET /api/history/{id}`.