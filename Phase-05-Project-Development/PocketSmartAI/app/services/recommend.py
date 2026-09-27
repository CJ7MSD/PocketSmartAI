import json
from app.catalog import search,product_url
from app.schemas import RecommendationResult,RecommendationItem
from app.config import get_settings
from app.services.live_catalog import search_live
from app.services import live_catalog

def fallback(kind,d):
    if kind=="home":
        tags=d["rooms"]+[d["style"]]+d.get("items",[]); cats=["lighting","furniture","decor","appliance"]
        title="Balanced Home Interior Plan"; summary=f"A {d['style']} setup for {', '.join(d['rooms'])}."
        alloc={"furniture":d["budget"]*.45,"lighting":d["budget"]*.2,"decor":d["budget"]*.2,"flexible":d["budget"]*.15}
    elif kind=="party":
        tags=[d["event_type"],"food","decor","venue"]; cats=["catering","venue","decoration"]
        title=f"{d['event_type'].title()} Budget Plan"; summary=f"A starter allocation for {d['guest_count']} guests."
        alloc={"catering":d["budget"]*.5,"venue":d["budget"]*.25,"decoration":d["budget"]*.15,"contingency":d["budget"]*.1}
    else:
        tags=[d["occasion"],d["style"],"elegant"]; cats=["necklace","earrings","necklace set","bracelet"]
        title=f"Jewelry Suggestions for {d['occasion'].title()}"; summary=f"Options emphasizing {d['style']} styling."
        alloc={"primary_piece":d["budget"]*.55,"earrings":d["budget"]*.25,"flexible":d["budget"]*.2}
    chosen=search(tags,cats); items=[]; total=0
    for x in chosen:
        qty=1
        if kind=="party" and x.category=="catering": qty=min(d["guest_count"],50)
        if total+x.price*qty <= d["budget"]*.92:
            items.append(RecommendationItem(name=x.name,category=x.category,platform=x.platform,price=x.price,quantity=qty,reason="Demo catalog match for your budget and preferences.",url=product_url(x))); total+=x.price*qty
        if len(items)>=6: break
    return RecommendationResult(planner_type=kind,title=title,summary=summary,budget=d["budget"],estimated_total=round(total,2),budget_remaining=round(d["budget"]-total,2),allocation=alloc,items=items,notes=["Demo catalog mode is active because no live provider result was used.","Verify current price and availability with the provider before purchasing."],source_mode="fallback")

def _requested_home_quantities(data):
    import re
    out = {}
    for raw in data.get("items", []) or []:
        text = str(raw).strip()
        m = re.search(r"\s*\(quantity:\s*(\d+)\)\s*$", text, re.I)
        if m:
            name = text[:m.start()].strip().lower()
            qty = max(1, min(50, int(m.group(1))))
        else:
            name, qty = text.lower(), 1
        if name:
            out[name] = qty
    return out

def _live_result(kind,d,live):
    if not live:
        return None
    budget=float(d["budget"])
    requested = _requested_home_quantities(d) if kind == "home" else {}
    items=[]
    total=0
    notes=[
        "Live provider mode is active.",
        "Each requested home item is searched separately so one product category does not replace the others.",
        "Prices, stock and delivery can change after this result is generated.",
        "Open the provider link to verify the current listing before purchase."
    ]

    if kind == "home" and requested:
        # Keep one product for EVERY requested item type. Prefer the cheapest
        # live listing for each item so adding more item types does not make
        # earlier/later items disappear just because the first listing was costly.
        groups = {name: [] for name in requested}
        for x in live:
            key = (x.requested_item or "").strip().lower()
            if key in groups:
                groups[key].append(x)

        for name, qty in requested.items():
            candidates = groups.get(name, [])
            if not candidates:
                continue
            candidates = sorted(candidates, key=lambda x: (x.price * qty, x.price, x.name.lower()))
            # Choose the cheapest live listing. We intentionally do not drop
            # the item when it exceeds the total budget; the user explicitly
            # requested that item and should see the real price instead of a
            # misleadingly incomplete plan.
            x = candidates[0]
            line_total = x.price * qty
            items.append(RecommendationItem(
                name=x.name,
                category=x.category,
                platform=x.platform,
                price=x.price,
                quantity=qty,
                reason=f"Live result for {name} ({qty} requested).",
                url=x.url
            ))
            total += line_total
            if line_total > budget:
                notes.append(f"{name.title()} is above the available budget at the requested quantity; consider a lower-cost listing or quantity.")

        missing = [name for name in requested if not any(
            (i.reason.lower().startswith(f"live result for {name.lower()} ")) for i in items
        )]
        if missing:
            notes.append("No usable live listing was returned for: " + ", ".join(missing) + ".")

    else:
        # For non-home planners, keep a useful set of distinct live results.
        seen = set()
        for x in sorted(live, key=lambda v: v.price):
            key = (x.url.lower().strip(), x.name.lower().strip())
            if key in seen:
                continue
            seen.add(key)
            items.append(RecommendationItem(
                name=x.name, category=x.category, platform=x.platform,
                price=x.price, quantity=1,
                reason="Live shopping result matched to your planner request.",
                url=x.url
            ))
            total += x.price
            if len(items) >= 8:
                break

    if not items:
        return None

    return RecommendationResult(
        planner_type=kind,
        title="Live Budget Recommendation",
        summary=(
            f"Live products selected for {len(requested)} requested item types."
            if kind == "home" and requested
            else "Recommendations assembled from live shopping results available at request time."
        ),
        budget=budget, estimated_total=round(total,2),
        budget_remaining=round(budget-total,2),
        allocation={}, items=items, notes=notes, source_mode="live"
    )

def generate(kind,d,image_bytes=None,mime=None):
    s=get_settings()
    # Query the live provider once. Repeating the same search can consume credits and
    # can cause the second call to fail/rate-limit, which previously forced a demo result.
    catalog_live=search_live(kind,d) if s.live_recommendations and (s.serpapi_api_key or s.serper_api_key) else []
    live=_live_result(kind,d,catalog_live)

    if live and not s.gemini_api_key:
        return live
    if not s.gemini_api_key:
        return fallback(kind,d)

    try:
        from google import genai
        from google.genai import types
        catalog = catalog_live
        if not catalog:
            demo=search(
                (d.get("rooms",[])+[d.get("style","")]+d.get("items",[]))
                if kind=="home" else
                ([d.get("event_type","")] if kind=="party" else [d.get("occasion","")+" "+d.get("style","")]),
                {"home":["lighting","furniture","decor","appliance"],
                 "party":["catering","venue","decoration"],
                 "jewelry":["necklace","earrings","necklace set","bracelet"]}[kind]
            )
            catalog_text="\n".join(f"{x.name} | {x.category} | {x.platform} | INR {x.price} | {product_url(x)}" for x in demo)
        else:
            catalog_text="\n".join(f"{x.name} | {x.category} | {x.platform} | INR {x.price} | {x.url}" for x in catalog)
        prompt=("You are PocketSmart AI. Use ONLY the catalog below. Do not invent prices, availability, reviews, ratings or URLs. "
                "Respect the total budget and return valid JSON matching the requested schema. Estimated total must equal price*quantity. "
                f"Planner={kind}\nUser={json.dumps(d)}\nCatalog:\n{catalog_text}")
        contents=[prompt]
        if image_bytes and mime:
            contents=[types.Part.from_bytes(data=image_bytes,mime_type=mime),prompt]
        # Gemini structured output supports a subset of JSON Schema. A free-form
        # Pydantic dict[str, float] becomes an additionalProperties schema, which
        # can be rejected by some Gemini API/model combinations. Use an explicit
        # array for allocation in the Gemini schema, then convert it back to the
        # UI's dictionary shape after validation.
        gemini_schema = {
            "type": "object",
            "properties": {
                "planner_type": {"type": "string", "enum": ["home", "party", "jewelry"]},
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "budget": {"type": "number"},
                "estimated_total": {"type": "number"},
                "budget_remaining": {"type": "number"},
                "allocation": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "amount": {"type": "number"}
                        },
                        "required": ["category", "amount"]
                    }
                },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "category": {"type": "string"},
                            "platform": {"type": "string"},
                            "price": {"type": "number"},
                            "quantity": {"type": "integer"},
                            "reason": {"type": "string"},
                            "url": {"type": "string"}
                        },
                        "required": ["name", "category", "platform", "price", "quantity", "reason", "url"]
                    }
                },
                "notes": {"type": "array", "items": {"type": "string"}},
                "source_mode": {"type": "string", "enum": ["live", "gemini", "fallback"]}
            },
            "required": ["planner_type", "title", "summary", "budget", "estimated_total", "budget_remaining", "allocation", "items", "notes", "source_mode"]
        }
        r=genai.Client(api_key=s.gemini_api_key).models.generate_content(
            model=s.gemini_model, contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=gemini_schema, temperature=0.3
            )
        )
        raw=json.loads(r.text)
        raw["allocation"]={x["category"]: float(x["amount"]) for x in raw.get("allocation", [])}
        result=RecommendationResult.model_validate(raw)
        if catalog_live:
            result.notes.append("Live shopping data was supplied to the AI layer.")
            result.source_mode="live"
        else:
            result.notes.append("Gemini is connected, but no live shopping results were returned; demo catalog data was used.")
            result.source_mode="gemini"
        return result
    except Exception as exc:
        # Never silently turn a real API failure into an unexplained demo result.
        if live:
            live.notes.append(f"Gemini ranking failed; showing live provider results directly. Error: {type(exc).__name__}")
            return live
        fallback_result=fallback(kind,d)
        fallback_result.notes.insert(0, f"Live/Gemini generation failed: {type(exc).__name__}: {str(exc)[:240]}")
        return fallback_result
