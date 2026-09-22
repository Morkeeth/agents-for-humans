"""Slice 60 — readout verbs + thirteenth/fourteenth word ordinals.

Found by running objects after S59:
  amounts to 4/5 / works out to 4/5 / evaluates to 4/5 → target=None
  totals 4/5 / registers at 4/5 / comes in at 4/5 → target=None
  posts 4/5 / yields 4/5 / nets 4/5 / returns 4/5 → target=None
  thirteenth to fourteenth → target=None while 13th to 14th grades
  Contrast: reads 4/5 / measures 4/5 / comes to 4/5 already grade.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_amounts_works_evaluates():
    for text in (
        "amounts to 4/5",
        "amount to 4",
        "amounts to four",
        "works out to 4/5",
        "work out to 4",
        "evaluates to 4/5",
        "evaluate to 4",
        "turns out 4/5",
        "turns out to be 4/5",
    ):
        assert claimed_target(text)["value"] == 4, text
        assert prediction_intent(text) == "flat", text
    missed = check_prediction(
        "amounts to 4/5", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "amounts to 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_totals_registers_comes_in():
    for text in (
        "totals 4/5",
        "total of 4/5",
        "totals four",
        "registers 4/5",
        "registers at 4/5",
        "comes in at 4/5",
        "checks in at 4/5",
    ):
        assert claimed_target(text)["value"] == 4, text


def test_posts_yields_nets_returns():
    for text in (
        "posts 4/5",
        "posts a 4/5",
        "posts four",
        "yields 4/5",
        "yielding 4/5",
        "nets 4/5",
        "netting 4/5",
        "returns 4/5",
        "returning 4/5",
    ):
        assert claimed_target(text)["value"] == 4, text
    # returns to still grades (pre-S60)
    assert claimed_target("returns to 4/5")["value"] == 4
    missed = check_prediction(
        "posts 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"


def test_thirteenth_to_fourteenth():
    tgt = claimed_target("thirteenth to fourteenth")
    assert tgt["value"] == 14
    assert claimed_target("from thirteenth to fourteenth")["value"] == 14
    assert claimed_target("thirteen to fourteen")["value"] == 14
    assert claimed_target("13th to 14th")["value"] == 14
    missed = check_prediction(
        "thirteenth to fourteenth",
        "unchanged",
        0,
        population=20,
        latest_value=13,
    )
    naive = naive_direction_check(
        "thirteenth to fourteenth",
        "unchanged",
        0,
        population=20,
        latest_value=13,
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_s59_regression():
    assert claimed_target("same as 4/5")["value"] == 4
    assert claimed_target("reads 4/5")["value"] == 4
    assert claimed_target("eleventh to twelfth")["value"] == 12


def test_pred_demo_includes_slice60():
    names = {s.name for s in SCENARIOS}
    for required in (
        "amounts_to_missed",
        "evaluates_to_missed",
        "posts_missed",
        "yields_missed",
        "thirteenth_to_fourteenth_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice60():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
