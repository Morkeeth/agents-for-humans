"""Slice 43 — negated-rise + shall/ought/may + bare no-worse/better.

Found by running objects (not titles):
  prediction_intent("doesn't rise") → rise
  check_prediction("doesn't rise", "helped", 1) → prediction-held   # THE LIE
  prediction_intent("shall not fall") → fall
  check_prediction("shall not fall", "hurt", -1) → prediction-held  # THE LIE
  prediction_intent("no worse") → fall
  check_prediction("no worse", "hurt", -1) → prediction-held        # THE LIE

Magnet must grade these as flat. Direction inventing held on a negated move
is the failure mode Slice 35/40 left open for rise verbs and shall/ought/may.
"""
from __future__ import annotations

from magnet.prediction import (
    check_prediction,
    claimed_ceiling,
    claimed_floor,
    prediction_intent,
)


def test_doesnt_rise_is_flat_not_rise():
    assert prediction_intent("doesn't rise") == "flat"
    assert prediction_intent("does not rise") == "flat"


def test_never_rises_is_flat():
    assert prediction_intent("never rises") == "flat"
    assert prediction_intent("never improves") == "flat"
    assert prediction_intent("never increases") == "flat"


def test_wont_improve_cannot_improve_are_flat():
    assert prediction_intent("won't improve") == "flat"
    assert prediction_intent("cannot improve") == "flat"
    assert prediction_intent("won't increase") == "flat"
    assert prediction_intent("cannot increase") == "flat"
    assert prediction_intent("doesn't improve") == "flat"


def test_negated_rise_misses_on_helped_holds_on_unchanged():
    """THE LIE: never rises was rise → invented held when score rose."""
    for pred in (
        "doesn't rise",
        "never rises",
        "won't improve",
        "cannot improve",
        "never increases",
    ):
        helped = check_prediction(pred, "helped", 1, population=5, latest_value=4)
        unchanged = check_prediction(pred, "unchanged", 0, population=5, latest_value=4)
        assert helped["outcome"] == "prediction-missed", pred
        assert unchanged["outcome"] == "prediction-held", pred
        assert helped["intent"] == "flat", pred


def test_shall_ought_may_not_fall_are_flat():
    for pred in (
        "shall not fall",
        "ought not fall",
        "ought not to fall",
        "may not fall",
        "coverage shall not drop",
        "may not regress",
    ):
        assert prediction_intent(pred) == "flat", pred
        hurt = check_prediction(pred, "hurt", -1, population=5, latest_value=3)
        unchanged = check_prediction(pred, "unchanged", 0, population=5, latest_value=4)
        assert hurt["outcome"] == "prediction-missed", pred
        assert unchanged["outcome"] == "prediction-held", pred


def test_wont_get_worse_is_flat():
    for pred in ("won't get worse", "cannot get worse", "never gets worse"):
        assert prediction_intent(pred) == "flat", pred
        hurt = check_prediction(pred, "hurt", -1, population=5, latest_value=3)
        assert hurt["outcome"] == "prediction-missed", pred


def test_bare_no_worse_is_flat_not_fall():
    """THE LIE: no worse matched worse → fall → invented held on hurt."""
    assert prediction_intent("no worse") == "flat"
    hurt = check_prediction("no worse", "hurt", -1, population=5, latest_value=3)
    unchanged = check_prediction("no worse", "unchanged", 0, population=5, latest_value=4)
    assert hurt["outcome"] == "prediction-missed"
    assert unchanged["outcome"] == "prediction-held"


def test_bare_no_better_is_flat_not_rise():
    """THE LIE: no better matched better → rise → invented held on helped."""
    assert prediction_intent("no better") == "flat"
    helped = check_prediction("no better", "helped", 1, population=5, latest_value=4)
    unchanged = check_prediction("no better", "unchanged", 0, population=5, latest_value=4)
    assert helped["outcome"] == "prediction-missed"
    assert unchanged["outcome"] == "prediction-held"


def test_non_regression_is_flat():
    assert prediction_intent("non-regression") == "flat"
    assert prediction_intent("non regression") == "flat"
    hurt = check_prediction("non-regression", "hurt", -1, population=5, latest_value=3)
    assert hurt["outcome"] == "prediction-missed"


def test_no_worse_than_still_opens_floor():
    """Bound parser still owns the level; intent is flat (not fall)."""
    pred = "no worse than 4/5"
    assert prediction_intent(pred) == "flat"
    assert claimed_floor(pred)["value"] == 4
    assert claimed_floor(pred)["population"] == 5
    below = check_prediction(pred, "hurt", -1, population=5, latest_value=3)
    at = check_prediction(pred, "unchanged", 0, population=5, latest_value=4)
    assert below["outcome"] == "prediction-missed"
    assert at["outcome"] == "prediction-held"
    assert below["grade"] == "floor"


def test_no_better_than_still_opens_ceiling():
    pred = "no better than 3/5"
    assert prediction_intent(pred) == "flat"
    assert claimed_ceiling(pred)["value"] == 3
    above = check_prediction(pred, "helped", 1, population=5, latest_value=4)
    at = check_prediction(pred, "hurt", -1, population=5, latest_value=3)
    assert above["outcome"] == "prediction-missed"
    assert at["outcome"] == "prediction-held"
    assert above["grade"] == "ceiling"
