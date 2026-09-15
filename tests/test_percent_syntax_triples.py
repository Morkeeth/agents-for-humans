"""Slice 39 — percent syntax without `by` + triples/Nx ratio.

Found 2026-09-15:
  claimed_percent("rises 20%") → None  # direction invented held on any rise
  triples / 3x / 2x → unknown
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_percent,
    claimed_ratio,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_rises_pct_without_by_parses():
    assert claimed_percent("rises 20%")["percent"] == 20
    assert claimed_percent("improves 20%")["percent"] == 20
    assert claimed_percent("20% improvement")["percent"] == 20
    assert claimed_percent("up 50%")["percent"] == 50
    assert claimed_percent("+20%")["percent"] == 20
    assert prediction_intent("+20%") == "rise"


def test_rises_pct_without_by_grades_pop():
    held = check_prediction(
        "rises 20%", "helped", 1, population=5, latest_value=4
    )
    missed = check_prediction(
        "rises 20%", "helped", 20, population=5, latest_value=5
    )
    naive = naive_direction_check(
        "rises 20%", "helped", 20, population=5, latest_value=5
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_triples_and_nx_ratio():
    assert claimed_ratio("triples")["kind"] == "triple"
    assert claimed_ratio("triples")["factor"] == 3
    assert claimed_ratio("3x")["factor"] == 3
    assert claimed_ratio("2x")["kind"] == "double"
    assert prediction_intent("pass rate triples") == "rise"
    assert prediction_intent("3x") == "rise"


def test_triples_grades_prior():
    # prior=2, latest=6, Δ=+4
    held = check_prediction(
        "pass rate triples", "helped", 4, population=10, latest_value=6
    )
    missed = check_prediction(
        "pass rate triples", "helped", 1, population=10, latest_value=4
    )
    naive = naive_direction_check(
        "pass rate triples", "helped", 1, population=10, latest_value=4
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pred_demo_includes_slice39():
    names = {s.name for s in SCENARIOS}
    for required in (
        "rises_pct_no_by_holds",
        "rises_pct_no_by_missed",
        "triples_holds",
        "triples_missed",
        "three_x_holds",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice39():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "20%" in proc.stdout or "triple" in proc.stdout.lower()
