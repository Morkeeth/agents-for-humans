"""Slice 48 — arrow glyphs ↑1/↓1 + unbound perfect score.

Found by running objects:
  prediction_intent("↑1") → unknown
  claimed_magnitude("↑1") → amount=None
  check_prediction("↑1", "helped", 1) → no-direction
  claimed_magnitude("↓1/5") → amount=None  # FRAC only knew ↑
  claimed_target("perfect score") → None → no-direction
  Contrast: up 1 / +1 / perfect 5/5 already grade.
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


def test_arrow_up_is_rise_with_magnitude():
    assert prediction_intent("↑1") == "rise"
    assert claimed_magnitude("↑1")["amount"] == 1
    assert prediction_intent("pass rate ↑1") == "rise"
    assert claimed_magnitude("↑ 1")["amount"] == 1


def test_arrow_down_is_fall_with_magnitude():
    assert prediction_intent("↓1") == "fall"
    assert claimed_magnitude("↓1")["amount"] == 1
    assert prediction_intent("pass rate ↓1") == "fall"
    assert claimed_magnitude("↓ 1")["amount"] == 1


def test_arrow_frac_both_glyphs():
    assert claimed_magnitude("↑1/5") == {
        "amount": 1,
        "population": 5,
        "raw": "↑1/5",
    }
    assert claimed_magnitude("↓1/5")["amount"] == 1
    assert claimed_magnitude("↓1/5")["population"] == 5
    assert prediction_intent("↑1/5") == "rise"
    assert prediction_intent("↓1/5") == "fall"


def test_arrow_true_magnitude_holds():
    c = check_prediction("↑1", "helped", 1, population=5, latest_value=4)
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+magnitude"


def test_arrow_absolute_lie_misses_naive_holds():
    """THE LIE: unbound ↑1 left no-direction; direction invents held on Δ=+20."""
    magnet = check_prediction("↑1", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check(
        "↑1", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "direction+magnitude"
    assert naive["outcome"] == "prediction-held"


def test_arrow_down_lie_misses():
    magnet = check_prediction("↓1", "hurt", -20, population=5, latest_value=0)
    naive = naive_direction_check(
        "↓1", "hurt", -20, population=5, latest_value=0
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_perfect_score_unbound_is_perfect_flag():
    t = claimed_target("perfect score")
    assert t["perfect"] is True
    assert t["value"] is None
    assert prediction_intent("perfect score") == "flat"
    assert claimed_target("a perfect score")["perfect"] is True
    assert claimed_target("perfect")["perfect"] is True
    assert claimed_target("full score")["perfect"] is True
    assert claimed_target("reaches a perfect score")["perfect"] is True


def test_perfect_score_resolves_to_population():
    held = check_prediction(
        "perfect score", "unchanged", 0, population=5, latest_value=5
    )
    assert held["outcome"] == "prediction-held"
    assert held["grade"] == "target"
    assert held["claimed_target"]["value"] == 5
    assert held["claimed_target"]["population"] == 5


def test_perfect_score_wrong_latest_misses_naive_holds():
    """THE LIE: unbound left no-direction; flat invents held off-perfect."""
    magnet = check_prediction(
        "perfect score", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "perfect score", "unchanged", 0, population=5, latest_value=4
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "target"
    assert naive["outcome"] == "prediction-held"


def test_perfect_score_needs_population():
    c = check_prediction(
        "perfect score", "unchanged", 0, population=None, latest_value=4
    )
    assert c["outcome"] == "no-direction"


def test_perfect_nn_still_explicit():
    """Slice 41 regression — explicit N/N is not the unbound path."""
    t = claimed_target("perfect 5/5")
    assert t["value"] == 5
    assert t["perfect"] is False


def test_pred_demo_includes_slice48():
    names = {s.name for s in SCENARIOS}
    for required in (
        "arrow_up_holds",
        "arrow_up_missed",
        "arrow_down_missed",
        "perfect_score_holds",
        "perfect_score_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice48():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
