# Roadmap

Captain Cool is designed as a practical match-decision companion rather than a generic cricket chatbot. The next improvements are grouped by judging impact and product maturity.

## Near Term

- Add a deterministic demo mode that works without Gemini or RapidAPI keys.
- Persist generated strategy calls to a lightweight local store for the History view.
- Add screenshots or short GIFs of the War Room, Insights, and History flows.
- Add stricter request validation for captain side, over/ball ranges, and wicket counts.

## Mid Term

- Add structured response schemas for each agent step.
- Add richer bowling-resource modeling: overs left, matchup history, death-over skill, and left-right pairing.
- Add confidence bands and counterfactual summaries to the final decision.
- Add deployment notes for Render, Railway, Fly.io, and Cloud Run.

## Stretch

- Support multiple competitions beyond IPL.
- Add a replay mode for historical matches.
- Add a frontend comparison view for Strategist Alpha vs Devil's Advocate Beta.
- Add telemetry hooks for prompt quality and tool-call latency.
