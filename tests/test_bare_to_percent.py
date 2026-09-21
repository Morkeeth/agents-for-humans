"""Slice 55 — bare word `three to four` · bare `twenty percent` / `20%`.

Found by running objects after S54:
  claimed_target("three to four") → None
  claimed_target("goes three to five") → None
  claimed_percent("twenty percent") → None
  claimed_percent("20%") → None
  claimed_percent("by twenty percent") → 20 but intent=unknown → no-direction
  Contrast: from three to four @4 held / @3 missed (naive held);
            twenty percent higher / +20% already grade percent-of-pop.
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


def test_goes_word_to_word_no_from():
    assert claimed_target("goes three to five")["value"] == 5
    missed = check_prediction(
        "goes three to five", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"


def test_bare_one_to_zero():
    assert claimed_target("one to zero")["value"] == 0
    held = check_prediction(
        "one to zero", "hurt", -1, population=5, latest_value=0
    )
    assert held["outcome"] == "prediction-held"


def test_from_word_to_regression():
    assert claimed_target("from three to four")["value"] == 4


def test_bare_twenty_percent():
    assert claimed_percent("twenty percent")["percent"] == 20
    assert prediction_intent("twenty percent") == "rise"
    magnet = check_prediction(
        "twenty percent", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "twenty percent", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"
    held = check_prediction(
        "twenty percent", "helped", 1, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"


def test_bare_digit_percent():
    assert claimed_percent("20%")["percent"] == 20
    assert claimed_percent("20 percent")["percent"] == 20
    assert prediction_intent("20%") == "rise"
    magnet = check_prediction("20%", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check(
        "20%", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_by_twenty_percent_no_longer_no_direction():
    """THE LIE: pct parsed, intent unknown → no-direction on true 20%."""
    assert claimed_percent("by twenty percent")["percent"] == 20
    assert prediction_intent("by twenty percent") == "rise"
    held = check_prediction(
        "by twenty percent", "helped", 1, population=5, latest_value=4
    )
    missed = check_prediction(
        "by twenty percent", "helped", 20, population=5, latest_value=24
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_signed_word_percent():
    assert prediction_intent("+twenty percent") == "rise"
    assert prediction_intent("-twenty percent") == "fall"
    assert claimed_percent("+twenty percent")["percent"] == 20
    held = check_prediction(
        "+twenty percent", "helped", 1, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"


def test_perfect_hundred_not_stolen_as_percent():
    """Bare percent must not steal 100% / 100 percent from perfect resolve."""
    assert claimed_percent("100%")["percent"] is None
    assert claimed_target("100%").get("perfect") is True
    assert claimed_percent("100 percent")["percent"] is None
    assert claimed_target("100 percent").get("perfect") is True
    held = check_prediction("100%", "helped", 1, population=5, latest_value=5)
    missed = check_prediction("100%", "helped", 1, population=5, latest_value=4)
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"


def test_pred_demo_includes_slice55():
    names = {s.name for s in SCENARIOS}
    for required in (
        "bare_word_to_missed",
        "bare_twenty_pct_missed",
        "bare_digit_pct_missed",
    ):
        assert required in names, required
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
