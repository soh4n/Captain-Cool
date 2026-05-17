"""Captain Cool — Multi-Agent IPL Match Strategist.

Entry point for the FastAPI application.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.core.config import APP_TITLE, CORS_ORIGINS
from src.api.matches import router as matches_router
from src.api.strategize import router as strategize_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Route registration ───────────────────────────────────────
app.include_router(matches_router)
app.include_router(strategize_router)

# ── Serve frontend static files ──────────────────────────────
app.mount("/", StaticFiles(directory=str(BASE_DIR / "frontend"), html=True), name="frontend")
