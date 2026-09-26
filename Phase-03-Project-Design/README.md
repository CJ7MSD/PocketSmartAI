# Phase 03 – Project Design

Project: **PocketSmart AI – Your Smart Budget & Recommendation Assistant**

## 1. System Architecture

Browser UI → FastAPI routes → planner/recommendation services → Gemini AI and live shopping provider → database/history → structured response → browser UI.

## 2. Main Components

Frontend templates and static assets; FastAPI application; authentication/session layer; planner routes; recommendation service; live catalog service; database/models; configuration/environment layer.

## 3. Planner Design

Home Planner: furniture, decor and lighting with budget and item quantities. Party Planner: event details, guest count, food/venue/decor requirements. Jewelry Planner: occasion/outfit and optional image input.

## 4. Authentication Design

/register creates an account; /login authenticates the user and establishes a session; /logout terminates the session; session information is used to protect and personalize application features.

## 5. Data Flow

User input → validation → planner route → recommendation service → AI/provider calls → normalize results → return structured response → render cards in the UI → optionally persist history.

## 6. UI/UX Design

Consistent navigation, centered authentication branding, separate authentication pages without the main navbar, stable Login/Logout styling, responsive planner forms, quantity controls and product recommendation cards.

## 7. Design Diagram

See architecture.md in this folder for a Mermaid diagram that can be rendered in GitHub.

