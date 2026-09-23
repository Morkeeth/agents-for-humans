"""Slice 64 — around / close-to / ~ soft-hedge refuse.

Found by running objects after S63:
  must stay at around 4/5 @3 → prediction-held (flat invents)
  around equals 4/5 → target=4 invents exact held @4
  must stay at close to 4/5 @3 → prediction-held
  must stay at ~4/5 @3 → prediction-held
  Contrast: roughly/about (S62) already refuse; must stay at 4/5 grades.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_target,
    is_soft_hedged,
    naive_direction_check,
)

ROOT = Path(__file__).resolve().parents[1]


def test_must_stay_at_around_refuses():
    text = "must stay at around 4/5"
    assert is_soft_hedged(text)
    r = check_prediction(text, "unchanged", 0, population=5, latest_value=3)
    n = naive_direction_check(text, "unchanged", 0, population=5, latest_value=3)
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"


def test_around_equals_refuses_exact_target():
    text = "around equals 4/5"
    assert is_soft_hedged(text)
    assert claimed_target(text)["value"] is None
    r = check_prediction(text, "unchanged", 0, population=5, latest_value=4)
    assert r["outcome"] == "no-direction"


def test_must_stay_at_close_to_refuses():
    text = "must stay at close to 4/5"
    assert is_soft_hedged(text)
    r = check_prediction(text, "unchanged", 0, population=5, latest_value=3)
    n = naive_direction_check(text, "unchanged", 0, population=5, latest_value=3)
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"


def test_tilde_soft_hedge_refuses():
    for text in ("must stay at ~4/5", "must stay at ≈4/5", "~4/5", "≈4/5"):
        assert is_soft_hedged(text), text
        r = check_prediction(text, "unchanged", 0, population=5, latest_value=3)
        assert r["outcome"] == "no-direction", text
    n = naive_direction_check(
        "must stay at ~4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert n["outcome"] == "prediction-held"


def test_circa_and_around_bare():
    for text in ("around 4/5", "circa 4/5"):
        assert is_soft_hedged(text), text
        assert check_prediction(
            text, "unchanged", 0, population=5, latest_value=4
        )["outcome"] == "no-direction"


def test_s62_regression_and_exact_still_grades():
    assert is_soft_hedged("must stay at roughly 4/5")
    assert check_prediction(
        "must stay at roughly 4/5", "unchanged", 0, population=5, latest_value=3
    )["outcome"] == "no-direction"
    assert not is_soft_hedged("must stay at 4/5")
    assert check_prediction(
        "must stay at 4/5", "unchanged", 0, population=5, latest_value=4
    )["outcome"] == "prediction-held"
    assert not is_soft_hedged("about to rise by 1")


def test_pred_demo_includes_slice64():
    names = {s.name for s in SCENARIOS}
    for required in (
        "soft_around_stay_refused",
        "soft_close_to_stay_refused",
        "soft_tilde_stay_refused",
        "soft_around_equals_refused",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    assert "around" in out.lower() or "Slice 64" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice64():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
