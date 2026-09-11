"""Slice 18 — prediction outcome check (held / missed / unmeasured)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.prediction import check_prediction, prediction_intent

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "fixtures" / "candidates"


def test_prediction_intent_rise_fall_flat():
    assert prediction_intent("pass rate rises by 1/5") == "rise"
    assert prediction_intent("coverage rises — debug gap fills") == "rise"
    assert prediction_intent("all tests still pass") == "unknown"
    assert prediction_intent("no coverage change expected") == "flat"
    assert prediction_intent("security must NOT rise on a claimed-only tag") == "flat"
    assert prediction_intent("pass rate drops") == "fall"
    assert prediction_intent("simplify skill frontmatter") == "fall"
    assert prediction_intent("relax permissions.deny for developer velocity") == "fall"
    assert prediction_intent("remove noisy PreToolUse blocker hooks") == "fall"
    assert prediction_intent("streamline allowed-tools declarations") == "fall"


def test_prediction_stems_match_real_english():
    """Slice 25 — broken stems found by running adopt with 'improves'."""
    assert prediction_intent("pass rate improves") == "rise"
    assert prediction_intent("coverage increases") == "rise"
    assert prediction_intent("coverage decreases") == "fall"
    assert prediction_intent("improve PreToolUse hooks") == "rise"
    assert prediction_intent("scores decreased after strip") == "fall"


def test_prediction_phrasal_up_does_not_invent_rise():
    """Bare \\bup\\b used to invent rise on clean up / set up."""
    assert prediction_intent("clean up frontmatter") == "unknown"
    assert prediction_intent("set up hooks") == "unknown"
    assert prediction_intent("speed up the agent") == "unknown"


def test_prediction_held_on_hurt_for_strip_title():
    c = check_prediction("simplify skill frontmatter (drop effort: fields)", "hurt", -1)
    assert c["outcome"] == "prediction-held"
    assert c["intent"] == "fall"


def test_prediction_held_on_helped():
    c = check_prediction("coverage rises", "helped", 1)
    assert c["outcome"] == "prediction-held"
    assert c["intent"] == "rise"
    assert "not attribution" in c["note"]



def test_prediction_missed_when_noise_unchanged():
    c = check_prediction("coverage rises", "unchanged", 0)
    assert c["outcome"] == "prediction-missed"


def test_prediction_flat_held_on_unchanged():
    c = check_prediction("no coverage change expected", "unchanged", 0)
    assert c["outcome"] == "prediction-held"
    assert c["intent"] == "flat"


def test_prediction_unmeasured_on_baseline():
    c = check_prediction("coverage rises", "baseline", None)
    assert c["outcome"] == "unmeasured"


def test_adopt_prints_prediction_held_with_demo_bonus(tmp_path):
    out = run_adopt(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    assert "MAGNET prediction check" in out
    assert "prediction-held" in out


def test_adopt_improves_is_prediction_held_not_no_direction(tmp_path):
    """Pre-fix: 'improves' → no-direction while verdict=helped."""
    out = run_adopt(
        "skill",
        "improves-stem-skill",
        "pass rate improves by 1/5",
        "demo-pass-rate",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    assert "prediction-held" in out
    assert "intent     rise" in out
    assert "no-direction" not in out


def test_adopt_prints_prediction_missed_on_noise_install(tmp_path):
    wine = CANDIDATES / "wine-pairing"
    out = run_adopt(
        "skill",
        "wine-pairing",
        "coverage rises",
        "stack-coverage",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        simulate_next_week=True,
        install_from=str(wine),
        fit_description="Suggest a wine to pair with dinner",
    )
    assert "prediction-missed" in out
    assert "unchanged" in out


def test_adopt_prints_prediction_held_on_gap_install(tmp_path):
    pdb = CANDIDATES / "pdb-navigator"
    out = run_adopt(
        "skill",
        "pdb-navigator",
        "coverage rises",
        "stack-coverage",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        simulate_next_week=True,
        install_from=str(pdb),
        fit_description="Debug a failing test by driving pdb and bisecting the stack trace",
    )
    assert "prediction-held" in out
    assert "helped" in out


def test_history_shows_prediction_outcome(tmp_path):
    log = str(tmp_path / "log.db")
    run_adopt(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "history"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "outcome" in proc.stdout
    assert "prediction-held" in proc.stdout
