# API Reference

Base URL for local development:

```text
http://localhost:8000
```

## Health

`GET /api/health`

Returns a lightweight readiness response for local demos, CI smoke checks, and hosting probes.

```json
{
  "status": "ok",
  "app": "Captain Cool API",
  "frontend": "mounted"
}
```

## Strategy Debate

`POST /api/strategize`

Runs the complete Gemini debate loop:

1. Stats Analyst Gamma summarizes match state and calls tools.
2. Strategist Alpha proposes one next-over call.
3. Devil's Advocate Beta challenges the call.
4. Strategist Alpha defends or revises and returns final JSON.

### Manual Request

```json
{
  "live": false,
  "captain_side": "bowling",
  "innings": 2,
  "over": 15,
  "ball": 2,
  "current_score": 142,
  "wickets": 4,
  "team_batting": "CSK",
  "team_bowling": "MI",
  "striker": "Shivam Dube",
  "non_striker": "MS Dhoni",
  "bowlers_remaining": {
    "Bumrah": 1,
    "Hardik": 2,
    "Coetzee": 1
  },
  "pitch_conditions": "two-paced with medium dew",
  "venue": "Mumbai",
  "target": 188,
  "impact_player_available": true
}
```

### Response Shape

```json
{
  "captain_side": "bowling",
  "live_score": null,
  "analyst_report": "...",
  "strategist_initial": "...",
  "devils_advocate": "...",
  "final_decision": {
    "decision": "...",
    "reasoning": "...",
    "dissent": "...",
    "win_prob_context": "..."
  }
}
```

Requires `GEMINI_API_KEY`.

## Match Data

`GET /api/matches`

Returns live and recent IPL match summaries from Cricbuzz RapidAPI. Requires `RAPIDAPI_KEY`.

`GET /api/live`

Returns the first live or recent IPL match state that can be mapped into Captain Cool's strategy context. Requires `RAPIDAPI_KEY`.

`GET /api/match/{match_id}`

Returns scorecard details for a Cricbuzz match ID. Requires `RAPIDAPI_KEY`.
