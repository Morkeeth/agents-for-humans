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


def test_prompt_consistency_claude_md_present_without_must_lines(tmp_path):
    """Live superpowers CLAUDE.md exists with inline MUST but zero ^MUST: lines."""
    from magnet.stack_bind import prompt_consistency

    (tmp_path / "CLAUDE.md").write_text(
        "# Guidelines\nBefore you act you MUST read this.\n",
        encoding="utf-8",
    )
    reading = prompt_consistency(str(tmp_path))
    assert reading["detail"]["claude_md_present"] is True
    assert reading["detail"]["claude_present"] is True  # alias of file presence
    assert reading["detail"]["must_line_count"] == 0
    assert reading["population"] == 0


def test_foreign_bind_finding_when_claude_md_lacks_ug_must_lines(tmp_path):
    from magnet.foreign_bind import measure_bind, render_foreign_bind

    (tmp_path / "CLAUDE.md").write_text(
        "# Not UG format\nContributors MUST identify themselves.\n",
        encoding="utf-8",
    )
    (tmp_path / "skills").mkdir()
    measured = measure_bind(str(tmp_path))
    text = render_foreign_bind(
        [
            {
                "stack": str(tmp_path),
                "label": "tmp",
                "probes": measured["probes"],
                "naive": measured["naive"],
            }
        ]
    )
    assert "CLAUDE.md present · 0 UG MUST: lines" in text
    assert "object missing" not in text.split("prompt-consistency")[1].split("\n")[0]
    assert "FINDING  CLAUDE.md present with 0 UG MUST: lines" in text
