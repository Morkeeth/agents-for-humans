"""Slice 16 — prediction outcome check + foreign-stack honesty."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.apply import copy_stack
from magnet.prediction import check_prediction, prediction_intent

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"


def test_prediction_intent_rise_fall_flat():
    assert prediction_intent("pass rate rises by 1/5") == "rise"
    assert prediction_intent("coverage rises — debug gap fills") == "rise"
    assert prediction_intent("all tests still pass") == "unknown"  # no rise/fall/flat
    assert prediction_intent("no coverage change expected") == "flat"
    assert prediction_intent("security must NOT rise on a claimed-only tag") == "flat"
    assert prediction_intent("pass rate drops") == "fall"


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


def test_adopt_prints_prediction_check_held(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    out = run_adopt(
        "skill",
        "pdb-navigator",
        "coverage rises",
        "stack-coverage",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply=True,
        simulate_next_week=True,
        stack_dir=str(work),
        fit_description="Debug a failing test by driving pdb and bisecting the stack trace",
    )
    assert "MAGNET prediction check" in out
    assert "prediction-held" in out


def test_adopt_prints_prediction_missed_on_noise(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    out = run_adopt(
        "skill",
        "wine-pairing",
        "coverage rises",  # wrong prediction on purpose
        "stack-coverage",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply=True,
        simulate_next_week=True,
        stack_dir=str(work),
        fit_description="Suggest a wine to pair with dinner",
    )
    assert "prediction-missed" in out
    assert "unchanged" in out


def test_history_shows_prediction_outcome(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    log = str(tmp_path / "log.db")
    run_adopt(
        "skill",
        "pdb-navigator",
        "coverage rises",
        "stack-coverage",
        log_path=log,
        reset=True,
        apply=True,
        simulate_next_week=True,
        stack_dir=str(work),
        fit_description="Debug a failing test by driving pdb and bisecting the stack trace",
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
