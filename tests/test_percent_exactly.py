"""Slice 36 — percent-of-pop + exactly-level prediction honesty.

Found 2026-09-15 by running the prediction object:
  claimed_magnitude("improves by 20%") → amount=20  # stripped %
  check_prediction(..., delta=1, pop=5) → prediction-missed   # true 20%
  check_prediction(..., delta=20, pop=5) → prediction-held    # THE LIE

Also: exactly 4/5 → no-direction while a level sat on the table.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    claimed_percent,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_percent_not_parsed_as_absolute_amount():
    """THE LIE: % stripped → amount=20 absolute."""
    mag = claimed_magnitude("coverage improves by 20%")
    assert mag["amount"] is None
    pct = claimed_percent("coverage improves by 20%")
    assert pct["percent"] == 20
    assert pct["raw"] is not None


def test_percent_of_pop_holds_on_true_fraction():
    """20% of pop 5 = Δ+1 — old magnet missed this."""
    c = check_prediction(
        "coverage improves by 20%",
        "helped",
        1,
        population=5,
        latest_value=4,
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+percent"
    assert c["expected_delta"] == 1


def test_percent_absolute_lie_misses():
    """Δ=+20 on pop 5 is not 20% — old magnet invented held."""
    pred = "coverage improves by 20%"
    magnet = check_prediction(
        pred, "helped", 20, population=5, latest_value=5
    )
    naive = naive_direction_check(
        pred, "helped", 20, population=5, latest_value=5
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["expected_delta"] == 1  # 20% of 5
    assert naive["outcome"] == "prediction-held"  # direction invents held


def test_exactly_parses_as_target():
    assert claimed_target("exactly 4/5")["value"] == 4
    assert claimed_target("exactly 4/5")["population"] == 5
    assert claimed_target("must be exactly 4/5")["value"] == 4
    assert claimed_target("lands at exactly 4/5")["value"] == 4
    assert prediction_intent("exactly 4/5") == "flat"


def test_exactly_grades_latest():
    held = check_prediction(
        "must be exactly 4/5", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "exactly 4/5", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "exactly 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pred_demo_includes_percent_and_exactly():
    names = {s.name for s in SCENARIOS}
    for required in (
        "percent_of_pop_holds",
        "percent_absolute_lie",
        "exactly_holds",
        "exactly_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    assert "Percent" in out or "percent" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice36():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
    assert "20%" in proc.stdout or "percent" in proc.stdout.lower()
