"""Slice 63 — twenty-compound word levels (never steal one→twenty).

Found by running objects after S62:
  twenty-one to twenty-two → raw=`one to twenty` value=20
    → prediction-held @latest=20 (THE LIE — true dest is 22)
  twenty-first to twenty-second → raw=`first to twenty` value=20 held @20
  from twenty to twenty-one → raw=`from twenty to twenty` value=20 held @20
  Contrast: 21st to 22nd / from 21 to 22 dest=22 miss @20 hold @22.
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


def test_twenty_one_to_twenty_two():
    assert claimed_target("twenty-one to twenty-two")["value"] == 22
    assert claimed_target("twenty one to twenty two")["value"] == 22
    assert claimed_target("21st to 22nd")["value"] == 22
    missed = check_prediction(
        "twenty-one to twenty-two",
        "unchanged",
        0,
        population=30,
        latest_value=20,
    )
    held = check_prediction(
        "twenty-one to twenty-two",
        "unchanged",
        0,
        population=30,
        latest_value=22,
    )
    naive = naive_direction_check(
        "twenty-one to twenty-two",
        "unchanged",
        0,
        population=30,
        latest_value=20,
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"
    assert naive["outcome"] == "prediction-held"
    assert prediction_intent("twenty-one to twenty-two") == "flat"
    # Must not steal destination as bare twenty (value=20 was THE LIE)
    assert claimed_target("twenty-one to twenty-two")["raw"] == "twenty-one to twenty-two"


def test_twenty_first_to_twenty_second():
    assert claimed_target("twenty-first to twenty-second")["value"] == 22
    assert claimed_target("twenty first to twenty second")["value"] == 22
    missed = check_prediction(
        "twenty-first to twenty-second",
        "unchanged",
        0,
        population=30,
        latest_value=20,
    )
    assert missed["outcome"] == "prediction-missed"


def test_from_twenty_to_twenty_one():
    assert claimed_target("from twenty to twenty-one")["value"] == 21
    assert claimed_target("twenty to twenty-one")["value"] == 21
    missed = check_prediction(
        "from twenty to twenty-one",
        "unchanged",
        0,
        population=30,
        latest_value=20,
    )
    held = check_prediction(
        "from twenty to twenty-one",
        "unchanged",
        0,
        population=30,
        latest_value=21,
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"


def test_twenty_eight_to_twenty_nine():
    assert claimed_target("twenty-eight to twenty-nine")["value"] == 29
    held = check_prediction(
        "twenty-eight to twenty-nine",
        "unchanged",
        0,
        population=30,
        latest_value=29,
    )
    missed = check_prediction(
        "twenty-eight to twenty-nine",
        "unchanged",
        0,
        population=30,
        latest_value=28,
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_teens_and_digit_regression():
    assert claimed_target("fifteenth to sixteenth")["value"] == 16
    assert claimed_target("three to four")["value"] == 4
    assert claimed_target("21st to 22nd")["value"] == 22
    assert claimed_target("from 21 to 22")["value"] == 22


def test_pred_demo_includes_slice63():
    names = {s.name for s in SCENARIOS}
    for required in (
        "twenty_one_to_twenty_two_missed",
        "twenty_first_to_twenty_second_missed",
        "from_twenty_to_twenty_one_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    assert "twenty-one" in out.lower() or "Slice 63" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice63():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
