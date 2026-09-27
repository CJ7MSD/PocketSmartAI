"""Live shopping provider integration for PocketSmart AI."""
from __future__ import annotations
import re
import requests
from dataclasses import dataclass
from app.config import get_settings

LAST_ERROR = ""
LAST_STATUS = "not_tested"
LAST_RESULT_COUNT = 0

@dataclass(frozen=True)
class LiveItem:
    name: str
    category: str
    platform: str
    price: float
    url: str
    source: str = "live"
    requested_item: str = ""

def _money(value):
    if isinstance(value, (int, float)):
        return float(value)
    if not value:
        return None
    cleaned = str(value).replace(",", "")
    digits = "".join(ch for ch in cleaned if ch.isdigit() or ch == ".")
    try:
        return float(digits) if digits else None
    except ValueError:
        return None

def _parse_home_item(value: str):
    """Parse 'ceiling lights (quantity: 10)' into ('ceiling lights', 10)."""
    text = str(value or "").strip()
    m = re.search(r"\s*\(quantity:\s*(\d+)\)\s*$", text, re.I)
    if m:
        qty = max(1, min(50, int(m.group(1))))
        name = text[:m.start()].strip()
        return name, qty
    return text, 1

def _item_category(name: str) -> str:
    n = name.lower()
    if any(x in n for x in ("light", "lamp", "bulb")):
        return "lighting"
    if any(x in n for x in ("fan", "ac", "air conditioner", "appliance")):
        return "appliance"
    if any(x in n for x in ("sofa", "bed", "table", "chair", "wardrobe", "cabinet", "shelf", "desk")):
        return "furniture"
    if any(x in n for x in ("curtain", "rug", "carpet", "decor", "wall", "mirror", "cushion", "pillow")):
        return "decor"
    return "home"

def shopping_search(query: str, category: str, limit: int = 8, requested_item: str = "") -> list[LiveItem]:
    global LAST_ERROR, LAST_STATUS, LAST_RESULT_COUNT
    LAST_ERROR = ""
    LAST_STATUS = "requesting"
    LAST_RESULT_COUNT = 0
    s = get_settings()
    if not s.live_recommendations:
        LAST_STATUS = "disabled"
        LAST_ERROR = "LIVE_RECOMMENDATIONS is disabled."
        return []
    api_key = s.serpapi_api_key or s.serper_api_key
    if not api_key:
        LAST_STATUS = "not_configured"
        LAST_ERROR = "SERPAPI_API_KEY was not loaded from the environment."
        return []
    try:
        r = requests.get(
            "https://serpapi.com/search",
            params={
                "engine": "google_shopping",
                "api_key": api_key,
                "q": query,
                "gl": "in",
                "hl": "en",
                "num": limit,
            },
            timeout=20,
        )
        if r.status_code >= 400:
            LAST_STATUS = "http_error"
            try:
                detail = r.json()
            except Exception:
                detail = r.text[:500]
            LAST_ERROR = f"SerpApi HTTP {r.status_code}: {detail}"
            return []
        payload = r.json()
        rows = payload.get("shopping_results", []) or []
        if not rows:
            LAST_STATUS = "no_results"
            LAST_ERROR = f"SerpApi returned no shopping results. Response keys: {list(payload.keys())}"
            return []
    except requests.RequestException as exc:
        LAST_STATUS = "request_error"
        LAST_ERROR = f"SerpApi request failed: {exc}"
        return []
    except ValueError as exc:
        LAST_STATUS = "invalid_json"
        LAST_ERROR = f"Invalid SerpApi JSON response: {exc}"
        return []

    out = []
    for x in rows:
        price = _money(x.get("extracted_price"))
        if price is None:
            price = _money(x.get("price"))
        link = x.get("product_link") or x.get("link") or x.get("productLink")
        name = x.get("title")
        if not name or price is None or not link:
            continue
        source = x.get("source") or "Google Shopping"
        out.append(LiveItem(
            name=name,
            category=category,
            platform=source,
            price=price,
            url=link,
            requested_item=requested_item,
        ))
    LAST_RESULT_COUNT = len(out)
    if out:
        LAST_STATUS = "ok"
        LAST_ERROR = ""
    else:
        LAST_STATUS = "invalid_results"
        LAST_ERROR = "SerpApi returned shopping rows, but none had usable title, price and link fields."
    return out

def _home_search_term(item_name: str) -> str:
    """Turn UI item values into a useful Google Shopping search phrase."""
    aliases = {
        "lights": "ceiling lights",
        "fans": "ceiling fans",
        "dining table": "dining table",
        "sofa": "sofa",
        "bed": "bed",
        "wardrobe": "wardrobe",
        "curtains": "curtains",
        "wall decor": "wall decor",
        "rug": "rug",
        "side table": "side table",
    }
    return aliases.get(item_name.strip().lower(), item_name.strip())


def _search_home_item(style: str, item_name: str, qty: int) -> list[LiveItem]:
    """Search an item with a primary query and a broader fallback query.

    A single unsuccessful/overly-specific query should not make a selected
    item disappear from the final plan.
    """
    term = _home_search_term(item_name)
    category = _item_category(term)
    queries = [
        f"{style} {term} India",
        f"{term} India",
        f"{term} home India",
    ]
    found: list[LiveItem] = []
    seen = set()
    for query in queries:
        batch = shopping_search(query, category, 8, requested_item=item_name)
        for x in batch:
            key = (x.url.lower().strip(), x.name.lower().strip())
            if key not in seen:
                seen.add(key)
                found.append(x)
        if len(found) >= 4:
            break
    return found


def search_live(kind: str, data: dict) -> list[LiveItem]:
    """Search each requested item separately and keep its own result pool."""
    if kind == "home":
        style = data.get("style", "modern")
        parsed = [_parse_home_item(x) for x in (data.get("items") or [])]
        result: list[LiveItem] = []

        if parsed:
            for item_name, qty in parsed:
                result.extend(_search_home_item(style, item_name, qty))
        else:
            rooms = ", ".join(data.get("rooms", []) or [])
            for category, term in [
                ("furniture", "furniture"),
                ("lighting", "ceiling lights"),
                ("decor", "home decor"),
                ("appliance", "home appliances"),
            ]:
                result.extend(shopping_search(f"{style} {term} {rooms} India", category, 6, requested_item=term))
    elif kind == "party":
        result = []
        base = f"{data.get('event_type','party')} party India"
        for category, term in [("catering", "catering"), ("venue", "venue"), ("decoration", "decoration")]:
            result.extend(shopping_search(f"{base} {term}", category, 6, requested_item=category))
    else:
        result = []
        base = f"{data.get('occasion','occasion')} {data.get('style','elegant')} jewelry India"
        for category in ["necklace", "earrings", "necklace set", "bracelet"]:
            result.extend(shopping_search(f"{base} {category}", category, 6, requested_item=category))

    seen = set()
    unique = []
    for x in result:
        key = (x.url.lower().strip(), x.name.lower().strip(), x.requested_item.lower().strip())
        if key in seen:
            continue
        seen.add(key)
        unique.append(x)
    return unique
