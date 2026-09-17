"""Slice 49 — climbs/slips magnitude · grows/shrinks intent · out-of/full marks/100%.

Found by running objects:
  claimed_magnitude("climbs 1") → None  # intent=rise → invents held on Δ=+20
  claimed_magnitude("slips 1") → None
  prediction_intent("grows by 1") → unknown  # amount=1 → no-direction
  prediction_intent("shrinks by 1") → unknown
  claimed_target("5 out of 5") → None
  claimed_target("score of 5/5") → None
  claimed_target("full marks") → None
  claimed_target("100%") → None
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_ceiling,
    claimed_magnitude,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_climbs_one_magnitude():
    assert prediction_intent("climbs 1") == "rise"
    assert claimed_magnitude("climbs 1")["amount"] == 1


def test_slips_one_magnitude():
    assert prediction_intent("slips 1") == "fall"
    assert claimed_magnitude("slips 1")["amount"] == 1


def test_climbs_lie_misses_naive_holds():
    magnet = check_prediction("climbs 1", "helped", 20, population=5, latest_value=24)
    naive = naive_direction_check(
        "climbs 1", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "direction+magnitude"
    assert naive["outcome"] == "prediction-held"


def test_grows_shrinks_intent():
    assert prediction_intent("grows by 1") == "rise"
    assert claimed_magnitude("grows by 1")["amount"] == 1
    assert prediction_intent("shrinks by 1") == "fall"
    assert claimed_magnitude("shrinks by 1")["amount"] == 1


def test_grows_lie_misses_naive_holds():
    magnet = check_prediction(
        "grows by 1", "helped", 20, population=5, latest_value=24
    )
    naive = naive_direction_check(
        "grows by 1", "helped", 20, population=5, latest_value=24
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_out_of_is_target():
    t = claimed_target("5 out of 5")
    assert t["value"] == 5
    assert t["population"] == 5
    assert prediction_intent("5 out of 5") == "flat"


def test_out_of_wrong_latest_misses():
    magnet = check_prediction(
        "5 out of 5", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "5 out of 5", "unchanged", 0, population=5, latest_value=4
    )
    assert magnet["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_score_of_is_target():
    t = claimed_target("score of 5/5")
    assert t["value"] == 5
    assert t["population"] == 5
    assert claimed_target("score of 5")["value"] == 5


def test_full_marks_and_100_percent_are_perfect():
    assert claimed_target("full marks")["perfect"] is True
    assert claimed_target("100%")["perfect"] is True
    assert claimed_target("one hundred percent")["perfect"] is True
    missed = check_prediction(
        "100%", "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        "100%", "unchanged", 0, population=5, latest_value=4
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_tops_out_and_caps():
    assert claimed_target("tops out at 5")["value"] == 5
    assert claimed_target("maxes out at 5/5")["value"] == 5
    assert claimed_ceiling("caps at 5")["value"] == 5


def test_pred_demo_includes_slice49():
    names = {s.name for s in SCENARIOS}
    for required in (
        "climbs_holds",
        "climbs_missed",
        "grows_missed",
        "out_of_holds",
        "out_of_missed",
        "full_marks_missed",
        "hundred_pct_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice49():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
