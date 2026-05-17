# Captain Cool

[![CI](https://github.com/soh4n/Captain-Cool/actions/workflows/ci.yml/badge.svg)](https://github.com/soh4n/Captain-Cool/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-ASGI-009688)
![Gemini](https://img.shields.io/badge/Gemini-multi--agent-673ab7)
![License](https://img.shields.io/badge/license-MIT-green)

Captain Cool is a Gemini-powered IPL captaincy strategist that turns live match state into a clear tactical call. Instead of acting like a generic chatbot, it runs a visible debate between named agents, uses real tools for cricket context, and explains the final decision in language a captain, coach, or fan can understand.

Repository: `soh4n/Captain-Cool`

## Quick Links

- [Architecture](docs/architecture.md)
- [API reference](docs/API_REFERENCE.md)
- [Evaluation guide](docs/EVALUATION.md)
- [Demo script](docs/DEMO_SCRIPT.md)
- [Deployment notes](docs/DEPLOYMENT.md)
- [Quality checklist](docs/QUALITY_CHECKLIST.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

## Highlights

- Gemini multi-agent orchestration using `google-genai`.
- Optional Google ADK agent scaffold under `adk_agents/captain_cool`.
- Three named agents with distinct prompts: Stats Analyst Gamma, Strategist Alpha, and Devil's Advocate Beta.
- Function-tool use inside the analyst agent for weather/dew context and win-probability calculation.
- Multi-turn tactical loop: propose, challenge, defend or revise.
- Live/recent IPL support through Cricbuzz RapidAPI.
- Static frontend served by FastAPI with War Room, Insights, and History views.
- Repository evidence pack: architecture docs, API reference, evaluation guide, demo script, CI, issue templates, security notes, and prompt pack.

## Why This Repository Stands Out

| Reviewer Signal | Evidence In This Repo |
| --- | --- |
| Clear product idea | Cricket-specific captaincy strategist with match-state inputs, not a generic chat wrapper |
| Agentic design | Visible Gamma -> Alpha -> Beta -> Alpha debate loop with defend-or-revise behavior |
| Real tool use | Open-Meteo weather/dew lookup, win-probability helper, Cricbuzz RapidAPI integration |
| Working backend shape | FastAPI routes, typed Pydantic schema, static frontend mount, health endpoint |
| Evaluation readiness | Demo script, API reference, architecture notes, submission mapping, quality checklist |
| Maintenance polish | CI workflow, PR template, issue templates, changelog, roadmap, security policy |

## How It Works

```mermaid
graph TD
    A[Manual or Live Match State] --> B[Stats Analyst Gamma]
    B --> C[Tool Calls: Weather + Win Probability]
    C --> D[Strategist Alpha: Initial Plan]
    D --> E[Devil's Advocate Beta: Challenge]
    E --> F[Strategist Alpha: Defend or Revise]
    F --> G[Captain-Friendly Final Decision]
```

The app makes separate Gemini calls for each role. The debate trace is returned to the UI so reviewers can see the back-and-forth rather than only the final answer.

## Architecture Diagram

```mermaid
flowchart LR
    subgraph Client["Frontend"]
        WarRoom["AI War Room<br/>frontend/index.html"]
        Insights["Insights<br/>frontend/insights.html"]
        History["History<br/>frontend/history.html"]
    end

    subgraph API["FastAPI Backend"]
        Main["main.py"]
        Health["GET /api/health"]
        Strategize["POST /api/strategize"]
        Live["GET /api/live"]
        Matches["GET /api/matches"]
        Scorecard["GET /api/match/{match_id}"]
    end

    subgraph Services["Application Services"]
        AgentPrompts["Agent prompt templates<br/>src/services/agents.py"]
        CricketTools["Cricket and tool services<br/>src/services/cricket_api.py"]
        Schemas["MatchState schema<br/>src/models/schemas.py"]
        Config["Environment config<br/>src/core/config.py"]
    end

    subgraph Gemini["Gemini Multi-Agent Debate"]
        Gamma["Stats Analyst Gamma"]
        Alpha1["Strategist Alpha<br/>Initial proposal"]
        Beta["Devil's Advocate Beta"]
        Alpha2["Strategist Alpha<br/>Final decision"]
    end

    subgraph External["External APIs"]
        OpenMeteo["Open-Meteo<br/>weather/dew"]
        Cricbuzz["Cricbuzz RapidAPI<br/>live scores"]
        GeminiAPI["Google Gemini API<br/>gemini-2.5-pro"]
    end

    Client --> Main
    Main --> Health
    Main --> Strategize
    Main --> Live
    Main --> Matches
    Main --> Scorecard
    Strategize --> Schemas
    Strategize --> AgentPrompts
    Strategize --> CricketTools
    Live --> CricketTools
    Matches --> CricketTools
    Scorecard --> CricketTools
    Config --> Strategize
    Config --> CricketTools
    CricketTools --> OpenMeteo
    CricketTools --> Cricbuzz
    Strategize --> Gamma
    Gamma --> Alpha1
    Alpha1 --> Beta
    Beta --> Alpha2
    Gamma --> GeminiAPI
    Alpha1 --> GeminiAPI
    Beta --> GeminiAPI
    Alpha2 --> GeminiAPI
```

## Agent Roles

| Agent | Role | Output |
| --- | --- | --- |
| Stats Analyst Gamma | Reads the match state, fetches venue weather, estimates dew and win probability | Statistical brief |
| Strategist Alpha | Makes one committed tactical proposal from the captain's perspective | Initial next-over plan |
| Devil's Advocate Beta | Attacks the plan and proposes the strongest alternative | Dissent and risk case |
| Strategist Alpha Final | Responds to the critique, then defends or revises | Final decision JSON |

## Inputs

Captain Cool supports manual match-state input through the API and live-state mode through Cricbuzz:

- Innings, over, ball, score, wickets
- Batting team, bowling team, striker, non-striker
- Bowlers remaining and overs used
- Pitch conditions, venue, dew factor
- Target and required run rate for chases
- Impact Player availability
- Captain side: batting or bowling

## Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- `google-genai`
- Open-Meteo weather API
- Cricbuzz RapidAPI
- Static HTML, Tailwind CDN, Material Symbols

## Project Structure

```text
.
|-- main.py                       # FastAPI app entry point
|-- frontend/                     # Static UI screens
|-- src/
|   |-- api/                      # FastAPI routers
|   |-- core/                     # Configuration
|   |-- models/                   # Request schemas
|   |-- services/                 # Agents and cricket tools
|   `-- tests/                    # Unit tests
|-- docs/architecture.md          # Architecture notes
|-- docs/API_REFERENCE.md         # Endpoint contracts
|-- docs/EVALUATION.md            # Reviewer-facing rubric mapping
|-- docs/DEMO_SCRIPT.md           # Repeatable demo walkthrough
|-- docs/DEPLOYMENT.md            # Hosting notes
|-- docs/QUALITY_CHECKLIST.md     # Pre-submission checklist
|-- adk_agents/                   # Google ADK-compatible agent project
|-- AI_STUDIO_PROMPT.md           # Prompt prototyping pack
|-- devto_blog.md                 # Blog draft
|-- .github/                      # CI, issue templates, PR template
|-- .antigravity/                 # Local agent trace/evidence package
|-- pyproject.toml                # Project metadata and test/lint settings
`-- requirements.txt
```

Generated design exports such as `stitch_assets/` are intentionally ignored and not tracked.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create a local `.env` file from `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
GEMINI_MODEL=gemini-2.5-pro
```

Run the app:

```powershell
uvicorn main:app --reload --port 8000
```

Open:

```text
http://localhost:8000
```

## Optional ADK Run

Captain Cool also includes a Google Agent Development Kit project that exposes the weather and win-probability tools through an ADK `root_agent`.

```powershell
cd adk_agents
adk run captain_cool
```

The ADK scaffold follows Google's documented Python pattern: `from google.adk.agents.llm_agent import Agent`, a `root_agent` definition, and tool functions supplied in the `tools` list.

## API Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Lightweight readiness check for demos and deployment probes |
| `POST` | `/api/strategize` | Runs the full Gemini agent debate |
| `GET` | `/api/live` | Gets the current live/recent IPL match state |
| `GET` | `/api/matches` | Lists live/recent IPL matches |
| `GET` | `/api/match/{match_id}` | Gets scorecard details for one match |

Example manual strategy request:

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

## Verification

Run tests:

```powershell
python -m pytest src\tests
```

Current verified result:

```text
6 passed
```

Additional repository checks:

```powershell
python -m compileall main.py src adk_agents
python -c "import main; print(main.app.title)"
```

## Evaluation Mapping

| Rubric Area | Evidence |
| --- | --- |
| Relevance | Cricket-specific state, captain side, match phase, bowling resources, pitch/dew, target pressure |
| Technical depth | Gemini calls per agent, function tools, FastAPI endpoints, live cricket data integration |
| Agentic design | Strategist proposal, Devil's Advocate critique, final defend-or-revise loop, optional ADK scaffold |
| Documentation | Architecture doc, API reference, evaluation guide, demo script, AI Studio prompt pack, dev.to blog draft, `.antigravity` trace package |
| Maintainability | CI workflow, project metadata, PR template, issue templates, security policy, changelog, roadmap |

## Notes For Submission

- Add a real Google AI Studio share link to `devto_blog.md` before publishing.
- If you use Google Antigravity directly, replace the local `.antigravity/` notes with the official exported traces.
- Keep `.env` local. Do not commit API keys.
- Rotate any API key that was previously committed or shared.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
