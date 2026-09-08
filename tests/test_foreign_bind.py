"""Slice 21 — foreign-bind embarrassment arm (offline fixtures)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.foreign_bind import measure_bind, run_foreign_bind

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"
GRINDER = ROOT / "fixtures" / "real-stacks" / "agentgrinder"


def test_fixture_hardening_near_zero():
    row = measure_bind(str(FIXTURE))
    assert row["probes"]["effort-coverage"]["value"] == 0
    assert row["probes"]["tools-coverage"]["value"] == 0
    assert row["probes"]["deny-coverage"]["value"] == 0
    assert row["naive"]["verdict"] == "complete"


def test_grinder_fixture_hardening_near_zero():
    row = measure_bind(str(GRINDER))
    assert row["probes"]["effort-coverage"]["value"] == 0
    assert row["probes"]["stack-coverage"]["value"] == 1
    assert row["naive"]["verdict"] == "complete"


def test_foreign_bind_offline_finds_naive_lie():
    text = run_foreign_bind(repo_root=str(ROOT))
    assert "FINDING" in text
    assert "naive_title=complete" in text
    assert "effort" in text
    assert str(FIXTURE) in text or "fixtures/stack" in text


def test_cli_foreign_bind_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "foreign-bind"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FINDING" in proc.stdout


def test_cli_foreign_bind_stack_arg():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "foreign-bind", "--stack", str(GRINDER)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "agentgrinder" in proc.stdout
    assert "FINDING" in proc.stdout
