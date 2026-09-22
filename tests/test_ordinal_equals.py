"""Slice 58 — ordinals `3rd to 4th` / `third to fourth` · `equals 4/5`.

Found by running objects after S57:
  claimed_target("3rd to 4th") → None
  claimed_target("from 3rd to 4th") → None
  claimed_target("third to fourth") → None
  claimed_target("from third to fourth") → None
  claimed_target("equals 4/5") → None
  claimed_target("equal to 4/5") → None
  claimed_target("== 4/5") → None
  claimed_target("equals four") → None
  THE LIE: claimed_target("3rd/5 to 4th/5") → raw='5 to 4' (digit steal)
  Contrast: 3 to 4 / from three to four / exactly 4/5 already grade.
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


def test_ordinal_digit_to_destination():
    tgt = claimed_target("3rd to 4th")
    assert tgt["value"] == 4
    assert tgt["raw"] == "3rd to 4th"
    assert prediction_intent("3rd to 4th") == "flat"
    held = check_prediction(
        "3rd to 4th", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "3rd to 4th", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "3rd to 4th", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_from_ordinal_digit_and_goes():
    assert claimed_target("from 3rd to 4th")["value"] == 4
    assert claimed_target("goes 3rd to 4th")["value"] == 4
    assert claimed_target("goes from 3rd to 4th")["value"] == 4
    assert claimed_target("1st to 2nd")["value"] == 2
    assert claimed_target("3rd → 4th")["value"] == 4


def test_ordinal_slash_not_digit_steal():
    """THE LIE: pre-S58 invented raw='5 to 4' from 3rd/5 to 4th/5."""
    tgt = claimed_target("3rd/5 to 4th/5")
    assert tgt["value"] == 4
    assert tgt["population"] == 5
    assert tgt["raw"] == "3rd/5 to 4th/5"
    missed = check_prediction(
        "3rd/5 to 4th/5", "unchanged", 0, population=5, latest_value=5
    )
    naive = naive_direction_check(
        "3rd/5 to 4th/5", "unchanged", 0, population=5, latest_value=5
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_ordinal_word_to_destination():
    tgt = claimed_target("third to fourth")
    assert tgt["value"] == 4
    assert prediction_intent("third to fourth") == "flat"
    assert claimed_target("from third to fourth")["value"] == 4
    assert claimed_target("first to second")["value"] == 2
    assert claimed_target("third/five to fourth/five") == {
        "value": 4,
        "population": 5,
        "raw": "third/five to fourth/five",
        "perfect": False,
    }
    missed = check_prediction(
        "third to fourth", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "third to fourth", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_equals_digit_target():
    for text in (
        "equals 4/5",
        "equal to 4/5",
        "is equal to 4/5",
        "must equal 4/5",
        "should equal 4/5",
        "== 4/5",
        "pass rate equals 4/5",
    ):
        tgt = claimed_target(text)
        assert tgt["value"] == 4, text
        assert tgt["population"] == 5, text
        assert prediction_intent(text) == "flat", text
    held = check_prediction(
        "equals 4/5", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "equals 4/5", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "equals 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_equals_word_destination():
    assert claimed_target("equals four")["value"] == 4
    assert claimed_target("equal to fourth")["value"] == 4
    missed = check_prediction(
        "equals four", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"


def test_cardinal_regression():
    assert claimed_target("3 to 4")["value"] == 4
    assert claimed_target("from three to four")["value"] == 4
    assert claimed_target("exactly 4/5")["value"] == 4
    assert claimed_target("3/5 to 4/5")["population"] == 5


def test_pred_demo_includes_slice58():
    names = {s.name for s in SCENARIOS}
    for required in (
        "ordinal_digit_to_missed",
        "ordinal_word_to_missed",
        "ordinal_slash_to_missed",
        "equals_slash_missed",
        "eq_eq_missed",
        "equals_word_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice58():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
