"""Core configuration module loads environment variables and app settings."""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ─────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

# ── Gemini Model Config ──────────────────────────────────────
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")

# ── API Base URLs ────────────────────────────────────────────
CRICBUZZ_BASE = "https://cricbuzz-cricket.p.rapidapi.com"
CRICBUZZ_HEADERS = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY,
}

# ── App Settings ─────────────────────────────────────────────
APP_TITLE = "Captain Cool API"
CORS_ORIGINS = ["*"]
