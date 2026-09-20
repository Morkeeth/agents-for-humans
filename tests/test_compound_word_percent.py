"""Slice 59 — compound word-percents (twenty-five / seventy five).

Found by running objects after S58:
  claimed_percent("twenty-five percent") → None
  claimed_percent("twenty five percent") → None
  claimed_percent("twenty-five percent higher") → None; rise → invents held on Δ=+20
  Contrast: 25 percent / 25% grade; true 25% of pop 5 ≡ Δ+1.
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


def test_twenty_five_percent():
    assert claimed_percent("twenty-five percent")["percent"] == 25
    assert claimed_percent("twenty five percent")["percent"] == 25
    assert prediction_intent("twenty-five percent") == "rise"


def test_twenty_five_percent_higher_lie():
    assert claimed_percent("twenty-five percent higher")["percent"] == 25
    missed = check_prediction(
        "twenty-five percent higher", "helped", 20, population=5, latest_value=24
    )
    held = check_prediction(
        "twenty-five percent higher", "helped", 1, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "twenty-five percent higher", "helped", 20, population=5, latest_value=24
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"
    assert naive["outcome"] == "prediction-held"


def test_seventy_five_forms():
    assert claimed_percent("seventy-five percent")["percent"] == 75
    assert claimed_percent("seventy five percent")["percent"] == 75
    assert claimed_percent("ninety-nine percent")["percent"] == 99


def test_bare_tens_regression():
    assert claimed_percent("twenty percent")["percent"] == 20
    assert claimed_percent("25 percent")["percent"] == 25


def test_exactly_twenty_five_target():
    assert claimed_target("exactly twenty-five")["value"] == 25
    assert claimed_target("exactly twenty five")["value"] == 25


def test_pred_demo_includes_slice59():
    names = {s.name for s in SCENARIOS}
    assert "twenty_five_percent_missed" in names
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice59():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
