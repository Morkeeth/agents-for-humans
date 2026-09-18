"""Slice 52 — 100 percent · N of N · scores/still · green/failures.

Found by running objects after S51:
  claimed_target("100 percent") → None  # 100% already grades
  claimed_target("5 of 5") → None       # 5 out of 5 grades
  claimed_target("scores 5/5") → None
  claimed_target("stays green") → None
  check_prediction("remains green", "unchanged", 0, latest=4)
    → prediction-held  # THE LIE: flat without perfect resolve
  Contrast: 100% / 5 out of 5 / hits 5/5 / all green grade.
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


def test_hundred_percent_word_forms():
    for text in ("100 percent", "100 pct", "100 per cent"):
        assert claimed_target(text)["perfect"] is True, text
        assert prediction_intent(text) == "flat", text
    missed = check_prediction(
        "100 percent", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "100 percent", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_n_of_n_without_out():
    tgt = claimed_target("5 of 5")
    assert tgt["value"] == 5 and tgt["population"] == 5
    assert prediction_intent("5 of 5") == "flat"
    # regression: out of still works
    assert claimed_target("5 out of 5")["value"] == 5
    missed = check_prediction("5 of 5", "unchanged", 0, population=5, latest_value=4)
    naive = naive_direction_check(
        "5 of 5", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_scores_gets_still_slash():
    for text in ("scores 5/5", "gets 5/5", "marks 5/5", "still 5/5"):
        tgt = claimed_target(text)
        assert tgt["value"] == 5 and tgt["population"] == 5, text
        assert prediction_intent(text) == "flat", text
    missed = check_prediction(
        "scores 5/5", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "scores 5/5", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_remains_green_lie_misses():
    """THE LIE: remains green was flat inventing held @ latest=4."""
    assert claimed_target("remains green")["perfect"] is True
    magnet = check_prediction(
        "remains green", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "remains green", "unchanged", 0, population=5, latest_value=4
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"
    held = check_prediction(
        "remains green", "unchanged", 0, population=5, latest_value=5
    )
    assert held["outcome"] == "prediction-held"


def test_stays_still_green_and_failures():
    for text in (
        "stays green",
        "still green",
        "back to green",
        "zero failures",
        "no failures",
        "all tests pass",
        "everything passes",
        "flawless",
        "clean sweep",
    ):
        assert claimed_target(text)["perfect"] is True, text
        missed = check_prediction(
            text, "unchanged", 0, population=5, latest_value=4
        )
        assert missed["outcome"] == "prediction-missed", text


def test_pred_demo_includes_slice52():
    names = {s.name for s in SCENARIOS}
    for required in (
        "hundred_percent_word_missed",
        "n_of_n_missed",
        "scores_slash_missed",
        "remains_green_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice52():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
