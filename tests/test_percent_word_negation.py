"""Slice 40 — word-percent absolute honesty + never/cannot negation.

Found 2026-09-16 by running objects:
  claimed_percent("improves by 20 percent") → None
  claimed_magnitude(...) → amount=20
  Δ=+1/pop5 → missed; Δ=+20 → held  # invents absolute points for the word
  prediction_intent("never falls") → fall
  check_prediction(..., "hurt") → prediction-held  # invents held on drop
  "won't decrease" → fall (decrease in fall lexicon, missing from negation)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    claimed_percent,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_word_percent_parses():
    for text in (
        "improves by 20 percent",
        "improves by 20 per cent",
        "rises 20 percent",
        "20 percent improvement",
        "20 pct improvement",
        "+20 percent",
        "up 20 percent",
        "falls by 20 percent",
    ):
        assert claimed_percent(text)["percent"] == 20, text
        assert claimed_magnitude(text)["amount"] is None, text


def test_word_percent_symbol_still_works():
    assert claimed_percent("improves by 20%")["percent"] == 20
    assert claimed_percent("rises 20%")["percent"] == 20
    assert claimed_magnitude("improves by 20%")["amount"] is None


def test_word_percent_grades_pop_not_absolute():
    held = check_prediction(
        "improves by 20 percent", "helped", 1, population=5, latest_value=4
    )
    missed = check_prediction(
        "improves by 20 percent", "helped", 20, population=5, latest_value=5
    )
    naive = naive_direction_check(
        "improves by 20 percent", "helped", 20, population=5, latest_value=5
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"  # direction invents held


def test_never_cannot_decrease_are_flat():
    for text in (
        "never falls",
        "cannot fall",
        "can't drop",
        "won't decrease",
        "will not decrease",
        "does not decrease",
        "never decreases",
        "cannot decrease",
        "no decrease",
        "without decreasing",
        "never worsens",
        "cannot worsen",
    ):
        assert prediction_intent(text) == "flat", text


def test_never_falls_does_not_invent_held_on_hurt():
    # THE LIE: intent=fall → hurt → prediction-held
    flat = check_prediction("never falls", "unchanged", 0, population=5, latest_value=3)
    hurt = check_prediction("never falls", "hurt", -1, population=5, latest_value=2)
    assert flat["outcome"] == "prediction-held"
    assert hurt["outcome"] == "prediction-missed"


def test_wont_decrease_hurt_is_missed():
    out = check_prediction("won't decrease", "hurt", -1, population=5, latest_value=2)
    assert out["intent"] == "flat"
    assert out["outcome"] == "prediction-missed"
    naive = naive_direction_check(
        "won't decrease", "hurt", -1, population=5, latest_value=2
    )
    # After fix, naive also sees flat intent — embarrassment is word-percent rows.
    # Pre-fix naive would have been fall→held; we refuse to ship that lie as naive.
    assert naive["intent"] == "flat"


def test_pred_demo_includes_slice40():
    names = {s.name for s in SCENARIOS}
    for required in (
        "word_percent_holds",
        "word_percent_missed",
        "never_falls_flat_holds",
        "never_falls_hurt_missed",
        "wont_decrease_hurt_missed",
        "cannot_fall_flat_holds",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out
    assert "20 percent" in out or "never falls" in out


def test_pred_demo_cli_exit_0_slice40():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
    assert "percent" in proc.stdout.lower() or "never falls" in proc.stdout.lower()
