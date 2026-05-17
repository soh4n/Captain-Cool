"""API routes for match data (non-AI endpoints)."""

from fastapi import APIRouter
from src.services.cricket_api import get_live_match_state, get_ipl_matches, get_match_scorecard

router = APIRouter(prefix="/api", tags=["matches"])


@router.get("/matches")
def list_ipl_matches():
    """Returns all live and recent IPL matches."""
    return get_ipl_matches()


@router.get("/match/{match_id}")
def match_scorecard(match_id: int):
    """Returns detailed scorecard for a specific match."""
    return get_match_scorecard(match_id)


@router.get("/live")
def live_match():
    """Returns the current live IPL match state."""
    return get_live_match_state()
