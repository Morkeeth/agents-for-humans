"""Slice 54 — word from→to levels.

Found by running objects after S53:
  claimed_target("from three to four") → None
  claimed_target("goes from three to five") → None
  claimed_target("from one to zero") → None
  Contrast: from 3 to 4 @4 held / @3 missed (naive held).
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


def test_word_from_to_destination():
    tgt = claimed_target("from three to four")
    assert tgt["value"] == 4
    assert prediction_intent("from three to four") == "flat"
    held = check_prediction(
        "from three to four", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "from three to four", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "from three to four", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_goes_from_word_to_word():
    assert claimed_target("goes from three to five")["value"] == 5
    missed = check_prediction(
        "goes from three to five", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"


def test_from_one_to_zero():
    assert claimed_target("from one to zero")["value"] == 0
    held = check_prediction(
        "from one to zero", "hurt", -1, population=5, latest_value=0
    )
    missed = check_prediction(
        "from one to zero", "hurt", -1, population=5, latest_value=1
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_digit_from_to_regression():
    assert claimed_target("from 3 to 4")["value"] == 4


def test_pred_demo_includes_slice54():
    names = {s.name for s in SCENARIOS}
    assert "word_from_to_missed" in names
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice54():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
