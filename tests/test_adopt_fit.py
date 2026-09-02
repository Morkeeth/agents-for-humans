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
