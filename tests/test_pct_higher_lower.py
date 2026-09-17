"""Slice 44 — trailing comparator percents (`20% higher` / `more` / `up`).

Found by running objects:
  claimed_percent("20% higher") → None
  check_prediction("20% higher", "helped", 20, population=5) → prediction-held  # THE LIE
  # true 20% of pop 5 is Δ=+1; absolute +20 must miss

`higher by 20%` already parsed; the trailing form did not.
"""
from __future__ import annotations

from magnet.prediction import (
    check_prediction,
    claimed_percent,
    naive_direction_check,
    prediction_intent,
)


def test_pct_higher_parses_percent():
    assert claimed_percent("20% higher")["percent"] == 20
    assert claimed_percent("20 percent higher")["percent"] == 20
    assert claimed_percent("20% up")["percent"] == 20
    assert claimed_percent("20% more")["percent"] == 20


def test_pct_lower_parses_percent():
    assert claimed_percent("20% lower")["percent"] == 20
    assert claimed_percent("20 percent lower")["percent"] == 20
    assert claimed_percent("20% down")["percent"] == 20
    assert claimed_percent("20% less")["percent"] == 20
    assert claimed_percent("20 pct less")["percent"] == 20


def test_pct_more_less_get_intent():
    """more/less are not in rise/fall lexicon — bind from trailing comparator."""
    assert prediction_intent("20% more") == "rise"
    assert prediction_intent("20% less") == "fall"


def test_pct_higher_true_20pct_holds():
    """20% of pop 5 → expected Δ=+1."""
    c = check_prediction(
        "20% higher", "helped", 1, population=5, latest_value=4
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+percent"


def test_pct_higher_absolute_lie_misses():
    """THE LIE: unbound pct left direction-only → invented held on Δ=+20."""
    magnet = check_prediction(
        "20% higher", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "20% higher", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pct_lower_absolute_lie_misses():
    magnet = check_prediction(
        "20% lower", "hurt", -20, population=5, latest_value=0
    )
    naive = naive_direction_check(
        "20% lower", "hurt", -20, population=5, latest_value=0
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pct_more_absolute_lie_misses():
    magnet = check_prediction(
        "20% more", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "20% more", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pct_up_word_form():
    assert claimed_percent("20 percent up")["percent"] == 20
    magnet = check_prediction(
        "20 percent up", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
