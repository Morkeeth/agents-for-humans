"""Slice 45 — bare `up N` / `down N` magnitude honesty.

Found by running objects:
  claimed_magnitude("up 1") → amount=None
  check_prediction("up 1", "helped", 20) → prediction-held  # THE LIE
  # claim said +1; absolute +20 must miss
  Contrast: claimed_magnitude("up by 1") → amount=1 (already graded)
"""
from __future__ import annotations

from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    claimed_percent,
    naive_direction_check,
    prediction_intent,
)


def test_up_n_parses_amount():
    assert claimed_magnitude("up 1")["amount"] == 1
    assert claimed_magnitude("up 2")["amount"] == 2
    assert prediction_intent("up 1") == "rise"


def test_down_n_parses_amount():
    assert claimed_magnitude("down 1")["amount"] == 1
    assert prediction_intent("down 1") == "fall"


def test_up_n_true_magnitude_holds():
    c = check_prediction("up 1", "helped", 1, population=5, latest_value=4)
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+magnitude"


def test_up_n_absolute_lie_misses():
    """THE LIE: unbound amount left direction-only → invented held on Δ=+20."""
    magnet = check_prediction("up 1", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check(
        "up 1", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_down_n_absolute_lie_misses():
    magnet = check_prediction("down 1", "hurt", -20, population=5, latest_value=0)
    naive = naive_direction_check(
        "down 1", "hurt", -20, population=5, latest_value=0
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_up_percent_still_percent_not_amount():
    """`up 20%` must stay percent-of-pop — never amount=20."""
    assert claimed_percent("up 20%")["percent"] == 20
    assert claimed_magnitude("up 20%")["amount"] is None
    magnet = check_prediction(
        "up 20%", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
