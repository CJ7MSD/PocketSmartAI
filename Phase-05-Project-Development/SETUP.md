# PocketSmart AI – Setup Guide

Project: **PocketSmart AI – Your Smart Budget & Recommendation Assistant**

## Prerequisites

Python 3.x and internet access for Gemini/SerpApi integration.

## Environment

Copy `.env.example` to `.env` and add your own API keys. Never publish `.env`.

## Install

Create a virtual environment:

```powershell
py -m venv .venv

Install the required packages:

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Run

Start the application:

.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
Open

Open the local application URL shown by Uvicorn:

http://127.0.0.1:8000
API Keys

Use a Gemini API key for Gemini AI generation and a SerpApi API key for Google Shopping/live product data. Provider credentials are separate.

Add the keys to .env:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
SERPAPI_API_KEY=YOUR_SERPAPI_API_KEY

Never upload .env or your API keys to GitHub.