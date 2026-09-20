"""Slice 57 — word exactly / falls-to / reaches targets.

Found by running objects after S56:
  claimed_target("exactly four") → None; intent=flat
  check @latest=3 → prediction-held (direction invents held)
  claimed_target("falls to four") → None; hurt@1 invents held
  claimed_target("exactly twenty") → None
  Contrast: exactly 4 / falls to 4 / exactly 20 grade.
  Guard: exactly twenty percent stays percent (not target=20).
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


def test_exactly_four_destination():
    assert claimed_target("exactly four")["value"] == 4
    assert prediction_intent("exactly four") == "flat"
    held = check_prediction(
        "exactly four", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "exactly four", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "exactly four", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_exactly_four_five_frac():
    tgt = claimed_target("exactly four/five")
    assert tgt["value"] == 4
    assert tgt["population"] == 5


def test_exactly_twenty_tens_word():
    assert claimed_target("exactly twenty")["value"] == 20
    missed = check_prediction(
        "exactly twenty", "unchanged", 0, population=20, latest_value=19
    )
    assert missed["outcome"] == "prediction-missed"


def test_exactly_twenty_percent_not_stolen():
    assert claimed_target("exactly twenty percent")["value"] is None
    assert claimed_percent("exactly twenty percent")["percent"] == 20


def test_falls_to_four():
    assert claimed_target("falls to four")["value"] == 4
    held = check_prediction(
        "falls to four", "hurt", -1, population=5, latest_value=4
    )
    missed = check_prediction(
        "falls to four", "hurt", -1, population=5, latest_value=1
    )
    naive = naive_direction_check(
        "falls to four", "hurt", -1, population=5, latest_value=1
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_reaches_hits_ends_word():
    assert claimed_target("reaches five")["value"] == 5
    assert claimed_target("hits four")["value"] == 4
    assert claimed_target("ends at four")["value"] == 4
    assert prediction_intent("reaches five") == "flat"


def test_digit_exactly_regression():
    assert claimed_target("exactly 4")["value"] == 4
    assert claimed_target("exactly zero")["value"] == 0


def test_pred_demo_includes_slice57():
    names = {s.name for s in SCENARIOS}
    assert "exactly_four_missed" in names
    assert "falls_to_four_missed" in names
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
