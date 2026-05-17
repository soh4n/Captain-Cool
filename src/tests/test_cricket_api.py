"""Basic tests for cricket API service."""

from src.services.cricket_api import calculate_win_probability, get_ipl_matches


def test_win_probability_basic():
    result = calculate_win_probability(target=180, current_score=100, wickets_lost=3, balls_bowled=60)
    assert "win_probability_percent" in result
    assert 1 <= result["win_probability_percent"] <= 99


def test_win_probability_target_reached():
    result = calculate_win_probability(target=150, current_score=155, wickets_lost=2, balls_bowled=90)
    assert result["win_probability"] == 100


def test_ipl_matches_returns_list():
    matches = get_ipl_matches()
    assert isinstance(matches, list)


if __name__ == "__main__":
    test_win_probability_basic()
    test_win_probability_target_reached()
    print("All tests passed.")
