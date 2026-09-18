"""Slice 51 — gains/loses/plus/minus · bare a-point magnitude.

Found by running objects after S50:
  prediction_intent("gains one") → rise; claimed_magnitude → amount=None
  check_prediction("gains one", "helped", 20) → prediction-held  # THE LIE
  claimed_magnitude("up a point") → None  # by a point already graded
  prediction_intent("loses one") → unknown; amount=None
  prediction_intent("plus 1") → unknown; amount=None before digit claim
  Contrast: gains by one / up by a point / improves one already grade.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_gains_one_intent_and_magnitude():
    assert prediction_intent("gains one") == "rise"
    assert claimed_magnitude("gains one")["amount"] == 1
    assert prediction_intent("gains 1") == "rise"
    assert claimed_magnitude("gains 1")["amount"] == 1
    assert claimed_magnitude("gain one")["amount"] == 1


def test_gains_one_lie_misses():
    magnet = check_prediction("gains one", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check(
        "gains one", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"
    held = check_prediction("gains one", "helped", 1, population=5, latest_value=4)
    assert held["outcome"] == "prediction-held"


def test_a_point_without_by():
    assert claimed_magnitude("up a point")["amount"] == 1
    assert claimed_magnitude("rises a point")["amount"] == 1
    assert claimed_magnitude("down a point")["amount"] == 1
    magnet = check_prediction(
        "up a point", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "up a point", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_loses_one_fall_magnitude():
    assert prediction_intent("loses one") == "fall"
    assert claimed_magnitude("loses one")["amount"] == 1
    assert prediction_intent("loses 1") == "fall"
    assert claimed_magnitude("lose one")["amount"] == 1
    magnet = check_prediction("loses one", "hurt", -20, population=5, latest_value=0)
    naive = naive_direction_check(
        "loses one", "hurt", -20, population=5, latest_value=0
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_plus_minus_word_forms():
    assert prediction_intent("plus 1") == "rise"
    assert claimed_magnitude("plus 1")["amount"] == 1
    assert prediction_intent("minus 1") == "fall"
    assert claimed_magnitude("minus 1")["amount"] == 1
    assert prediction_intent("plus one") == "rise"
    assert claimed_magnitude("plus one")["amount"] == 1
    assert prediction_intent("minus one") == "fall"
    magnet = check_prediction("plus 1", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check("plus 1", "helped", 20, population=5, latest_value=24)
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_adds_subtracts():
    assert prediction_intent("adds 1") == "rise"
    assert claimed_magnitude("adds 1")["amount"] == 1
    assert prediction_intent("subtracts 1") == "fall"
    assert claimed_magnitude("subtracts 1")["amount"] == 1
    assert claimed_magnitude("adds one")["amount"] == 1
    assert claimed_magnitude("subtracts one")["amount"] == 1


def test_regresses_intent():
    assert prediction_intent("regresses by one") == "fall"
    assert claimed_magnitude("regresses by one")["amount"] == 1


def test_pred_demo_includes_slice51():
    names = {s.name for s in SCENARIOS}
    for required in (
        "gains_one_missed",
        "up_a_point_missed",
        "plus_1_missed",
        "loses_one_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice51():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
