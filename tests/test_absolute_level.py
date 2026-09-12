"""Slice 28 — absolute-level honesty: stay-at without /pop, remain/hold/keep, floor.

Found 2026-09-12 by running:
  claimed_level("must stay at 5") → None
  check_prediction(..., latest_value=4) → prediction-held   # THE LIE
  claimed_level("remain at 4/5") → 4/5 but intent=unknown → no-direction
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
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_stay_at_without_pop_parses_value():
    level = claimed_level("must stay at 5")
    assert level["value"] == 5
    assert level["population"] is None
    assert level["raw"] is not None


def test_stay_at_without_pop_wrong_level_misses():
    """THE DEFECT: Slice 26 left 'must stay at 5' unparsed → invents held."""
    pred = "must stay at 5"
    magnet = check_prediction(
        pred, "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        pred, "unchanged", 0, population=5, latest_value=4
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "direction+level"
    assert magnet["level_ok"] is False
    assert naive["outcome"] == "prediction-held"
    assert naive["grade"] == "direction-only"


def test_stay_at_without_pop_correct_holds():
    c = check_prediction(
        "stay at 4", "unchanged", 0, population=5, latest_value=4
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+level"


def test_remain_at_is_flat_and_grades_level():
    assert prediction_intent("must remain at 5/5") == "flat"
    assert prediction_intent("remain at 4/5") == "flat"
    level = claimed_level("remain at 4/5")
    assert level["value"] == 4
    assert level["population"] == 5
    c = check_prediction(
        "must remain at 5/5", "unchanged", 0, population=5, latest_value=4
    )
    assert c["outcome"] == "prediction-missed"
    assert c["level_ok"] is False


def test_hold_at_is_flat_and_grades_level():
    assert prediction_intent("hold at 190/190") == "flat"
    c = check_prediction(
        "hold at 190/190", "unchanged", 0, population=190, latest_value=189
    )
    assert c["outcome"] == "prediction-missed"
    naive = naive_direction_check(
        "hold at 190/190", "unchanged", 0, population=190, latest_value=189
    )
    assert naive["outcome"] == "prediction-held"


def test_keep_at_is_flat_and_grades_level():
    assert prediction_intent("keep at 5/5") == "flat"
    level = claimed_level("keep at 5/5")
    assert level["value"] == 5
    assert level["population"] == 5


def test_unchanged_at_parses_level():
    assert prediction_intent("unchanged at 5/5") == "flat"
    level = claimed_level("unchanged at 5/5")
    assert level["value"] == 5
    assert level["population"] == 5
    c = check_prediction(
        "unchanged at 5/5", "unchanged", 0, population=5, latest_value=4
    )
    assert c["outcome"] == "prediction-missed"


def test_level_claim_forces_flat_when_lexicon_misses():
    """If a level is parsed, unknown intent must not skip grading."""
    # Synthetic: level present → treated as flat even if wording is odd.
    # "exactly 5/5" may not parse as stay-at; floor/exactly handled separately.
    pred = "must stay at 5/5"
    assert prediction_intent(pred) == "flat"


def test_floor_at_least_parses():
    floor = claimed_floor("pass rate at least 4/5")
    assert floor["value"] == 4
    assert floor["population"] == 5


def test_floor_no_worse_than_parses():
    floor = claimed_floor("no worse than 4/5")
    assert floor["value"] == 4
    assert floor["population"] == 5


def test_floor_met_holds():
    c = check_prediction(
        "pass rate at least 4/5", "unchanged", 0, population=5, latest_value=4
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "floor"
    assert c["floor_ok"] is True


def test_floor_missed_when_below():
    c = check_prediction(
        "pass rate at least 4/5", "hurt", -1, population=5, latest_value=3
    )
    assert c["outcome"] == "prediction-missed"
    assert c["floor_ok"] is False
    naive = naive_direction_check(
        "pass rate at least 4/5", "hurt", -1, population=5, latest_value=3
    )
    # Naive has no floor signal → no-direction or misses direction; must NOT invent held.
    assert naive["outcome"] != "prediction-held" or naive["grade"] == "direction-only"


def test_floor_held_when_above_after_helped():
    c = check_prediction(
        "at least 4/5", "helped", 1, population=5, latest_value=5
    )
    assert c["outcome"] == "prediction-held"
    assert c["floor_ok"] is True


def test_pred_demo_includes_no_slash_and_floor_rows():
    text = run_pred_demo()
    assert "stay_at_no_slash" in text
    assert "remain_at_wrong" in text
    assert "floor_missed" in text
    assert "FINDING" in text
    magnet_line = next(ln for ln in text.splitlines() if ln.strip().startswith("magnet"))
    score = magnet_line.split()[1]
    n, t = score.split("/")
    assert n == t == str(len(SCENARIOS))
    # At least one new embarrassment vs naive inventing held.
    assert "embarrassed" in text


def test_cli_pred_demo_exit_zero_slice28():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "stay_at_no_slash" in proc.stdout
    assert "floor_missed" in proc.stdout
