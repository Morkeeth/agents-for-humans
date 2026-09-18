"""Slice 53 — emoji FE0F arrows · double-struck · word-number percent.

Found by running objects after S52:
  '⬆️1' codepoints U+2B06,U+FE0F,U+31 → intent=rise amount=None
  check_prediction → prediction-held on Δ=+20  # THE LIE
  '⇑1' / '⇧1' / '🔼1' → fully unbound
  'twenty percent higher' → rise pct=None → held on Δ=+20
    (true 20% of pop 5 is +1)
  Contrast: ⬆1 / 20% higher / improves by 20 percent already grade.
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


def test_emoji_fe0f_arrow_magnitude():
    assert prediction_intent("⬆️1") == "rise"
    assert claimed_magnitude("⬆️1")["amount"] == 1
    assert prediction_intent("⬇️1") == "fall"
    assert claimed_magnitude("⬇️1")["amount"] == 1


def test_emoji_arrow_lie_misses():
    magnet = check_prediction("⬆️1", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check("⬆️1", "helped", 20, population=5, latest_value=24)
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"
    held = check_prediction("⬆️1", "helped", 1, population=5, latest_value=4)
    assert held["outcome"] == "prediction-held"


def test_double_struck_and_triangle_arrows():
    for glyph, intent in (
        ("⇑", "rise"),
        ("⇓", "fall"),
        ("⇧", "rise"),
        ("⇩", "fall"),
        ("🔼", "rise"),
        ("🔽", "fall"),
    ):
        text = f"{glyph}1"
        assert prediction_intent(text) == intent, text
        assert claimed_magnitude(text)["amount"] == 1, text


def test_word_twenty_percent():
    assert claimed_percent("twenty percent higher")["percent"] == 20
    assert claimed_percent("improves by twenty percent")["percent"] == 20
    assert claimed_percent("rises twenty percent")["percent"] == 20
    magnet = check_prediction(
        "twenty percent higher", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "twenty percent higher", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"
    held = check_prediction(
        "improves by twenty percent", "helped", 1, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"


def test_word_fifty_percent_better():
    assert claimed_percent("fifty percent better")["percent"] == 50


def test_pred_demo_includes_slice53():
    names = {s.name for s in SCENARIOS}
    for required in (
        "emoji_arrow_missed",
        "double_struck_missed",
        "word_twenty_pct_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice53():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
