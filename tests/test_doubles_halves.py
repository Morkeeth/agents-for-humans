"""Slice 37 — doubles/halves vs prior honesty.

Found 2026-09-15: prediction_intent("pass rate doubles") → unknown.
Direction-only would invent held on any rise. Prior = latest − Δ is the object.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_ratio,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_doubles_intent_and_ratio():
    assert prediction_intent("pass rate doubles") == "rise"
    assert claimed_ratio("pass rate doubles")["kind"] == "double"
    assert claimed_ratio("twice as many")["kind"] == "double"


def test_halves_intent_and_ratio():
    assert prediction_intent("pass rate halves") == "fall"
    assert claimed_ratio("halves")["kind"] == "half"
    assert claimed_ratio("cuts in half")["kind"] == "half"


def test_doubles_holds_when_delta_equals_prior():
    # prior=2, latest=4, Δ=+2
    c = check_prediction(
        "pass rate doubles", "helped", 2, population=5, latest_value=4
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+ratio"
    assert c["prior"] == 2


def test_doubles_misses_non_double_rise():
    """THE LIE: direction invents held when claim said doubles but Δ ≠ prior."""
    pred = "pass rate doubles"
    magnet = check_prediction(
        pred, "helped", 1, population=5, latest_value=4
    )
    naive = naive_direction_check(
        pred, "helped", 1, population=5, latest_value=4
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["prior"] == 3
    assert naive["outcome"] == "prediction-held"


def test_halves_holds_and_misses():
    held = check_prediction(
        "pass rate halves", "hurt", -2, population=5, latest_value=2
    )
    missed = check_prediction(
        "pass rate halves", "hurt", -1, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "pass rate halves", "hurt", -1, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_pred_demo_includes_ratio_scenarios():
    names = {s.name for s in SCENARIOS}
    for required in ("doubles_holds", "doubles_missed", "halves_holds", "halves_missed"):
        assert required in names
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice37():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "doubles" in proc.stdout.lower() or "double" in proc.stdout.lower()
