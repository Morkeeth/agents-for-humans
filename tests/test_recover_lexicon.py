"""Slice 32 — recover/restore are rise so one-workflow predictions grade.

Found 2026-09-14 by running the Devpost object:
  prediction_intent("pass rate recovers by 1") → unknown
  adopt … 'pass rate recovers by 1' → no-direction while Δ +1

DEMO-ONE-WORKFLOW.md still says recovers; Slice 31 sidecar rewrote to rises.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.prediction import check_prediction, claimed_magnitude, prediction_intent
from magnet.pred_demo import SCENARIOS, run_pred_demo

ROOT = Path(__file__).resolve().parents[1]


def test_recover_and_restore_are_rise():
    assert prediction_intent("pass rate recovers by 1") == "rise"
    assert prediction_intent("pass rate recovers by 1/5") == "rise"
    assert prediction_intent("coverage recovers") == "rise"
    assert prediction_intent("coverage restores by 1") == "rise"
    assert prediction_intent("coverage regains") == "rise"
    assert prediction_intent("pass rate rebounds") == "rise"


def test_recover_by_1_holds_on_matching_delta():
    """THE DEFECT: amount parsed, intent unknown → no-direction while helped."""
    pred = "pass rate recovers by 1"
    claim = claimed_magnitude(pred)
    assert claim["amount"] == 1
    c = check_prediction(pred, "helped", 1, population=244, latest_value=244)
    assert c["intent"] == "rise"
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction+magnitude"


def test_recover_wrong_magnitude_misses():
    c = check_prediction(
        "pass rate recovers by 2",
        "helped",
        1,
        population=244,
        latest_value=244,
    )
    assert c["intent"] == "rise"
    assert c["outcome"] == "prediction-missed"


def test_pred_demo_includes_recover_rows():
    names = {s.name for s in SCENARIOS}
    assert "recover_held" in names
    assert "recover_wrong_mag" in names
    assert "restore_held" in names
    text = run_pred_demo()
    assert "magnet" in text
    # magnet must score every scenario including recover rows
    import re

    m = re.search(r"magnet\s+(\d+)/(\d+)", text)
    assert m is not None
    assert m.group(1) == m.group(2) == str(len(SCENARIOS))


def test_adopt_recover_prediction_grades(tmp_path):
    log = tmp_path / "log.db"
    out = run_adopt(
        "skill",
        "recover-lexicon",
        "pass rate recovers by 1",
        "demo-pass-rate",
        log_path=str(log),
        apply_demo_bonus=True,
        reset=True,
    )
    assert "prediction-held" in out or "intent     rise" in out
    assert "no-direction" not in out


def test_cli_one_workflow_script_exists():
    script = ROOT / "scripts" / "one-workflow.sh"
    assert script.is_file()
    assert "recovers by 1" in script.read_text(encoding="utf-8")


def test_cli_pred_demo_exit_zero_slice32():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "recover" in proc.stdout.lower() or "FINDING" in proc.stdout
