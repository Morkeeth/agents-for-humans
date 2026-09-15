"""Slice 35 — negation + ceiling + target-level prediction honesty.

Found 2026-09-15 by running the prediction object:
  prediction_intent("won't fall") → fall
  check_prediction("won't fall", "hurt", -1, …) → prediction-held
  check_prediction("won't fall", "unchanged", 0, …) → prediction-missed
That invents that "won't fall" means fall.

Also:
  claimed_ceiling("at most 3/5") → None  (floor dual missing)
  falls to 2/5 + latest 3 → prediction-held on direction alone
  coverage improves by 1 → no-direction (improv stem word-boundary)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_ceiling,
    claimed_target,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_wont_fall_is_flat_not_fall():
    """THE LIE: won't fall graded as fall → invents held when score drops."""
    assert prediction_intent("won't fall") == "flat"
    assert prediction_intent("pass rate won't fall") == "flat"
    assert prediction_intent("will not fall") == "flat"
    assert prediction_intent("does not regress") == "flat"
    assert prediction_intent("should not drop") == "flat"
    assert prediction_intent("coverage doesn't fall") == "flat"


def test_wont_fall_unchanged_holds():
    c = check_prediction(
        "pass rate won't fall", "unchanged", 0, population=5, latest_value=4
    )
    assert c["outcome"] == "prediction-held"
    assert c["intent"] == "flat"


def test_wont_fall_hurt_misses_the_lie():
    """When the score falls, 'won't fall' must miss — old magnet held."""
    pred = "pass rate won't fall"
    magnet = check_prediction(
        pred, "hurt", -1, population=5, latest_value=3
    )
    naive = naive_direction_check(
        pred, "hurt", -1, population=5, latest_value=3
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["intent"] == "flat"
    # Naive direction-only also uses fixed intent (flat), so also misses.
    # The embarrassment arm for negation is the *old* fall lie — documented
    # in pred-demo note; ceiling/target still embarrass via direction-only.
    assert naive["intent"] == "flat"
    assert naive["outcome"] == "prediction-missed"


def test_must_not_rise_still_flat():
    assert prediction_intent("must NOT rise") == "flat"
    assert prediction_intent("coverage will not rise") == "flat"


def test_claimed_ceiling_parses():
    for text in (
        "at most 3/5",
        "no better than 3/5",
        "no more than 4/5",
        "capped at 4/5",
        "must not exceed 4/5",
    ):
        c = claimed_ceiling(text)
        assert c["value"] is not None, text
        assert c["raw"] is not None


def test_ceiling_holds_when_latest_at_or_below():
    c = check_prediction(
        "pass rate at most 3/5", "unchanged", 0, population=5, latest_value=3
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "ceiling"
    assert c["ceiling_ok"] is True


def test_ceiling_misses_when_latest_above():
    pred = "pass rate at most 3/5"
    magnet = check_prediction(
        pred, "unchanged", 0, population=5, latest_value=4
    )
    naive = naive_direction_check(
        pred, "unchanged", 0, population=5, latest_value=4
    )
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["ceiling_ok"] is False
    assert naive["outcome"] == "prediction-held"  # direction flat invents held


def test_falls_to_target_holds():
    c = check_prediction(
        "pass rate falls to 2/5", "hurt", -2, population=5, latest_value=2
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+target"
    assert c["target_ok"] is True


def test_falls_to_target_misses_wrong_latest():
    """THE LIE: direction fall alone invented held while latest ≠ 2."""
    pred = "pass rate falls to 2/5"
    magnet = check_prediction(
        pred, "hurt", -1, population=5, latest_value=3
    )
    naive = naive_direction_check(
        pred, "hurt", -1, population=5, latest_value=3
    )
    assert claimed_target(pred)["value"] == 2
    assert claimed_target(pred)["population"] == 5
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["target_ok"] is False
    assert naive["outcome"] == "prediction-held"


def test_reaches_grades_target_without_rise_word():
    assert prediction_intent("pass rate reaches 5/5") == "flat"
    held = check_prediction(
        "pass rate reaches 5/5", "unchanged", 0, population=5, latest_value=5
    )
    missed = check_prediction(
        "pass rate reaches 5/5", "unchanged", 0, population=5, latest_value=4
    )
    assert held["outcome"] == "prediction-held"
    assert held["grade"] == "target"
    assert missed["outcome"] == "prediction-missed"


def test_improves_is_rise_not_unknown():
    """improv stem failed word-boundary on 'improves' — was no-direction."""
    assert prediction_intent("coverage improves by 1") == "rise"
    c = check_prediction(
        "coverage improves by 1", "helped", 1, population=12, latest_value=9
    )
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+magnitude"


def test_climbs_and_declines_lexicon():
    assert prediction_intent("pass rate climbs by 1") == "rise"
    assert prediction_intent("pass rate declines by 1") == "fall"


def test_pred_demo_includes_slice35_scenarios_and_embarrasses():
    names = {s.name for s in SCENARIOS}
    for required in (
        "wont_fall_holds",
        "wont_fall_missed",
        "ceiling_holds",
        "ceiling_missed",
        "falls_to_holds",
        "falls_to_missed",
        "reaches_holds",
        "reaches_missed",
        "improves_held",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    assert "won't fall" in out or "Negation" in out or "negation" in out.lower()
    # magnet must score all scenarios
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out
    assert "embarrassed" in out


def test_pred_demo_cli_exit_0():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
