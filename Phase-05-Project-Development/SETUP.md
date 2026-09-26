# PocketSmart AI – Setup Guide

Project: **PocketSmart AI – Your Smart Budget & Recommendation Assistant**

## Prerequisites

Python 3.x and internet access for Gemini/SerpApi integration.

## Environment

Copy `.env.example` to `.env` and add your own API keys. Never publish `.env`.

## Install

Run `pip install -r requirements.txt`.

## Run

Run `uvicorn app.main:app --reload`.

## Open

Open the local application URL shown by Uvicorn.

## API Keys

Use a Gemini API key for Gemini and a SerpApi private key for Google Shopping. Provider credentials are separate.

