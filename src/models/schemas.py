"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional


class MatchState(BaseModel):
    """Input schema for the /api/strategize endpoint."""
    live: bool = False
    captain_side: Optional[str] = "batting"  # "batting" or "bowling"
    innings: Optional[int] = 1
    over: Optional[int] = 0
    ball: Optional[int] = 0
    current_score: Optional[int] = 0
    wickets: Optional[int] = 0
    team_batting: Optional[str] = "Unknown"
    team_bowling: Optional[str] = "Unknown"
    striker: Optional[str] = "Unknown"
    non_striker: Optional[str] = "Unknown"
    bowlers_remaining: dict = Field(default_factory=dict)
    pitch_conditions: Optional[str] = "Unknown"
    venue: Optional[str] = "Unknown"
    target: Optional[int] = None
    impact_player_available: Optional[bool] = False
