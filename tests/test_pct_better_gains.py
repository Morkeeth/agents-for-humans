"""Slice 42 — percent-better/worse + gains/jumps/boosts.

Found 2026-09-16 by running objects:
  claimed_percent("50% better") → None; intent=unknown → no-direction
  "gains 20%" / "jumps 20%" → unbound
  "boosts by 20%" → pct=20 but intent=unknown → no-direction on true 20%
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_percent,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_pct_better_worse_parse():
    assert claimed_percent("50% better")["percent"] == 50
    assert claimed_percent("50% worse")["percent"] == 50
    assert claimed_percent("20 percent better")["percent"] == 20
    assert claimed_percent("gets 20% better")["percent"] == 20
    assert prediction_intent("50% better") == "rise"
    assert prediction_intent("50% worse") == "fall"


def test_pct_better_grades_pop_not_absolute():
    # 50% of pop 5 → Δ=+2
    held = check_prediction(
        "50% better", "helped", 2, population=5, latest_value=4
    )
    missed = check_prediction(
        "50% better", "helped", 20, population=5, latest_value=5
    )
    naive = naive_direction_check(
        "50% better", "helped", 20, population=5, latest_value=5
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_gains_jumps_boosts_rise_and_percent():
    for text in ("gains 20%", "jumps 20%", "boosts by 20%", "boosts 20%", "gains by 20%"):
        assert prediction_intent(text) == "rise", text
        assert claimed_percent(text)["percent"] == 20, text
    held = check_prediction("gains 20%", "helped", 1, population=5, latest_value=4)
    missed = check_prediction("gains 20%", "helped", 20, population=5, latest_value=5)
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_pred_demo_includes_slice42():
    names = {s.name for s in SCENARIOS}
    for required in (
        "pct_better_holds",
        "pct_better_missed",
        "pct_worse_holds",
        "gains_pct_holds",
        "gains_pct_missed",
        "boosts_by_pct_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice42():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
    assert "better" in proc.stdout.lower() or "gains" in proc.stdout.lower()
