"""Slice 47 — crash/collapse/soar targets + from→to transitions.

Found by running objects:
  claimed_target("crashes to zero") → None
  claimed_target("from 3/5 to 4/5") → None
  # unbound → no-direction while a named end-state sat on the table
  Contrast: claimed_target("falls to zero") → 0 (Slice 41)
"""
from __future__ import annotations

from magnet.prediction import (
    check_prediction,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)


def test_crashes_to_zero_is_target():
    t = claimed_target("crashes to zero")
    assert t["value"] == 0
    assert prediction_intent("crashes to zero") == "fall"


def test_collapses_to_zero_is_target():
    assert claimed_target("collapses to 0")["value"] == 0


def test_soars_to_perfect_is_target():
    t = claimed_target("soars to 5/5")
    assert t["value"] == 5
    assert t["population"] == 5
    assert prediction_intent("soars to 5/5") == "rise"


def test_dives_and_plunges_and_spikes():
    assert claimed_target("dives to 1/5")["value"] == 1
    assert claimed_target("plunges to 0")["value"] == 0
    assert claimed_target("spikes to 5")["value"] == 5


def test_crashes_wrong_latest_misses_naive_holds():
    """THE LIE: unbound crash left no-direction; direction invents held off-zero."""
    magnet = check_prediction(
        "crashes to zero", "hurt", -1, population=5, latest_value=1
    )
    naive = naive_direction_check(
        "crashes to zero", "hurt", -1, population=5, latest_value=1
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "direction+target"
    assert naive["outcome"] == "prediction-held"


def test_crashes_at_zero_holds():
    c = check_prediction(
        "crashes to zero", "hurt", -3, population=5, latest_value=0
    )
    assert c["outcome"] == "prediction-held"


def test_from_to_destination_is_target():
    t = claimed_target("from 3/5 to 4/5")
    assert t["value"] == 4
    assert t["population"] == 5


def test_arrow_transition_is_target():
    t = claimed_target("3/5 → 4/5")
    assert t["value"] == 4
    assert t["population"] == 5


def test_from_to_zero():
    assert claimed_target("from 5 to zero")["value"] == 0


def test_from_to_wrong_latest_misses():
    magnet = check_prediction(
        "from 3/5 to 4/5", "helped", 1, population=5, latest_value=5
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "target"


def test_falls_to_zero_regression():
    """Slice 41 must still hold."""
    assert claimed_target("falls to zero")["value"] == 0
    missed = check_prediction(
        "falls to zero", "hurt", -2, population=5, latest_value=1
    )
    assert missed["outcome"] == "prediction-missed"
