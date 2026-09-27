from pathlib import Path
from fastapi import FastAPI,Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.database import Base,engine
from app.routes.auth import r as auth
from app.routes.planners import r as planners
from app.routes.history import r as history
from app.services import live_catalog
base=Path(__file__).resolve().parent; s=get_settings(); Base.metadata.create_all(bind=engine)
app=FastAPI(title=s.app_name,version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=s.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory=str(base/"static")),name="static"); templates=Jinja2Templates(directory=str(base/"templates")); app.include_router(auth); app.include_router(planners); app.include_router(history)
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": s.app_name,
        "live_recommendations": bool(s.live_recommendations and (s.serpapi_api_key or s.serper_api_key)),
        "gemini": bool(s.gemini_api_key),
    }

@app.get("/api/live/test")
def live_test(q: str = "wireless headphones India"):
    """Directly test the configured SerpApi Google Shopping provider."""
    items = live_catalog.shopping_search(q, "diagnostic", 5)
    return {
        "configured": bool(s.live_recommendations and (s.serpapi_api_key or s.serper_api_key)),
        "status": live_catalog.LAST_STATUS,
        "result_count": len(items),
        "error": live_catalog.LAST_ERROR or None,
        "query": q,
        "results": [
            {"name": x.name, "price": x.price, "platform": x.platform, "url": x.url}
            for x in items
        ],
    }

@app.get("/api/system/status")
def system_status():
    # Safe diagnostics: never expose API keys.
    live_enabled = bool(s.live_recommendations and (s.serpapi_api_key or s.serper_api_key))
    return {
        "service": s.app_name,
        "mode": "live" if live_enabled else "demo",
        "ai_enabled": bool(s.gemini_api_key),
        "live_provider_enabled": live_enabled,
        "serpapi_key_loaded": bool(s.serpapi_api_key),
        "serper_key_loaded": bool(s.serper_api_key),
        "gemini_key_loaded": bool(s.gemini_api_key),
        "env_file_expected": str(Path(__file__).resolve().parent.parent / ".env"),
        "live_error": live_catalog.LAST_ERROR or None,
    }
@app.get("/",response_class=HTMLResponse)
def index(req:Request): return templates.TemplateResponse("index.html",{"request":req})
@app.get("/login",response_class=HTMLResponse)
def login(req:Request): return templates.TemplateResponse("login.html",{"request":req})
@app.get("/register",response_class=HTMLResponse)
def register(req:Request): return templates.TemplateResponse("register.html",{"request":req})
@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(req:Request): return templates.TemplateResponse("dashboard.html",{"request":req})
@app.get("/planner/{kind}",response_class=HTMLResponse)
def planner(req:Request,kind:str):
    if kind not in {"home","party","jewelry"}: raise HTTPException(404,"Planner not found.")
    return templates.TemplateResponse(f"{kind}.html",{"request":req})
