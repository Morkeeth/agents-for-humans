"""Slice 57 — decimal truncation refuse · up to ceiling · down to target.

Found by running objects after S56:
  claimed_percent("2.5%") → 5   # THE LIE: fractional digit stolen
  claimed_percent("50.5%") → 5
  claimed_magnitude("rises by 1.5") → amount=1
  claimed_magnitude("by 1.5") → amount=1
  "up to 4" → intent=rise, ceiling=None → invents held on helped
  "down to 2" → intent=fall, target=None → invents held off destination
  Contrast: 20% / rises by 1 / at most 4 / falls to 2 already grade.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_ceiling,
    claimed_magnitude,
    claimed_percent,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_decimal_percent_refused():
    for text in ("2.5%", "50.5%", "0.5%", "improves 2.5%", "rises by 2.5%"):
        assert claimed_percent(text)["percent"] is None, text


def test_integer_percent_regression():
    assert claimed_percent("20%")["percent"] == 20
    assert claimed_percent("improves by 20%")["percent"] == 20
    missed = check_prediction("20%", "helped", 20, population=5, latest_value=24)
    assert missed["outcome"] == "prediction-missed"


def test_decimal_magnitude_refused():
    for text in ("rises by 1.5", "by 1.5", "up 0.5", "+1.5"):
        assert claimed_magnitude(text)["amount"] is None, text


def test_integer_magnitude_regression():
    assert claimed_magnitude("rises by 1")["amount"] == 1
    assert claimed_magnitude("up 1")["amount"] == 1
    assert claimed_magnitude("+1")["amount"] == 1
    missed = check_prediction(
        "rises by 1", "helped", 20, population=5, latest_value=24
    )
    assert missed["outcome"] == "prediction-missed"


def test_up_to_ceiling():
    assert prediction_intent("up to 4") == "flat"
    assert claimed_ceiling("up to 4")["value"] == 4
    assert claimed_ceiling("up to 4/5")["value"] == 4
    held = check_prediction("up to 4", "unchanged", 0, population=5, latest_value=4)
    missed = check_prediction(
        "up to 4", "unchanged", 0, population=5, latest_value=5
    )
    naive = naive_direction_check(
        "up to 4", "unchanged", 0, population=5, latest_value=5
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_down_to_target():
    assert claimed_target("down to 2")["value"] == 2
    assert claimed_target("down to 2/5")["value"] == 2
    held = check_prediction("down to 2", "hurt", -2, population=5, latest_value=2)
    missed = check_prediction(
        "down to 2", "hurt", -1, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "down to 2", "hurt", -1, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pred_demo_includes_slice57():
    names = {s.name for s in SCENARIOS}
    for required in ("up_to_missed", "down_to_missed", "decimal_pct_refused"):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice57():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
