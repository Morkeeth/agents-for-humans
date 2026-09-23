"""Slice 65 — decade compounds + hundred (never steal nine→one).

Found by running objects after S64:
  ninety-nine to one hundred → raw=`nine to one` value=1
    → prediction-held @latest=1 (THE LIE — true dest is 100)
  thirty-one to thirty-two unbound while 31st to 32nd grades.
  Contrast: twenty-one to twenty-two (S63) already grades.
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
)

ROOT = Path(__file__).resolve().parents[1]


def test_ninety_nine_to_one_hundred():
    assert claimed_target("ninety-nine to one hundred")["value"] == 100
    assert claimed_target("ninety nine to one hundred")["value"] == 100
    assert claimed_target("from 99 to 100")["value"] == 100
    missed = check_prediction(
        "ninety-nine to one hundred",
        "unchanged",
        0,
        population=100,
        latest_value=1,
    )
    held = check_prediction(
        "ninety-nine to one hundred",
        "unchanged",
        0,
        population=100,
        latest_value=100,
    )
    naive = naive_direction_check(
        "ninety-nine to one hundred",
        "unchanged",
        0,
        population=100,
        latest_value=1,
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"
    assert naive["outcome"] == "prediction-held"
    # Must not steal dest=1
    assert claimed_target("ninety-nine to one hundred")["value"] != 1


def test_thirty_one_to_thirty_two():
    assert claimed_target("thirty-one to thirty-two")["value"] == 32
    assert claimed_target("thirty-first to thirty-second")["value"] == 32
    assert claimed_target("31st to 32nd")["value"] == 32
    missed = check_prediction(
        "thirty-one to thirty-two",
        "unchanged",
        0,
        population=100,
        latest_value=30,
    )
    assert missed["outcome"] == "prediction-missed"


def test_from_thirty_to_thirty_one():
    assert claimed_target("from thirty to thirty-one")["value"] == 31
    missed = check_prediction(
        "from thirty to thirty-one",
        "unchanged",
        0,
        population=100,
        latest_value=30,
    )
    held = check_prediction(
        "from thirty to thirty-one",
        "unchanged",
        0,
        population=100,
        latest_value=31,
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"


def test_eighty_eight_to_eighty_nine():
    assert claimed_target("eighty-eight to eighty-nine")["value"] == 89
    assert claimed_target("forty-one to forty-two")["value"] == 42


def test_twenty_nine_to_thirty():
    assert claimed_target("twenty-nine to thirty")["value"] == 30
    missed = check_prediction(
        "twenty-nine to thirty",
        "unchanged",
        0,
        population=100,
        latest_value=29,
    )
    held = check_prediction(
        "twenty-nine to thirty",
        "unchanged",
        0,
        population=100,
        latest_value=30,
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"


def test_s63_regression():
    assert claimed_target("twenty-one to twenty-two")["value"] == 22
    assert claimed_target("fifteenth to sixteenth")["value"] == 16


def test_pred_demo_includes_slice65():
    names = {s.name for s in SCENARIOS}
    for required in (
        "ninety_nine_to_hundred_missed",
        "thirty_one_to_thirty_two_missed",
        "from_thirty_to_thirty_one_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    assert "ninety-nine" in out.lower() or "Slice 65" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice65():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
