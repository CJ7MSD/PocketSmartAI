# Phase 02 – Requirement Analysis

Project: **PocketSmart AI – Your Smart Budget & Recommendation Assistant**

## 1. Functional Requirements

- User registration and login.
- Session-based authentication and logout.
- Home Interior recommendations.
- Party recommendations using guest count and event details.
- Jewelry recommendations using occasion/outfit information and optional image input.
- Budget-based recommendation generation.
- Live product search integration.
- Dashboard and recommendation history.
- Structured recommendation output.

## 2. Non-Functional Requirements

- Usable and responsive UI.
- Modular backend architecture.
- Secure handling of credentials and API keys.
- Reliable API error handling.
- Maintainable code structure.
- Reasonable response time for API-backed operations.

## 3. Technology Requirements

Python, FastAPI, Jinja2/HTML, CSS, JavaScript, SQLite/database layer, Gemini API, SerpApi/Google Shopping integration, Uvicorn and environment variables.

## 4. External API Requirements

Gemini API for AI generation and reasoning; SerpApi Google Shopping for live product information. API keys must be stored in environment variables and must not be committed to GitHub.

## 5. User Flow

Register → Login → Main Home Page → Select planner → Enter budget/preferences → Generate recommendation → Review live/AI results → Save/review through Dashboard/History.

## 6. Acceptance Criteria

A valid user can register and manually log in; authenticated users can access protected planners; each planner accepts its required inputs; recommendations are returned in structured form; live provider failures are handled without exposing secrets; dashboard/history can display saved recommendation data.

