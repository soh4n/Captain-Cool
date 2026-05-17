# Runtime Agent Debate Trace

Captain Cool's runtime behavior is agentic because the decision is not produced by a single prompt. Each role receives its own system prompt and Gemini call.

## Agent 1: Stats Analyst Gamma

Purpose:

- Convert match state into a statistical brief.
- Call `get_venue_weather` for venue weather and dew context.
- Call `calculate_win_probability` for chase pressure and counterfactual context.

Temperature: `0.2`

## Agent 2: Strategist Alpha

Purpose:

- Read the match state and Gamma's brief.
- Propose one tactical call for the next over or decision point.
- Speak as the batting or bowling captain, depending on `captain_side`.

Temperature: `0.7`

## Agent 3: Devil's Advocate Beta

Purpose:

- Challenge Alpha's proposed call.
- Identify matchup, phase, dew, field, or resource-management risk.
- Offer the strongest alternative decision.

Temperature: `0.8`

## Final Turn: Strategist Alpha

Purpose:

- Directly respond to Beta's objection.
- Defend the initial plan or revise the call.
- Return structured JSON with decision, reasoning, dissent, and win-probability context.

## Visible Debate Output

The API returns:

- `analyst_report`
- `strategist_initial`
- `devils_advocate`
- `final_decision`

The frontend displays the trace so reviewers can inspect the collaboration.
