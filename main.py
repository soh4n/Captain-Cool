"""Captain Cool - Multi-Agent IPL Match Strategist.

Entry point for the FastAPI application.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.matches import router as matches_router
from src.api.strategize import router as strategize_router
from src.core.config import APP_TITLE, CORS_ORIGINS

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["health"])
def health_check():
    """Return a lightweight readiness signal for demos, CI, and hosting probes."""
    return {
        "status": "ok",
        "app": APP_TITLE,
        "frontend": "mounted",
    }


app.include_router(matches_router)
app.include_router(strategize_router)

app.mount("/", StaticFiles(directory=str(BASE_DIR / "frontend"), html=True), name="frontend")
