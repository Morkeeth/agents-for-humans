"""Slice 56 — bare digit `3 to 4` / `3/5 to 4/5` · mixed word/digit.

Found by running objects after S55:
  claimed_target("3 to 4") → None
  claimed_target("3/5 to 4/5") → None
  claimed_target("goes 3 to 4") → None
  claimed_target("three to 4") → None
  claimed_target("3 to four") → None
  claimed_target("zero to 4") → None
  Contrast: from 3 to 4 @4 held / @3 missed (naive held);
            three to four (S55) already grades.
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


def test_bare_digit_to_destination():
    tgt = claimed_target("3 to 4")
    assert tgt["value"] == 4
    assert prediction_intent("3 to 4") == "flat"
    held = check_prediction("3 to 4", "unchanged", 0, population=5, latest_value=4)
    missed = check_prediction("3 to 4", "unchanged", 0, population=5, latest_value=3)
    naive = naive_direction_check(
        "3 to 4", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_bare_slash_to_slash():
    tgt = claimed_target("3/5 to 4/5")
    assert tgt["value"] == 4
    assert tgt["population"] == 5
    held = check_prediction(
        "3/5 to 4/5", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "3/5 to 4/5", "unchanged", 0, population=5, latest_value=5
    )
    naive = naive_direction_check(
        "3/5 to 4/5", "unchanged", 0, population=5, latest_value=5
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_goes_digit_to_digit():
    assert claimed_target("goes 3 to 4")["value"] == 4
    assert claimed_target("moves 2 to 0")["value"] == 0


def test_mixed_word_digit_to():
    assert claimed_target("three to 4")["value"] == 4
    assert claimed_target("3 to four")["value"] == 4
    assert claimed_target("zero to 4")["value"] == 4
    missed = check_prediction(
        "3 to four", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "3 to four", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_from_digit_regression():
    assert claimed_target("from 3 to 4")["value"] == 4
    assert claimed_target("3→4")["value"] == 4


def test_pred_demo_includes_slice56():
    names = {s.name for s in SCENARIOS}
    for required in ("bare_digit_to_missed", "bare_slash_to_missed", "mixed_to_missed"):
        assert required in names, required
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
