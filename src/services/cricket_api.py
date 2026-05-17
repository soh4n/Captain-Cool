"""Cricket data service for live scores, match lists, and scorecards."""

import requests
from src.core.config import CRICBUZZ_BASE, CRICBUZZ_HEADERS


def get_venue_weather(city: str) -> dict:
    """Fetches real-time weather and calculates potential dew factor for a given city.

    Args:
        city (str): The name of the city where the match is taking place (e.g. 'Mumbai', 'Chennai').

    Returns:
        dict: A dictionary containing temperature, humidity, and a calculated dew_factor.
    """
    try:
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        res = requests.get(geocode_url).json()
        if not res.get("results"):
            return {"error": "City not found", "dew_factor": "Unknown"}

        lat = res["results"][0]["latitude"]
        lon = res["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,is_day,wind_speed_10m&timezone=auto"
        weather_res = requests.get(weather_url).json()

        current = weather_res.get("current", {})
        temp = current.get("temperature_2m", 25)
        humidity = current.get("relative_humidity_2m", 50)
        is_day = current.get("is_day", 1)

        dew_factor = "High" if humidity > 70 and not is_day else "Medium" if humidity > 50 and not is_day else "Low"

        return {
            "city": city,
            "temperature_c": temp,
            "humidity_percent": humidity,
            "is_day": bool(is_day),
            "dew_factor": dew_factor,
            "analysis": f"With a humidity of {humidity}% {'at night' if not is_day else 'during the day'}, the dew factor is expected to be {dew_factor}.",
        }
    except Exception as e:
        return {"error": str(e), "dew_factor": "Unknown"}


def calculate_win_probability(
    target: int,
    current_score: int,
    wickets_lost: int,
    balls_bowled: int,
) -> dict:
    """Calculates a rudimentary win probability based on the match state.

    Args:
        target (int): Target score to win. (Provide a high number if 1st innings to estimate par)
        current_score (int): Current runs scored.
        wickets_lost (int): Number of wickets fallen (0-10).
        balls_bowled (int): Total balls bowled in the innings (max 120).

    Returns:
        dict: Win probability and required run rate.
    """
    balls_remaining = 120 - balls_bowled
    if balls_remaining <= 0:
        return {"win_probability": 0 if current_score < target else 100, "status": "Match Over"}

    runs_needed = target - current_score
    if runs_needed <= 0:
        return {"win_probability": 100, "status": "Target Reached"}

    rrr = (runs_needed / balls_remaining) * 6
    crr = (current_score / balls_bowled) * 6 if balls_bowled > 0 else 0

    base_prob = 50
    if rrr > 12:
        base_prob -= 30
    elif rrr > 10:
        base_prob -= 15
    elif rrr < 6:
        base_prob += 20
    elif rrr < 8:
        base_prob += 10

    if wickets_lost < 3:
        base_prob += 15
    elif wickets_lost > 7:
        base_prob -= 30
    elif wickets_lost > 5:
        base_prob -= 15

    prob = max(1, min(99, base_prob))

    return {
        "win_probability_percent": prob,
        "required_run_rate": round(rrr, 2),
        "current_run_rate": round(crr, 2),
        "analysis": f"Batting team has a {prob}% chance of winning. They need {runs_needed} runs from {balls_remaining} balls at {round(rrr, 2)} RPO.",
    }


def _find_ipl_match(res: dict):
    """Scan a Cricbuzz typeMatches response and return the first IPL match info."""
    if "typeMatches" not in res:
        return None, {}
    for t in res["typeMatches"]:
        for series in t.get("seriesMatches", []):
            if "seriesAdWrapper" in series:
                for match in series["seriesAdWrapper"].get("matches", []):
                    m_info = match.get("matchInfo", {})
                    s_name = m_info.get("seriesName", "").lower()
                    if "ipl" in s_name or "indian premier league" in s_name:
                        return m_info.get("matchId"), m_info
    return None, {}


def get_live_match_state() -> dict:
    """Fetches the live match state of the currently active IPL match from Cricbuzz.

    Returns:
        dict: The live match state including venue, team names, current score, and batter/bowler details.
    """
    try:
        if not CRICBUZZ_HEADERS["x-rapidapi-key"]:
            return {"error": "RAPIDAPI_KEY environment variable is not set."}

        endpoints = [
            f"{CRICBUZZ_BASE}/matches/v1/live",
            f"{CRICBUZZ_BASE}/matches/v1/recent",
        ]

        match_id, match_info = None, {}
        for url in endpoints:
            res = requests.get(url, headers=CRICBUZZ_HEADERS).json()
            match_id, match_info = _find_ipl_match(res)
            if match_id:
                break

        if not match_id:
            return {"error": "No live or recent IPL matches found."}

        score_url = f"{CRICBUZZ_BASE}/mcenter/v1/{match_id}/comm"
        score_res = requests.get(score_url, headers=CRICBUZZ_HEADERS).json()
        miniscore = score_res.get("miniscore", {})

        team_batting = match_info.get("team1", {}).get("teamName", "")
        if match_info.get("currBatTeamId") == match_info.get("team2", {}).get("teamId"):
            team_batting = match_info.get("team2", {}).get("teamName", "")

        team_bowling = match_info.get("team2", {}).get("teamName", "")
        if team_batting == match_info.get("team2", {}).get("teamName", ""):
            team_bowling = match_info.get("team1", {}).get("teamName", "")

        return {
            "match_id": match_id,
            "status": match_info.get("status", ""),
            "match_format": match_info.get("matchFormat", ""),
            "venue": match_info.get("venueInfo", {}).get("city", "Unknown Venue"),
            "team_batting": team_batting,
            "team_bowling": team_bowling,
            "target": miniscore.get("target", 0),
            "striker": miniscore.get("batsmanstriker", {}).get("name", ""),
            "striker_runs": miniscore.get("batsmanstriker", {}).get("runs", 0),
            "striker_balls": miniscore.get("batsmanstriker", {}).get("balls", 0),
            "non_striker": miniscore.get("batsmannonstriker", {}).get("name", ""),
            "bowler": miniscore.get("bowlerstriker", {}).get("name", ""),
            "crr": miniscore.get("crr", "0"),
            "rrr": miniscore.get("rrr", "0"),
            "recent_overs": miniscore.get("recentOvsStats", ""),
        }
    except Exception as e:
        return {"error": f"Failed to fetch live match state: {str(e)}"}


def get_ipl_matches() -> list:
    """Fetches all recent and live IPL matches from Cricbuzz.

    Returns:
        list: A list of IPL match summary dicts.
    """
    try:
        if not CRICBUZZ_HEADERS["x-rapidapi-key"]:
            return [{"error": "RAPIDAPI_KEY environment variable is not set."}]

        matches = []
        endpoints = [
            f"{CRICBUZZ_BASE}/matches/v1/live",
            f"{CRICBUZZ_BASE}/matches/v1/recent",
        ]
        seen_ids = set()

        for url in endpoints:
            res = requests.get(url, headers=CRICBUZZ_HEADERS).json()
            if "typeMatches" in res:
                for t in res["typeMatches"]:
                    for series in t.get("seriesMatches", []):
                        if "seriesAdWrapper" in series:
                            for match in series["seriesAdWrapper"].get("matches", []):
                                m_info = match.get("matchInfo", {})
                                s_name = m_info.get("seriesName", "").lower()
                                if "ipl" in s_name or "indian premier league" in s_name:
                                    mid = m_info.get("matchId")
                                    if mid and mid not in seen_ids:
                                        seen_ids.add(mid)
                                        team1 = m_info.get("team1", {})
                                        team2 = m_info.get("team2", {})
                                        matches.append({
                                            "match_id": mid,
                                            "series": m_info.get("seriesName", ""),
                                            "match_desc": m_info.get("matchDesc", ""),
                                            "status": m_info.get("status", ""),
                                            "state": m_info.get("state", ""),
                                            "venue": m_info.get("venueInfo", {}).get("ground", ""),
                                            "city": m_info.get("venueInfo", {}).get("city", ""),
                                            "team1_name": team1.get("teamName", ""),
                                            "team1_sname": team1.get("teamSName", ""),
                                            "team2_name": team2.get("teamName", ""),
                                            "team2_sname": team2.get("teamSName", ""),
                                            "match_format": m_info.get("matchFormat", "T20"),
                                        })
        return matches
    except Exception as e:
        return [{"error": str(e)}]


def get_match_scorecard(match_id: int) -> dict:
    """Fetches the full scorecard and match details for a specific match ID.

    Args:
        match_id: The Cricbuzz match ID.

    Returns:
        dict: Scorecard details including innings scores, current batsmen, bowlers, and match state.
    """
    try:
        if not CRICBUZZ_HEADERS["x-rapidapi-key"]:
            return {"error": "RAPIDAPI_KEY environment variable is not set."}

        score_url = f"{CRICBUZZ_BASE}/mcenter/v1/{match_id}/comm"
        score_res = requests.get(score_url, headers=CRICBUZZ_HEADERS).json()
        miniscore = score_res.get("miniscore", {})
        match_header = score_res.get("matchHeader", {})

        innings_scores = []
        for inn in match_header.get("matchTeamInfo", []):
            b_team = inn.get("battingTeamShortName", "")
            innings_scores.append({
                "team": b_team,
                "score": f"{inn.get('battingTeamScore', {}).get('inngs1', {}).get('runs', '?')}/{inn.get('battingTeamScore', {}).get('inngs1', {}).get('wickets', '?')}",
                "overs": inn.get("battingTeamScore", {}).get("inngs1", {}).get("overs", "?"),
            })

        striker = miniscore.get("batsmanstriker", {})
        non_striker = miniscore.get("batsmannonstriker", {})
        bowler = miniscore.get("bowlerstriker", {})
        bowler_ns = miniscore.get("bowlernonstriker", {})

        return {
            "match_id": match_id,
            "status": match_header.get("status", ""),
            "state": match_header.get("state", ""),
            "toss": match_header.get("tossResults", {}).get("tossWinnerName", ""),
            "toss_decision": match_header.get("tossResults", {}).get("decision", ""),
            "innings_scores": innings_scores,
            "crr": miniscore.get("crr", "0"),
            "rrr": miniscore.get("rrr", "0"),
            "target": miniscore.get("target", 0),
            "partnership": f"{miniscore.get('partnership', {}).get('runs', 0)}({miniscore.get('partnership', {}).get('balls', 0)})",
            "recent_overs": miniscore.get("recentOvsStats", ""),
            "striker": {
                "name": striker.get("name", ""), "runs": striker.get("runs", 0),
                "balls": striker.get("balls", 0), "fours": striker.get("fours", 0),
                "sixes": striker.get("sixes", 0), "sr": striker.get("strkRate", "0"),
            },
            "non_striker": {
                "name": non_striker.get("name", ""), "runs": non_striker.get("runs", 0),
                "balls": non_striker.get("balls", 0), "fours": non_striker.get("fours", 0),
                "sixes": non_striker.get("sixes", 0), "sr": non_striker.get("strkRate", "0"),
            },
            "bowler": {
                "name": bowler.get("name", ""), "overs": bowler.get("overs", "0"),
                "runs": bowler.get("runs", 0), "wickets": bowler.get("wickets", 0),
                "economy": bowler.get("economy", "0"),
            },
            "bowler_ns": {
                "name": bowler_ns.get("name", ""), "overs": bowler_ns.get("overs", "0"),
                "runs": bowler_ns.get("runs", 0), "wickets": bowler_ns.get("wickets", 0),
                "economy": bowler_ns.get("economy", "0"),
            },
        }
    except Exception as e:
        return {"error": f"Failed to fetch scorecard: {str(e)}"}
