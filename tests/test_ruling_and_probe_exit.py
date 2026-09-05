"""Slice 16 — ruling honesty + pytest-miss exits non-zero."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from magnet.probes import check_docs, run_pytest_probe

ROOT = Path(__file__).resolve().parents[1]


def test_readme_does_not_name_grinder_as_the_entry():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "the Agents for Humans entry" not in readme
    assert "not itself the submission" not in readme


def test_readme_and_night_scope_agree_magnet_submits():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    night = (ROOT / "_NIGHT-SCOPE.md").read_text(encoding="utf-8")
    assert "MAGNET submits" in night
    assert "Sep 14" in readme
    # Companion product language is fine; naming Grinder as the entry is not.
    assert "Agent Grinder" in readme
    assert "companion" in readme.lower() or "separate product" in readme.lower()


def test_check_docs_catches_grinder_as_entry_claim(tmp_path):
    """Control must go RED: plant the old README lie and watch check_docs fail."""
    (tmp_path / "README.md").write_text(
        "# MAGNET\n\n"
        "MAGNET is the engine library for Agent Grinder, the Agents for Humans entry; "
        "this repo is not itself the submission.\n"
        "Strands agent · 4 tools\n"
        "run_probe record_week adopt_change check_docs\n",
        encoding="utf-8",
    )
    (tmp_path / "hack.md").write_text(
        "ruling: MAGNET submits Sep 14\nEYES: MAGNET submits, Grinder product\n",
        encoding="utf-8",
    )
    (tmp_path / "_NIGHT-SCOPE.md").write_text(
        "**EYES ruling:** MAGNET submits. Agent Grinder is a separate product.\n",
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()
    results = check_docs(str(tmp_path))
    ruling = [r for r in results if r["claim"] == "sep14 entry ruling"]
    assert ruling, results
    assert ruling[0]["ok"] is False


def test_check_docs_passes_ruling_on_this_repo():
    results = check_docs(str(ROOT))
    ruling = [r for r in results if r["claim"] == "sep14 entry ruling"]
    assert ruling and ruling[0]["ok"] is True, ruling


def test_pytest_probe_unmeasured_when_command_dies():
    reading = run_pytest_probe(
        command=f"{sys.executable} -c \"raise SystemExit('no pytest')\"",
        scoped=True,
    )
    assert reading["value"] is None
    assert reading["population"] is None
    assert reading["detail"]["exit_code"] != 0


def test_cli_probe_exits_nonzero_when_unmeasured(monkeypatch):
    """The DEVPOST-DESCRIPTION defect: dead probe must not exit 0."""
    from magnet import cli as magnet_cli

    monkeypatch.setattr(
        "magnet.cli.tool_run_probe",
        lambda name, **kw: {
            "probe_name": name,
            "value": None,
            "population": None,
            "command": "dead",
        },
    )
    args = argparse.Namespace(name="pytest-pass-rate", log=None, repo=".", stack=None)
    assert magnet_cli.cmd_probe(args) == 1


def test_cli_registry_dead_probe_exits_nonzero(tmp_path):
    magnet_dir = tmp_path / ".magnet"
    magnet_dir.mkdir()
    (magnet_dir / "probes.json").write_text(
        '{"probes": {"dead-eval": {"command": "false", "parser": "pytest_summary",'
        ' "direction": "up"}}}',
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "probe", "dead-eval"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "None" in proc.stdout or "unmeasured" in proc.stdout.lower()
