"""Slice 59 — same-as invent-held + is/reads/matches targets.

Found by running objects after S58:
  same as 4/5 → intent=flat target=None → prediction-held @latest=3  # THE LIE
  is 4/5 / was 4/5 / reads 4/5 / measures 4/5 → target=None
  matches 4/5 / identical to 4/5 / lands on 4/5 → target=None
  finishes at 4/5 / comes to 4/5 / settles on 4/5 → target=None
  eleventh to twelfth → target=None while 11th to 12th grades
  Contrast: equals 4/5 / exactly 4/5 / lands at 4/5 already grade.
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


def test_same_as_is_target_not_bare_flat():
    """THE LIE: same as 4/5 was flat with no target → invents held @3."""
    tgt = claimed_target("same as 4/5")
    assert tgt["value"] == 4
    assert tgt["population"] == 5
    assert prediction_intent("same as 4/5") == "flat"
    held = check_prediction(
        "same as 4/5", "unchanged", 0, population=5, latest_value=4
    )
    missed = check_prediction(
        "same as 4/5", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "same as 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert held["outcome"] == "prediction-held"
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_same_as_word_and_identical():
    assert claimed_target("same as four")["value"] == 4
    assert claimed_target("identical to 4/5")["value"] == 4
    missed = check_prediction(
        "identical to 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"


def test_is_was_are_targets():
    for text in ("is 4/5", "was 4/5", "are 4/5", "is 4", "is four"):
        assert claimed_target(text)["value"] == 4, text
        assert prediction_intent(text) == "flat", text
    missed = check_prediction(
        "is 4/5", "unchanged", 0, population=5, latest_value=3
    )
    naive = naive_direction_check(
        "is 4/5", "unchanged", 0, population=5, latest_value=3
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_reads_measures_matches():
    for text in (
        "reads 4/5",
        "reads as 4/5",
        "reads four",
        "measures 4/5",
        "measures at 4/5",
        "matches 4/5",
        "matches four",
    ):
        assert claimed_target(text)["value"] == 4, text
    missed = check_prediction(
        "reads 4/5", "unchanged", 0, population=5, latest_value=2
    )
    assert missed["outcome"] == "prediction-missed"


def test_lands_on_finishes_comes_settles():
    for text in (
        "lands on 4/5",
        "settles on 4/5",
        "finishes at 4/5",
        "finish at 4",
        "comes to 4/5",
        "comes out to 4/5",
        "stands at 4/5",
        "sits at 4/5",
        "clocks in at 4/5",
    ):
        assert claimed_target(text)["value"] == 4, text


def test_eleventh_to_twelfth():
    tgt = claimed_target("eleventh to twelfth")
    assert tgt["value"] == 12
    assert claimed_target("from eleventh to twelfth")["value"] == 12
    assert claimed_target("eleven to twelve")["value"] == 12
    # digit ordinal regression
    assert claimed_target("11th to 12th")["value"] == 12
    missed = check_prediction(
        "eleventh to twelfth", "unchanged", 0, population=20, latest_value=11
    )
    naive = naive_direction_check(
        "eleventh to twelfth", "unchanged", 0, population=20, latest_value=11
    )
    assert missed["outcome"] == "prediction-missed"
    assert naive["outcome"] == "prediction-held"


def test_bare_same_still_no_target():
    """Bare 'same' stays flat without inventing a level."""
    assert claimed_target("same")["value"] is None
    assert prediction_intent("same") == "flat"


def test_equals_regression():
    assert claimed_target("equals 4/5")["value"] == 4
    assert claimed_target("holds at 4/5")["value"] is None  # stay-at owns level


def test_pred_demo_includes_slice59():
    names = {s.name for s in SCENARIOS}
    for required in (
        "same_as_missed",
        "is_slash_missed",
        "reads_missed",
        "matches_missed",
        "lands_on_missed",
        "eleventh_to_twelfth_missed",
        "same_as_word_missed",
    ):
        assert required in names, required
    out = run_pred_demo()
    assert "FINDING" in out
    total = len(SCENARIOS)
    assert f"magnet       {total}/{total}" in out


def test_pred_demo_cli_exit_0_slice59():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "FINDING" in proc.stdout
