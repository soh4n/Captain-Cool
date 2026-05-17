# Security Policy

## Supported Version

This repository is a hackathon/demo project. Security fixes are accepted against the `main` branch.

## Reporting a Vulnerability

Please open a private report or contact the maintainer before creating a public issue for:

- Exposed API keys or credentials
- Prompt injection paths that can leak secrets
- Server-side request or file-access vulnerabilities
- Dependency issues with a known CVE

Do not include working secrets, tokens, or private RapidAPI/Gemini account details in public issues.

## Secret Handling

- Runtime secrets live in `.env`, which is ignored by Git.
- `.env.example` documents required keys without real values.
- If a key was committed, shared in a screenshot, or used in a public demo, rotate it immediately.
