"""Slice 41 — zero/perfect targets + quadrupples/N-times ratio.

Found 2026-09-16 by running objects:
  claimed_target("falls to zero") → None
  check_prediction(..., hurt, latest=1) → prediction-held  # invents held off-zero
  "goes to zero" / "perfect 5/5" → no-direction
  claimed_ratio("quadruples"|"five times"|"fivefold") → None while 4x grades
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_ratio,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_zero_word_is_target():
    assert claimed_target("falls to zero")["value"] == 0
    assert claimed_target("goes to zero")["value"] == 0
    assert claimed_target("goes to 0")["value"] == 0
    assert claimed_target("drops to 0")["value"] == 0


def test_falls_to_zero_does_not_invent_held_off_zero():
    held = check_prediction(
        "falls to zero", "hurt", -3, population=5, latest_value=0
    )
    missed = check_prediction(
        "falls to zero", "hurt", -2, population=5, latest_value=1
    )
    naive = naive_direction_check(
        "falls to zero", "hurt", -2, population=5, latest_value=1
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"  # direction invents held


def test_perfect_is_target():
    assert claimed_target("perfect 5/5") == {
        "value": 5,
        "population": 5,
        "raw": "perfect 5/5",
    }
    assert prediction_intent("perfect 5/5") == "flat"
    held = check_prediction(
        "perfect 5/5", "helped", 1, population=5, latest_value=5
    )
    missed = check_prediction(
        "perfect 5/5", "helped", 1, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_quadruples_and_n_times():
    assert claimed_ratio("quadruples")["factor"] == 4
    assert claimed_ratio("quadruples")["kind"] == "quadruple"
    assert claimed_ratio("five times")["factor"] == 5
    assert claimed_ratio("5 times")["factor"] == 5
    assert claimed_ratio("fivefold")["factor"] == 5
    assert claimed_ratio("4x")["factor"] == 4
    assert prediction_intent("pass rate quadruples") == "rise"
    assert prediction_intent("five times") == "rise"


def test_quadruples_grades_prior():
    held = check_prediction(
        "pass rate quadruples", "helped", 6, population=10, latest_value=8
    )
    missed = check_prediction(
        "pass rate quadruples", "helped", 1, population=10, latest_value=4
    )
    naive = naive_direction_check(
        "pass rate quadruples", "helped", 1, population=10, latest_value=4
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pred_demo_includes_slice41():
    names = {s.name for s in SCENARIOS}
    for required in (
        "falls_to_zero_holds",
        "falls_to_zero_missed",
        "perfect_holds",
        "perfect_missed",
        "quadruples_holds",
        "quadruples_missed",
        "five_times_holds",
        "five_times_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice41():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
    assert "zero" in proc.stdout.lower() or "quadruple" in proc.stdout.lower()
