"""Slice 56 — signed word-percent + word arrows.

Found by running objects after S55:
  prediction_intent("-twenty percent") → rise  (digit -20% → fall)
  prediction_intent("minus twenty percent") → rise  (minus 20% → fall)
  claimed_target("three → four") → None  (digit 3→4 grades)
  claimed_target("three -> four") → None
  claimed_target("one → zero") → None

THE LIE: bare-percent default invents rise/held on helped when the claim
said fall; word arrows left no-direction while a destination sat on the table.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_minus_twenty_percent_is_fall():
    assert prediction_intent("-twenty percent") == "fall"
    assert prediction_intent("minus twenty percent") == "fall"
    # THE LIE: rise invents held on helped
    held = check_prediction(
        "-twenty percent", "hurt", -1, population=5, latest_value=3
    )
    missed_help = check_prediction(
        "-twenty percent", "helped", 1, population=5, latest_value=4
    )
    missed_abs = check_prediction(
        "minus twenty percent", "hurt", -20, population=5, latest_value=0
    )
    naive = naive_direction_check(
        "-twenty percent", "helped", 1, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"
    assert missed_help["outcome"] == "prediction-missed"
    assert missed_abs["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-missed"  # naive sees fall intent too


def test_plus_twenty_percent_is_rise():
    assert prediction_intent("+twenty percent") == "rise"
    assert prediction_intent("plus twenty percent") == "rise"
    held = check_prediction(
        "+twenty percent", "helped", 1, population=5, latest_value=4
    )
    missed = check_prediction(
        "plus twenty percent", "helped", 20, population=5, latest_value=24
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_digit_signed_percent_regression():
    assert prediction_intent("-20%") == "fall"
    assert prediction_intent("minus 20%") == "fall"
    assert prediction_intent("+20%") == "rise"


def test_word_arrow_destination():
    assert claimed_target("three → four")["value"] == 4
    assert claimed_target("three -> four")["value"] == 4
    assert claimed_target("one → zero")["value"] == 0
    assert claimed_target("from three → four")["value"] == 4
    held = check_prediction(
        "three → four", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "three → four", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "three → four", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_digit_arrow_regression():
    assert claimed_target("3→4")["value"] == 4


def test_pred_demo_includes_slice56():
    names = {s.name for s in SCENARIOS}
    assert "minus_twenty_percent_missed" in names
    assert "word_arrow_missed" in names
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice56():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
