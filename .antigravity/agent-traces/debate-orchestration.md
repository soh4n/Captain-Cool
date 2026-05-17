# Runtime Agent Debate Trace

Captain Cool's runtime behavior is agentic because the decision is not produced by a
single prompt. Each role receives its own system prompt, temperature, and Gemini API call.

## Multi-Agent Debate Architecture

```
         ┌──────────────────────────────────────┐
         │        User / Frontend                │
         │  POST /api/strategize                 │
         │  {live: true, captain_side: "batting"}│
         └──────────────┬───────────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────────┐
         │   Live Data Fetch (if live=true)      │
         │   get_live_match_state()              │
         │   → Cricbuzz API: /matches/v1/live    │
         │   → IPL filter → scorecard parse      │
         └──────────────┬───────────────────────┘
                        │ match_state
                        ▼
┌───────────────────────────────────────────────────┐
│  Agent 1: Stats Analyst Gamma                     │
│  Temperature: 0.2  |  Model: gemini-2.5-pro       │
│                                                   │
│  System Prompt: "You are Stats Analyst Gamma..."   │
│  Tools: get_venue_weather, calculate_win_probability│
│                                                   │
│  INPUT:  Raw match state JSON                     │
│  OUTPUT: Structured statistical brief             │
│          (weather, dew, win prob, phase analysis)  │
└───────────────────────┬───────────────────────────┘
                        │ analyst_report
                        ▼
┌───────────────────────────────────────────────────┐
│  Agent 2: Strategist Alpha (Initial Proposal)     │
│  Temperature: 0.7  |  Model: gemini-2.5-pro       │
│                                                   │
│  System Prompt: Side-aware (batting/bowling)      │
│  No tools (reasoning only)                        │
│                                                   │
│  INPUT:  match_state + analyst_report             │
│  OUTPUT: One tactical decision with reasoning     │
│          in cricket commentary language            │
└───────────────────────┬───────────────────────────┘
                        │ strategist_initial
                        ▼
┌───────────────────────────────────────────────────┐
│  Agent 3: Devil's Advocate Beta                   │
│  Temperature: 0.8  |  Model: gemini-2.5-pro       │
│                                                   │
│  System Prompt: "Challenge the call — hard..."     │
│  No tools (adversarial reasoning)                 │
│                                                   │
│  INPUT:  match_state + analyst + strategist plan   │
│  OUTPUT: Strongest objection + alternative call    │
└───────────────────────┬───────────────────────────┘
                        │ devils_advocate
                        ▼
┌───────────────────────────────────────────────────┐
│  Agent 2: Strategist Alpha (Final Decision)       │
│  Temperature: 0.7  |  Model: gemini-2.5-pro       │
│                                                   │
│  System Prompt: "Defend or Revise..."              │
│  No tools (produces final structured JSON)        │
│                                                   │
│  INPUT:  initial_plan + DA objection               │
│  OUTPUT: JSON {decision, reasoning, dissent,      │
│          win_prob_context}                         │
└───────────────────────┬───────────────────────────┘
                        │ final_decision
                        ▼
         ┌──────────────────────────────────────┐
         │  API Response to Frontend             │
         │  {                                   │
         │    analyst_report: "...",             │
         │    strategist_initial: "...",         │
         │    devils_advocate: "...",            │
         │    final_decision: {...},             │
         │    live_score: {...}                  │
         │  }                                   │
         └──────────────────────────────────────┘
```

## Visible Debate in Frontend

The frontend displays the full debate trace in sequential panels so
reviewers can inspect the multi-agent collaboration:

1. **📊 Analyst Report** — Statistical brief from Gamma
2. **⚔️ Strategist's Initial Call** — Alpha's first proposal
3. **🔥 Devil's Advocate Challenge** — Beta's objection
4. **🏆 Final Decision** — Alpha's defense/revision as structured JSON

## Key Design Decisions

- **Separate API calls, not a single multi-turn chat**: Each agent gets its
  own `client.models.generate_content()` call with distinct system instructions
  and temperature settings.

- **Temperature gradient**: Analyst (0.2) → Strategist (0.7) → DA (0.8) to
  ensure data precision, balanced tactics, and creative dissent respectively.

- **Real tool use**: Gamma's function tools (`get_venue_weather`,
  `calculate_win_probability`) are registered as Gemini function declarations,
  not hardcoded. The agent decides when to call them.

- **Captain-side awareness**: All prompts adapt based on whether the user
  selected "batting" or "bowling" captain, fundamentally changing the
  decision space.

- **Genuine revision**: The final turn can produce OPTION A (defend) or
  OPTION B (revise), meaning the DA can actually change the outcome.
