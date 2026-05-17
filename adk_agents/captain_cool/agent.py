"""Google ADK agent definition for Captain Cool.

Run from the repository root after installing `google-adk`:

    cd adk_agents
    adk run captain_cool
"""

from google.adk.agents.llm_agent import Agent

from src.services.cricket_api import calculate_win_probability, get_venue_weather


ROOT_INSTRUCTION = """You are Captain Cool, an IPL match strategy coordinator.

Use the get_venue_weather and calculate_win_probability tools when the user gives
venue, score, target, wickets, or balls/overs information. Respond as a concise
captaincy advisor: explain the match context, propose a tactical move, challenge
your own plan with one risk, then give a final call in plain cricket language.

Do not use machine-learning jargon. Speak to a captain and coaching staff."""


root_agent = Agent(
    model="gemini-2.5-pro",
    name="captain_cool_adk_agent",
    description="IPL captaincy strategy agent with weather and win-probability tools.",
    instruction=ROOT_INSTRUCTION,
    tools=[get_venue_weather, calculate_win_probability],
)
