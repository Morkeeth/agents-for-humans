"""Slice 14 — adopt --fit receipt + stack-coverage probe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.probes import run_stack_coverage_probe
from magnet.stack import CAPABILITIES, fit_one

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"


def test_fit_one_fills_debug_gap():
    fit = fit_one(
        "pdb-navigator",
        "Debug a failing test by bisecting the stack trace",
        str(FIXTURE),
    )
    assert fit["label"] == "fills-gap"
    assert "debug" in fit["fills"]
    assert fit["score"] > 0


def test_fit_one_marks_duplicate():
    fit = fit_one(
        "writing-coach-pro",
        "Writing rules for anything with a reader. Draft an email, reply, DM, "
        "LinkedIn note, connection request, cover letter, bio or post",
        str(FIXTURE),
    )
    assert fit["label"] == "duplicate"
    assert fit["score"] < 0


def test_fit_one_no_signal_on_noise():
    fit = fit_one("tarot", "read a tarot spread", str(FIXTURE))
    assert fit["label"] == "no-signal"
    assert fit["score"] == 0


def test_adopt_fit_appends_fit_block(tmp_path):
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "pdb-navigator",
        "Debug failing tests with pdb and stack traces",
        "demo-pass-rate",
        log_path=log,
        apply_demo_bonus=True,
        reset=True,
        fit=True,
        stack_dir=str(FIXTURE),
        fit_description="Debug a failing test by driving pdb and bisecting the stack trace",
    )
    assert "MAGNET fit" in out
    assert "fills-gap" in out or "fills" in out.lower()
    assert "debug" in out


def test_adopt_fit_flags_duplicate(tmp_path):
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "writing-coach-pro",
        "more writing help",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        fit=True,
        stack_dir=str(FIXTURE),
        fit_description=(
            "Writing rules for anything with a reader. Draft an email, reply, "
            "DM, LinkedIn note, connection request, cover letter, bio or post"
        ),
    )
    assert "duplicate" in out
    assert "overlaps" in out.lower() or "OVERLAPS" in out or "overlaps" in out


def test_stack_coverage_probe_rederived():
    reading = run_stack_coverage_probe(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    assert reading["probe_name"] == "stack-coverage"
    assert reading["population"] == len(CAPABILITIES)
    assert reading["value"] is not None
    assert 0 <= reading["value"] <= reading["population"]
    # Fixture covers writing, test-gate, docs, review, planning, design, verification
    assert reading["value"] >= 5
    assert "debug" in reading["detail"]["uncovered"]


def test_cli_probe_stack_coverage():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "probe", "stack-coverage"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "stack-coverage:" in proc.stdout
    assert "/" in proc.stdout


def test_demo_bonus_is_opt_in_only(tmp_path):
    """Regression: demo-pass-rate must NOT invent +1/5 unless --demo-bonus."""
    from magnet.log import connect, get_demo_bonus, list_readings, reset_demo
    from magnet.tools import tool_adopt_change, tool_record_week

    log = str(tmp_path / "log.db")
    conn = connect(log)
    reset_demo(conn)
    tool_record_week("demo-pass-rate", log_path=log)
    tool_adopt_change(
        "skill",
        "wine-pairing",
        "noise",
        "demo-pass-rate",
        log_path=log,
        apply_demo_bonus=False,
    )
    assert get_demo_bonus(connect(log)) == 0
    tool_record_week("demo-pass-rate", log_path=log, simulate_next_week=True)
    values = [r["value"] for r in list_readings(connect(log), "demo-pass-rate")]
    assert values == [3, 3], values


def test_demo_bonus_opt_in_raises_score(tmp_path):
    from magnet.log import connect, list_readings, reset_demo
    from magnet.tools import tool_adopt_change, tool_record_week

    log = str(tmp_path / "log.db")
    reset_demo(connect(log))
    tool_record_week("demo-pass-rate", log_path=log)
    tool_adopt_change(
        "skill",
        "pdb",
        "up",
        "demo-pass-rate",
        log_path=log,
        apply_demo_bonus=True,
    )
    tool_record_week("demo-pass-rate", log_path=log, simulate_next_week=True)
    values = [r["value"] for r in list_readings(connect(log), "demo-pass-rate")]
    assert values == [3, 4], values


def test_list_probes_includes_stack_coverage():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "list-probes"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "stack-coverage" in proc.stdout
    assert "total      4" in proc.stdout
