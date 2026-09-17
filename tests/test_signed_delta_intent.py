"""Slice 46 — signed `+N` / `-N` intent honesty.

Found by running objects:
  claimed_magnitude("+1") → amount=1
  prediction_intent("+1") → unknown
  check_prediction("+1", "helped", 1) → no-direction  # THE LIE
  Contrast: prediction_intent("Δ+1") → rise (word char before +)

Also: `_CLAIM_SIGNED` backtracking stole `-2` from `-20%` — fixed with (?!\\d).
"""
from __future__ import annotations

from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    claimed_percent,
    naive_direction_check,
    prediction_intent,
)


def test_plus_one_is_rise_with_magnitude():
    assert prediction_intent("+1") == "rise"
    assert claimed_magnitude("+1")["amount"] == 1


def test_minus_one_is_fall_with_magnitude():
    assert prediction_intent("-1") == "fall"
    assert claimed_magnitude("-1")["amount"] == 1


def test_pass_rate_plus_one():
    assert prediction_intent("pass rate +1") == "rise"
    assert claimed_magnitude("pass rate +1")["amount"] == 1


def test_coverage_minus_one():
    assert prediction_intent("coverage -1") == "fall"


def test_signed_true_magnitude_holds():
    c = check_prediction("+1", "helped", 1, population=5, latest_value=4)
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+magnitude"


def test_signed_absolute_lie_misses():
    """THE LIE: amount on table but intent unknown → no-direction."""
    magnet = check_prediction("+1", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check(
        "+1", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_signed_percent_not_stolen_as_absolute():
    """`-20%` must not backtrack into signed amount=-2."""
    assert claimed_percent("-20%")["percent"] == 20
    assert claimed_magnitude("-20%")["amount"] is None
    assert prediction_intent("-20%") == "fall"
    magnet = check_prediction(
        "-20%", "hurt", -20, population=5, latest_value=0
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "direction+percent"


def test_plus_percent_still_percent():
    assert claimed_percent("+20%")["percent"] == 20
    assert claimed_magnitude("+20%")["amount"] is None
    assert prediction_intent("+20%") == "rise"
