"""Slice 55 — bare three→four + bare twenty percent.

Found by running objects after S54:
  claimed_target("three to four") → None
  claimed_target("3 to 4") → None
  claimed_target("3/5 to 4/5") → None
  claimed_percent("twenty percent") → None
  claimed_percent("20%") → None
  prediction_intent("by twenty percent") → unknown (pct parsed, never graded)

Contrast: from three to four / twenty percent higher / by 20% with rise word.
THE LIE: no-direction while a destination/percent sat on the table; or
direction invents held on absolute Δ=+20 while 20% of pop 5 is +1.
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


def test_bare_word_to_destination():
    tgt = claimed_target("three to four")
    assert tgt["value"] == 4
    assert prediction_intent("three to four") == "flat"
    held = check_prediction(
        "three to four", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "three to four", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "three to four", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_goes_bare_word_to():
    assert claimed_target("goes three to four")["value"] == 4
    missed = check_prediction(
        "goes three to five", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"


def test_bare_digit_to_destination():
    assert claimed_target("3 to 4")["value"] == 4
    assert claimed_target("goes 3 to 4")["value"] == 4
    frac = claimed_target("3/5 to 4/5")
    assert frac["value"] == 4
    assert frac["population"] == 5
    held = check_prediction("3 to 4", "unchanged", 0, population=5, latest_value=4)
    missed = check_prediction("3 to 4", "unchanged", 0, population=5, latest_value=3)
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_bare_zero_to_one():
    assert claimed_target("zero to one")["value"] == 1
    assert claimed_target("one to zero")["value"] == 0
    held = check_prediction(
        "one to zero", "hurt", -1, population=5, latest_value=0
    )
    missed = check_prediction(
        "one to zero", "hurt", -1, population=5, latest_value=1
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_from_word_to_regression():
    assert claimed_target("from three to four")["value"] == 4
    assert claimed_target("from 3 to 4")["value"] == 4


def test_bare_twenty_percent():
    assert claimed_percent("twenty percent")["percent"] == 20
    assert claimed_percent("20%")["percent"] == 20
    assert prediction_intent("twenty percent") == "rise"
    assert prediction_intent("20%") == "rise"
    # THE LIE: absolute Δ=+20 invents held; true 20% of pop 5 is +1
    missed = check_prediction(
        "twenty percent", "helped", 20, population=5, latest_value=24
    )
    held = check_prediction(
        "twenty percent", "helped", 1, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "twenty percent", "helped", 20, population=5, latest_value=24
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"
    assert naive["outcome"] == "prediction-held"


def test_by_percent_without_rise_word():
    """pct already parsed; intent was unknown → no-direction. Now rise."""
    assert claimed_percent("by twenty percent")["percent"] == 20
    assert prediction_intent("by twenty percent") == "rise"
    assert prediction_intent("by 20%") == "rise"
    missed = check_prediction(
        "by twenty percent", "helped", 20, population=5, latest_value=24
    )
    held = check_prediction(
        "by 20%", "helped", 1, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"
    assert held["outcome"] == "prediction-held"


def test_bare_percent_does_not_steal_perfect_100():
    assert claimed_percent("100%")["percent"] is None
    assert claimed_target("100%")["perfect"] is True
    held = check_prediction("100%", "unchanged", 0, population=5, latest_value=5)
    missed = check_prediction("100%", "unchanged", 0, population=5, latest_value=4)
    naive = naive_direction_check(
        "100%", "unchanged", 0, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_word_percent_higher_regression():
    assert claimed_percent("twenty percent higher")["percent"] == 20
    assert prediction_intent("twenty percent higher") == "rise"


def test_pred_demo_includes_slice55():
    names = {s.name for s in SCENARIOS}
    assert "bare_three_to_four_missed" in names
    assert "bare_twenty_percent_missed" in names
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice55():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
