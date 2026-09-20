"""Slice 58 — fifteen percent + must-be targets.

Found by running objects after S57:
  claimed_percent("fifteen percent") → None (15% grades)
  claimed_percent("fifteen percent higher") → None; rise → invents held on Δ=+20
  claimed_target("must be four") → None; claimed_target("must be 4") → None
  Contrast: must be exactly 4 / exactly four grade.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_percent,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_fifteen_percent():
    assert claimed_percent("fifteen percent")["percent"] == 15
    assert prediction_intent("fifteen percent") == "rise"
    missed = check_prediction(
        "fifteen percent", "helped", 20, population=5, latest_value=24
    )
    held = check_prediction(
        "fifteen percent", "helped", 1, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "fifteen percent", "helped", 20, population=5, latest_value=24
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"
    assert naive["outcome"] == "prediction-held"


def test_fifteen_percent_higher_lie():
    assert claimed_percent("fifteen percent higher")["percent"] == 15
    missed = check_prediction(
        "fifteen percent higher", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "fifteen percent higher", "helped", 20, population=5, latest_value=24
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_teen_percents():
    assert claimed_percent("thirteen percent")["percent"] == 13
    assert claimed_percent("nineteen percent")["percent"] == 19


def test_must_be_four():
    assert claimed_target("must be four")["value"] == 4
    assert claimed_target("must be 4")["value"] == 4
    assert prediction_intent("must be four") == "flat"
    missed = check_prediction(
        "must be four", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "must be four", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_should_ought_be_four():
    assert claimed_target("should be four")["value"] == 4
    assert claimed_target("ought to be four")["value"] == 4


def test_must_be_exactly_regression():
    assert claimed_target("must be exactly 4")["value"] == 4
    assert claimed_target("must be exactly four")["value"] == 4


def test_pred_demo_includes_slice58():
    names = {s.name for s in SCENARIOS}
    assert "fifteen_percent_missed" in names
    assert "must_be_four_missed" in names
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
