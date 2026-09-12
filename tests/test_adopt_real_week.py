"""Slice 29 — adopt default is a real week, not a fabricated SIMULATED stamp.

Found 2026-09-12 by running:
  magnet adopt skill x 'pass rate rises by 1/5' --probe demo-pass-rate --demo-bonus --reset
  → reading … (SIMULATED week)
  → simulated  2026-09-20T…  (SIMULATED week — not a real read time)

Same-day readings already survive (Slice bugs #2). The default fabricated a
week for no reason. Real week is now default; --simulate is the demo opt-in.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt

ROOT = Path(__file__).resolve().parents[1]


def test_run_adopt_default_has_no_simulated(tmp_path):
    out = run_adopt(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply_demo_bonus=True,
    )
    assert "SIMULATED" not in out, out
    assert "verdict    helped" in out
    assert "prediction-held" in out


def test_run_adopt_simulate_opt_in_still_labels(tmp_path):
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
    assert "SIMULATED" in out
    assert "verdict    helped" in out


def test_cli_bare_adopt_prints_no_simulated(tmp_path):
    log = tmp_path / "cli.db"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "--log",
            str(log),
            "adopt",
            "skill",
            "x",
            "pass rate rises by 1/5",
            "--probe",
            "demo-pass-rate",
            "--demo-bonus",
            "--reset",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SIMULATED" not in proc.stdout, proc.stdout
    assert "helped" in proc.stdout


def test_cli_simulate_flag_labels_simulated(tmp_path):
    log = tmp_path / "sim.db"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "--log",
            str(log),
            "adopt",
            "skill",
            "x",
            "pass rate rises by 1/5",
            "--probe",
            "demo-pass-rate",
            "--demo-bonus",
            "--reset",
            "--simulate",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SIMULATED" in proc.stdout


def test_cli_no_simulate_alias_still_real_week(tmp_path):
    """Old docs pass --no-simulate; must remain a real week (and stay green)."""
    log = tmp_path / "alias.db"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "--log",
            str(log),
            "adopt",
            "skill",
            "x",
            "pass rate rises by 1/5",
            "--probe",
            "demo-pass-rate",
            "--demo-bonus",
            "--reset",
            "--no-simulate",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SIMULATED" not in proc.stdout
