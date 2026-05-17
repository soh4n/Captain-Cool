"""API route for the multi-agent strategize debate."""

import json
from fastapi import APIRouter
from google import genai
from google.genai import types

from src.core.config import GEMINI_API_KEY, GEMINI_MODEL
from src.models.schemas import MatchState
from src.services.cricket_api import (
    get_venue_weather,
    calculate_win_probability,
    get_live_match_state,
    get_match_scorecard,
)
from src.services.agents import (
    analyst_prompt,
    strategist_prompt,
    devils_advocate_prompt,
    final_decision_prompt,
)

router = APIRouter(prefix="/api", tags=["strategize"])


@router.post("/strategize")
def strategize(state: MatchState):
    """Run the full multi-agent debate pipeline and return the tactical decision."""
    if not GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY environment variable is not set."}

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        return {"error": f"Failed to initialize Gemini Client: {str(e)}"}

    captain_side = state.captain_side or "batting"

    if state.live:
        live_data = get_live_match_state()
        if "error" in live_data:
            return {"error": live_data["error"]}

        captain_team = live_data.get("team_batting") if captain_side == "batting" else live_data.get("team_bowling")
        opponent_team = live_data.get("team_bowling") if captain_side == "batting" else live_data.get("team_batting")
        scorecard = get_match_scorecard(live_data.get("match_id", 0))

        state_str = f"""
Current LIVE Match State from Cricbuzz:
CAPTAIN'S PERSPECTIVE: You are the {captain_side.upper()} captain of {captain_team} against {opponent_team}.
Match Status: {live_data.get('status')}
Format: {live_data.get('match_format')}
Score (Recent Overs): {live_data.get('recent_overs')} (CRR: {live_data.get('crr')} RRR: {live_data.get('rrr')})
Batting: {live_data.get('team_batting')} (Striker: {live_data.get('striker')} - {live_data.get('striker_runs')}({live_data.get('striker_balls')}), Non-striker: {live_data.get('non_striker')})
Bowling: {live_data.get('team_bowling')} (Current Bowler: {live_data.get('bowler')})
Venue: {live_data.get('venue')}
Target: {live_data.get('target')}
Partnership: {scorecard.get('partnership', 'N/A')}
"""
    else:
        state_str = f"""
Current Match State:
Innings: {state.innings}
Over: {state.over}.{state.ball}
Score: {state.current_score}/{state.wickets}
Batting: {state.team_batting} (Striker: {state.striker}, Non-striker: {state.non_striker})
Bowling: {state.team_bowling}
Bowlers remaining (overs used): {state.bowlers_remaining}
Pitch: {state.pitch_conditions}
Venue: {state.venue}
Target: {state.target}
Impact Player Available: {state.impact_player_available}
"""

    analyst_response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=state_str + "\nPlease analyze the current match state. Be sure to call get_venue_weather for the venue, and calculate_win_probability.",
        config=types.GenerateContentConfig(
            system_instruction=analyst_prompt(captain_side),
            tools=[get_venue_weather, calculate_win_probability],
            temperature=0.2,
        ),
    )
    analyst_output = analyst_response.text

    strategist_initial = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"Match State:\n{state_str}\n\nStats Analyst Report:\n{analyst_output}\n\nWhat is your proposed strategy for the next over?",
        config=types.GenerateContentConfig(
            system_instruction=strategist_prompt(captain_side),
            temperature=0.7,
        ),
    ).text

    da_response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"Match State:\n{state_str}\n\nStrategist's Plan:\n{strategist_initial}\n\nCritique this plan and propose an alternative.",
        config=types.GenerateContentConfig(
            system_instruction=devils_advocate_prompt(),
            temperature=0.8,
        ),
    ).text

    final_response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=final_decision_prompt(strategist_initial, da_response),
        config=types.GenerateContentConfig(
            system_instruction=strategist_prompt(captain_side),
            response_mime_type="application/json",
            temperature=0.7,
        ),
    ).text

    try:
        final_data = json.loads(final_response)
    except Exception:
        final_data = {
            "decision": "Error parsing decision",
            "reasoning": final_response,
            "dissent": da_response,
            "win_prob_context": "",
        }

    live_score_data = None
    if state.live:
        live_score_data = {
            "match_id": live_data.get("match_id"),
            "status": live_data.get("status"),
            "team_batting": live_data.get("team_batting"),
            "team_bowling": live_data.get("team_bowling"),
            "striker": live_data.get("striker"),
            "striker_runs": live_data.get("striker_runs"),
            "striker_balls": live_data.get("striker_balls"),
            "non_striker": live_data.get("non_striker"),
            "bowler": live_data.get("bowler"),
            "crr": live_data.get("crr"),
            "rrr": live_data.get("rrr"),
            "target": live_data.get("target"),
            "venue": live_data.get("venue"),
            "recent_overs": live_data.get("recent_overs"),
            "innings_scores": scorecard.get("innings_scores", []),
            "partnership": scorecard.get("partnership", "0(0)"),
        }

    return {
        "captain_side": captain_side,
        "live_score": live_score_data,
        "analyst_report": analyst_output,
        "strategist_initial": strategist_initial,
        "devils_advocate": da_response,
        "final_decision": final_data,
    }
