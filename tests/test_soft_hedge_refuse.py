"""Slice 62 — soft-hedge refuse (never invent exact held).

Found by running objects after S61:
  must stay at roughly 4/5 @latest=3 → prediction-held (direction)
  roughly equals 4/5 / almost exactly 4/5 → target=4 invents exact held
  same as about 4/5 → flat invents held
  roughly stay at 4/5 → level=4 invents exact held
  roughly at least 4/5 → floor=4 invents exact held
  won't fall below about 3/5 @2 → direction invents held
  improves by roughly 20% / roughly doubles / almost doubles invent exact
  Contrast: must stay at 4/5 / exactly 4/5 / same as 4/5 / doubles grade.
  Non-hedge about (about to rise / talk about) must not refuse.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_floor,
    claimed_level,
    claimed_percent,
    claimed_ratio,
    claimed_target,
    is_soft_hedged,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_must_stay_at_roughly_refuses():
    text = "must stay at roughly 4/5"
    assert is_soft_hedged(text)
    assert claimed_level(text)["value"] is None
    r = check_prediction(
        text, "unchanged", 0, population=5, latest_value=3
    )
    n = naive_direction_check(
        text, "unchanged", 0, population=5, latest_value=3
    )
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"
    assert r["grade"] == "soft-hedge"


def test_almost_exactly_refuses_exact_target():
    text = "almost exactly 4/5"
    assert is_soft_hedged(text)
    assert claimed_target(text)["value"] is None
    r = check_prediction(
        text, "unchanged", 0, population=5, latest_value=4
    )
    n = naive_direction_check(
        text, "unchanged", 0, population=5, latest_value=4
    )
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"


def test_roughly_equals_refuses():
    text = "roughly equals 4/5"
    assert is_soft_hedged(text)
    assert claimed_target(text)["value"] is None
    r = check_prediction(
        text, "unchanged", 0, population=5, latest_value=4
    )
    assert r["outcome"] == "no-direction"


def test_same_as_about_refuses():
    text = "same as about 4/5"
    assert is_soft_hedged(text)
    assert claimed_target(text)["value"] is None
    r = check_prediction(
        text, "unchanged", 0, population=5, latest_value=3
    )
    n = naive_direction_check(
        text, "unchanged", 0, population=5, latest_value=3
    )
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"


def test_roughly_stay_at_refuses_exact_level():
    text = "roughly stay at 4/5"
    assert is_soft_hedged(text)
    assert claimed_level(text)["value"] is None
    r = check_prediction(
        text, "unchanged", 0, population=5, latest_value=4
    )
    n = naive_direction_check(
        text, "unchanged", 0, population=5, latest_value=4
    )
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"


def test_roughly_at_least_refuses_exact_floor():
    text = "roughly at least 4/5"
    assert is_soft_hedged(text)
    assert claimed_floor(text)["value"] is None
    r = check_prediction(
        text, "unchanged", 0, population=5, latest_value=4
    )
    assert r["outcome"] == "no-direction"


def test_wont_fall_below_about_refuses():
    text = "won't fall below about 3/5"
    assert is_soft_hedged(text)
    assert claimed_floor(text)["value"] is None
    r = check_prediction(
        text, "unchanged", 0, population=5, latest_value=2
    )
    n = naive_direction_check(
        text, "unchanged", 0, population=5, latest_value=2
    )
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"


def test_roughly_percent_refuses():
    text = "improves by roughly 20%"
    assert is_soft_hedged(text)
    assert claimed_percent(text)["percent"] is None
    r = check_prediction(
        text, "helped", 1, population=5, latest_value=4
    )
    n = naive_direction_check(
        text, "helped", 1, population=5, latest_value=4
    )
    assert r["outcome"] == "no-direction"
    assert n["outcome"] == "prediction-held"


def test_roughly_doubles_refuses():
    for text in ("roughly doubles", "almost doubles", "nearly halves"):
        assert is_soft_hedged(text), text
        assert claimed_ratio(text)["kind"] is None, text
        r = check_prediction(
            text, "helped", 2, population=5, latest_value=4
        )
        assert r["outcome"] == "no-direction", text


def test_exact_forms_still_grade():
    assert not is_soft_hedged("must stay at 4/5")
    assert claimed_level("must stay at 4/5")["value"] == 4
    held = check_prediction(
        "must stay at 4/5", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "must stay at 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert claimed_target("exactly 4/5")["value"] == 4
    assert claimed_target("same as 4/5")["value"] == 4
    assert claimed_percent("improves by 20%")["percent"] == 20
    assert claimed_ratio("doubles")["kind"] == "double"
    assert claimed_floor("at least 4/5")["value"] == 4


def test_non_hedge_about_does_not_refuse():
    for text in (
        "about to rise by 1",
        "talk about skills",
        "bring about a rise",
    ):
        assert not is_soft_hedged(text), text
    # about to rise still grades as rise+magnitude
    assert prediction_intent("about to rise by 1") == "rise"
    held = check_prediction(
        "about to rise by 1", "helped", 1, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"


def test_hedge_variants():
    for text in (
        "approximately equals 4/5",
        "nearly exactly 4/5",
        "about equal to 4/5",
        "nearly equal to 4/5",
        "almost equal to 4/5",
        "about 20 percent",
        "roughly 20% higher",
    ):
        assert is_soft_hedged(text), text
        r = check_prediction(
            text, "unchanged", 0, population=5, latest_value=4
        )
        assert r["outcome"] == "no-direction", text


def test_pred_demo_includes_slice62():
    names = {s.name for s in SCENARIOS}
    for required in (
        "soft_stay_roughly_refused",
        "soft_almost_exactly_refused",
        "soft_same_as_about_refused",
        "soft_roughly_stay_refused",
        "soft_below_about_refused",
        "soft_roughly_percent_refused",
        "soft_roughly_doubles_refused",
        "soft_almost_doubles_refused",
        "soft_roughly_equals_refused",
        "soft_nearly_exactly_refused",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    assert "soft hedge" in out.lower() or "Slice 62" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice62():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
