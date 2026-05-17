# Quality Checklist

Use this before submitting or publishing the repository.

## Repository

- [ ] README has current setup, architecture, endpoints, and verification output.
- [ ] `.env.example` contains placeholders only.
- [ ] No real API keys are committed.
- [ ] Screenshots or demo media are current, if included.
- [ ] `CHANGELOG.md` reflects meaningful changes.
- [ ] `ROADMAP.md` is honest about unfinished work.

## Runtime

- [ ] `python -m pytest`
- [ ] `python -m compileall main.py src adk_agents`
- [ ] `uvicorn main:app --reload --port 8000`
- [ ] `GET /api/health` returns `status: ok`.

## Demo

- [ ] Manual strategy mode works with a known scenario.
- [ ] Live mode behavior is explained if no IPL match or RapidAPI key is available.
- [ ] The final decision includes decision, reasoning, dissent, and win-probability context.
- [ ] The demo mentions the optional ADK scaffold.
