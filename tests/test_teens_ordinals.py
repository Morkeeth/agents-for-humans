"""Slice 61 — word ordinals fifteenth…nineteenth.

Found by running objects after S60:
  fifteenth to sixteenth → target=None while 15th to 16th grades
  seventeenth to eighteenth → target=None while 17th to 18th grades
  nineteenth to twentieth → target=None while 19th to 20th grades
  fifteen to sixteen → target=None
  Contrast: thirteenth to fourteenth (S60) already grades.
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


def test_fifteenth_to_sixteenth():
    assert claimed_target("fifteenth to sixteenth")["value"] == 16
    assert claimed_target("fifteen to sixteen")["value"] == 16
    assert claimed_target("15th to 16th")["value"] == 16
    missed = check_prediction(
        "fifteenth to sixteenth",
        "unchanged",
        0,
        population=20,
        latest_value=15,
    )
    naive = naive_direction_check(
        "fifteenth to sixteenth",
        "unchanged",
        0,
        population=20,
        latest_value=15,
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"
    assert prediction_intent("fifteenth to sixteenth") == "flat"


def test_seventeenth_to_eighteenth():
    assert claimed_target("seventeenth to eighteenth")["value"] == 18
    assert claimed_target("seventeen to eighteen")["value"] == 18
    assert claimed_target("17th to 18th")["value"] == 18
    missed = check_prediction(
        "seventeenth to eighteenth",
        "unchanged",
        0,
        population=20,
        latest_value=17,
    )
    assert missed["outcome"] == "prediction-missed"


def test_nineteenth_to_twentieth():
    assert claimed_target("nineteenth to twentieth")["value"] == 20
    assert claimed_target("nineteen to twenty")["value"] == 20
    assert claimed_target("19th to 20th")["value"] == 20
    held = check_prediction(
        "nineteenth to twentieth",
        "unchanged",
        0,
        population=20,
        latest_value=20,
    )
    missed = check_prediction(
        "nineteenth to twentieth",
        "unchanged",
        0,
        population=20,
        latest_value=19,
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_lower_ordinal_regression():
    assert claimed_target("third to fourth")["value"] == 4
    assert claimed_target("eleventh to twelfth")["value"] == 12
    assert claimed_target("thirteenth to fourteenth")["value"] == 14


def test_pred_demo_includes_slice61():
    names = {s.name for s in SCENARIOS}
    for required in (
        "fifteenth_to_sixteenth_missed",
        "seventeenth_to_eighteenth_missed",
        "nineteenth_to_twentieth_missed",
        "fifteen_to_sixteen_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice61():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
