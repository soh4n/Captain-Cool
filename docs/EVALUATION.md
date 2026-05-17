# Evaluation Guide

This guide maps repository evidence to the areas a hackathon or portfolio reviewer is likely to inspect.

## Relevance

Captain Cool stays inside cricket strategy instead of presenting a generic chatbot shell.

- Inputs model T20 match state: innings, over, score, wickets, target, venue, pitch, striker, non-striker, and bowling resources.
- Prompts force captain-side perspective: batting captain and bowling captain receive different tactical scopes.
- The final answer is phrased for cricket operators and fans, not model developers.

## Technical Depth

- FastAPI backend with typed Pydantic request schema.
- Gemini orchestration with separate calls for analyst, strategist, critic, and final decision roles.
- Function-tool use for weather/dew context and win-probability calculation.
- Cricbuzz RapidAPI integration for live/recent IPL match context.
- Optional Google ADK agent scaffold that reuses core tools.

## Agentic Design

The visible debate is the strongest differentiator:

| Step | Agent | Why It Matters |
| --- | --- | --- |
| 1 | Stats Analyst Gamma | Separates evidence gathering from decision-making |
| 2 | Strategist Alpha | Forces one committed next-over tactical call |
| 3 | Devil's Advocate Beta | Adds adversarial review before final answer |
| 4 | Strategist Alpha Final | Requires defend-or-revise behavior |

## Repository Quality

- `README.md` gives setup, architecture, endpoint, and verification output.
- `docs/architecture.md` explains runtime flow and agent roles.
- `docs/API_REFERENCE.md` documents endpoint contracts.
- `docs/DEMO_SCRIPT.md` gives a repeatable evaluator walkthrough.
- `.github/workflows/ci.yml` runs compile and tests across Python 3.10-3.12.
- Issue and PR templates make the repository look maintained and reviewable.
- `SECURITY.md`, `CHANGELOG.md`, and `ROADMAP.md` cover operational maturity.

## Honest Limitations

- Gemini calls require a valid `GEMINI_API_KEY`.
- Live IPL data requires `RAPIDAPI_KEY`.
- Win probability is intentionally simple and should be treated as tactical context, not a betting model.
- The current History view is frontend-facing; long-term persistence is listed on the roadmap.
