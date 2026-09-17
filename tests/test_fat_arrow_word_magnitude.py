"""Slice 50 — fat arrows ⬆▲ · word magnitudes · all green/passing.

Found by running objects:
  prediction_intent("⬆1") → unknown; claimed_magnitude → None
  claimed_magnitude("up by one") → None  # invents held on Δ=+20
  claimed_magnitude("one point") → None
  claimed_target("all green") → None
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_fat_arrows_intent_and_magnitude():
    for glyph, intent in (("⬆", "rise"), ("⬇", "fall"), ("▲", "rise"), ("▼", "fall")):
        text = f"{glyph}1"
        assert prediction_intent(text) == intent, text
        assert claimed_magnitude(text)["amount"] == 1, text


def test_fat_arrow_lie_misses():
    magnet = check_prediction("⬆1", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check("⬆1", "helped", 20, population=5, latest_value=24)
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_word_magnitudes():
    assert claimed_magnitude("up by one")["amount"] == 1
    assert claimed_magnitude("rises by one")["amount"] == 1
    assert claimed_magnitude("up one")["amount"] == 1
    assert claimed_magnitude("one point")["amount"] == 1
    assert claimed_magnitude("by a point")["amount"] == 1
    assert claimed_magnitude("rises by two")["amount"] == 2
    assert claimed_magnitude("two points")["amount"] == 2
    assert prediction_intent("up by one") == "rise"
    assert prediction_intent("down one") == "fall"


def test_word_magnitude_lie_misses():
    magnet = check_prediction(
        "up by one", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "up by one", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_all_green_passing_perfect():
    assert claimed_target("all green")["perfect"] is True
    assert claimed_target("all passing")["perfect"] is True
    assert claimed_target("passes all")["perfect"] is True
    missed = check_prediction(
        "all green", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "all green", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_thin_arrow_regression():
    assert prediction_intent("↑1") == "rise"
    assert claimed_magnitude("↓1")["amount"] == 1


def test_pred_demo_includes_slice50():
    names = {s.name for s in SCENARIOS}
    for required in (
        "fat_arrow_missed",
        "word_one_missed",
        "all_green_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice50():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
