# Demo Script

Use this walkthrough when recording a submission video, presenting to a reviewer, or checking the repository quickly.

## 1. Start Locally

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open:

```text
http://localhost:8000
```

## 2. Show The Reviewer The Flow

1. Open the War Room screen.
2. Point out the captain-side toggle and manual match state fields.
3. Use a pressure chase scenario: CSK 142/4 after 15.2 overs, chasing 188 in Mumbai.
4. Submit the state and show the debate trace:
   - Stats Analyst Gamma
   - Strategist Alpha
   - Devil's Advocate Beta
   - Strategist Alpha Final
5. Move to Insights and History to show that the frontend is a multi-screen product, not only an API demo.

## 3. API Smoke Checks

```powershell
Invoke-WebRequest http://localhost:8000/api/health -UseBasicParsing
python -m pytest
```

## 4. What To Emphasize

- This is a captaincy strategist, not a general chat interface.
- The final answer is produced only after a challenge step.
- The analyst agent uses real tools for weather/dew and win-probability context.
- The repository includes an optional Google ADK-compatible scaffold for agent portability.

## 5. Known Demo Requirements

- `GEMINI_API_KEY` is required for `/api/strategize`.
- `RAPIDAPI_KEY` is required for live/recent IPL match endpoints.
- Manual mode is the most reliable demo path when external services are unavailable.
