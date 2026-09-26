# Phase 05 – Project Development

Project: **PocketSmart AI – Your Smart Budget & Recommendation Assistant**

## 1. Implemented Stack

Python + FastAPI backend, Jinja2 templates, HTML/CSS/JavaScript frontend, database/session layer, Gemini AI integration and SerpApi live shopping integration.

## 2. Backend

The backend provides planner routes, authentication/session routes, recommendation logic, history handling, configuration and live catalog integration.

## 3. Frontend

The frontend contains the main page, Home Interior, Party, Jewelry, Login, Register, Dashboard and supporting recommendation/history views.

## 4. AI Integration

Gemini is used to interpret user requirements and produce structured recommendations. The implementation uses a schema compatible with the configured Gemini API.

## 5. Live Product Integration

SerpApi Google Shopping is used for live product discovery. Product fields are normalized so the UI can display usable titles, prices and links.

## 6. Security/Configuration

API keys are configured through environment variables. The repository copy intentionally excludes the real .env file.

## 7. Run Instructions

Create a virtual environment, install requirements.txt, configure .env from .env.example, then run `uvicorn app.main:app --reload`. Do not commit API keys.

