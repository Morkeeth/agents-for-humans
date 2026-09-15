"""Slice 38 — below-bound floor compounds.

Found 2026-09-15 by running the object:
  claimed_floor("won't fall below 3/5") → None
  check_prediction(..., unchanged, latest=2) → prediction-held   # THE LIE

Also: stays above / never below / no lower than unbound; no lower than was fall.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_floor,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_wont_fall_below_parses_floor():
    floor = claimed_floor("won't fall below 3/5")
    assert floor["value"] == 3
    assert floor["population"] == 5
    assert floor["exclusive"] is False
    assert prediction_intent("won't fall below 3/5") == "flat"


def test_wont_fall_below_misses_when_below_bound():
    """THE LIE: unbound floor invented held at latest 2."""
    pred = "won't fall below 3/5"
    magnet = check_prediction(
        pred, "unchanged", 0, population=5, latest_value=2
    )
    naive = naive_direction_check(
        pred, "unchanged", 0, population=5, latest_value=2
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "floor"
    assert magnet["floor_ok"] is False
    assert naive["outcome"] == "prediction-held"


def test_wont_fall_below_holds_at_or_above():
    at = check_prediction(
        "won't fall below 3/5", "unchanged", 0, population=5, latest_value=3
    )
    above = check_prediction(
        "won't fall below 3/5", "unchanged", 0, population=5, latest_value=4
    )
    assert at["outcome"] == "prediction-held"
    assert above["outcome"] == "prediction-held"


def test_stays_above_is_exclusive_floor():
    floor = claimed_floor("stays above 3/5")
    assert floor["value"] == 3
    assert floor["exclusive"] is True
    assert prediction_intent("stays above 3/5") == "flat"
    miss = check_prediction(
        "stays above 3/5", "unchanged", 0, population=5, latest_value=3
    )
    hold = check_prediction(
        "stays above 3/5", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "stays above 3/5", "unchanged", 0, population=5, latest_value=3
    )
    assert miss["outcome"] == "prediction-missed"
    assert hold["outcome"] == "prediction-held"
    assert naive["outcome"] == "prediction-held"


def test_no_lower_than_is_flat_floor_not_fall():
    """'lower' in fall lexicon used to force intent=fall."""
    assert prediction_intent("no lower than 3/5") == "flat"
    floor = claimed_floor("no lower than 3/5")
    assert floor["value"] == 3
    c = check_prediction(
        "no lower than 3/5", "unchanged", 0, population=5, latest_value=3
    )
    assert c["outcome"] == "prediction-held"


def test_never_below_and_must_not_drop_under():
    assert claimed_floor("never below 4/5")["value"] == 4
    assert claimed_floor("must not drop under 4/5")["value"] == 4
    assert prediction_intent("never below 4/5") == "flat"
    assert prediction_intent("must not drop under 4/5") == "flat"


def test_pred_demo_includes_below_bound_scenarios():
    names = {s.name for s in SCENARIOS}
    for required in (
        "wont_fall_below_holds",
        "wont_fall_below_missed",
        "stays_above_holds",
        "stays_above_missed",
        "no_lower_than_holds",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice38():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "won't fall below" in proc.stdout.lower() or "below" in proc.stdout.lower()
