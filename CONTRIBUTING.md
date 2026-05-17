# Contributing to Captain Cool

Thank you for your interest in contributing to **Captain Cool**!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/captain-cool.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your API keys
6. Run the app: `uvicorn main:app --reload`

## Code Style

- Python: Follow PEP 8
- Frontend: Standard HTML/CSS/JS with Tailwind
- Keep modules small and focused
- Prefer clear cricket language in prompts and user-facing copy.
- Keep secrets in `.env`; never commit real Gemini or RapidAPI keys.

## Verification

Before opening a pull request, run:

```powershell
python -m pytest
python -m compileall main.py src adk_agents
```

If you change runtime behavior, also smoke-test:

```powershell
uvicorn main:app --reload --port 8000
```

## Pull Request Process

1. Ensure your code runs without errors
2. Update the README if you add new features
3. Update docs under `docs/` when you change API shape, demo flow, or architecture
4. Submit your PR with a clear description and verification notes

## Issues

Use GitHub Issues to report bugs or request features.
