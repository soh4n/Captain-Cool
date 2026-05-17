"""Tests for the Gemini debate orchestration endpoint."""

from src.api import strategize as strategize_module
from src.models.schemas import MatchState


class _FakeResponse:
    def __init__(self, text: str):
        self.text = text


class _FakeModels:
    def __init__(self):
        self.responses = [
            _FakeResponse("Gamma says dew is medium and win probability is 45%."),
            _FakeResponse("Alpha says bring Bumrah now."),
            _FakeResponse("Beta says saving Bumrah could be too passive."),
            _FakeResponse(
                '{"decision":"Bring Bumrah now","reasoning":"Break the set pair immediately.","dissent":"Beta wanted urgency, and Alpha agrees.","win_prob_context":"Waiting one over risks momentum."}'
            ),
        ]
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return self.responses.pop(0)


class _FakeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.models = _FakeModels()


def test_strategize_returns_visible_debate_trace(monkeypatch):
    fake_client = _FakeClient(api_key="test")
    monkeypatch.setattr(strategize_module, "GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(strategize_module.genai, "Client", lambda api_key: fake_client)

    result = strategize_module.strategize(
        MatchState(
            live=False,
            captain_side="bowling",
            innings=2,
            over=15,
            ball=2,
            current_score=142,
            wickets=4,
            team_batting="CSK",
            team_bowling="MI",
            striker="Shivam Dube",
            non_striker="MS Dhoni",
            bowlers_remaining={"Bumrah": 1, "Hardik": 2},
            pitch_conditions="two-paced with medium dew",
            venue="Mumbai",
            target=188,
            impact_player_available=True,
        )
    )

    assert result["captain_side"] == "bowling"
    assert result["analyst_report"].startswith("Gamma")
    assert result["strategist_initial"].startswith("Alpha")
    assert result["devils_advocate"].startswith("Beta")
    assert result["final_decision"]["decision"] == "Bring Bumrah now"
    assert len(fake_client.models.calls) == 4
    assert fake_client.models.calls[0]["config"].tools


def test_strategize_requires_gemini_key(monkeypatch):
    monkeypatch.setattr(strategize_module, "GEMINI_API_KEY", "")

    result = strategize_module.strategize(MatchState())

    assert result == {"error": "GEMINI_API_KEY environment variable is not set."}
