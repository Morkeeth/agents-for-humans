"""Slice 15 — stack-bind probes + bind-demo embarrassment arm."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.bind_demo import run_bind_demo
from magnet.probes import run_deny_coverage_probe, run_effort_coverage_probe
from magnet.stack_bind import (
    SENSITIVE_DENY_PATTERNS,
    apply_deny_patterns,
    apply_effort_frontmatter,
    copy_stack,
    deny_coverage,
    effort_coverage,
    skill_has_effort,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"


def test_fixture_effort_starts_at_zero():
    reading = effort_coverage(str(FIXTURE))
    assert reading["probe_name"] == "effort-coverage"
    assert reading["population"] == 7  # re-derived from fixtures/stack/skills
    assert reading["value"] == 0
    assert len(reading["detail"]["missing_effort"]) == 7


def test_fixture_deny_starts_below_full():
    reading = deny_coverage(str(FIXTURE))
    assert reading["probe_name"] == "deny-coverage"
    assert reading["population"] == len(SENSITIVE_DENY_PATTERNS)
    assert reading["value"] < reading["population"]


def test_apply_effort_then_probe_moves(tmp_path):
    stack = copy_stack(str(FIXTURE), str(tmp_path / "stack"))
    before = effort_coverage(stack)
    touched = apply_effort_frontmatter(stack)
    after = effort_coverage(stack)
    assert len(touched) == before["population"]
    assert after["value"] == after["population"]
    assert after["value"] > before["value"]
    # Open the object — every SKILL.md now carries effort:
    skills = Path(stack) / "skills"
    for child in skills.iterdir():
        assert skill_has_effort(child / "SKILL.md")


def test_apply_deny_then_probe_moves(tmp_path):
    stack = copy_stack(str(FIXTURE), str(tmp_path / "stack"))
    before = deny_coverage(stack)
    added = apply_deny_patterns(stack)
    after = deny_coverage(stack)
    assert added  # fixture was missing patterns
    assert after["value"] == after["population"]
    assert after["value"] > before["value"]
    # Open settings.json itself
    settings = json.loads((Path(stack) / "settings.json").read_text())
    blob = json.dumps(settings)
    for pattern in SENSITIVE_DENY_PATTERNS:
        assert pattern in blob


def test_bind_demo_embarrasses_repo_blind():
    text = run_bind_demo(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    assert "repo-blind check-docs stayed flat while stack-bind probes moved" in text
    assert "effort-coverage" in text
    assert "deny-coverage" in text
    assert "naive (title only)" in text
    assert "helped" in text
    # Source fixture must be untouched
    assert effort_coverage(str(FIXTURE))["value"] == 0


def test_cli_bind_demo_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "bind-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FINDING" in proc.stdout


def test_cli_probe_effort_and_deny():
    for name in ("effort-coverage", "deny-coverage"):
        proc = subprocess.run(
            [sys.executable, "-m", "magnet.cli", "probe", name],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert name in proc.stdout


def test_adopt_hook_with_deny_probe_measures_stack(tmp_path):
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "hook",
        "permissions.deny for secrets",
        "deny-coverage rises",
        "deny-coverage",
        log_path=log,
        reset=True,
        simulate_next_week=False,
        stack_dir=str(FIXTURE),
    )
    assert "measures   stack" in out
    assert "measures   repo only" not in out


def test_adopt_hook_with_demo_probe_still_warns(tmp_path):
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "hook",
        "permissions.deny for secrets",
        "no change expected",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        simulate_next_week=False,
    )
    assert "measures   repo only" in out


def test_run_effort_probe_helper():
    reading = run_effort_coverage_probe(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    assert reading["value"] == 0
    assert reading["population"] == 7


def test_run_deny_probe_helper():
    reading = run_deny_coverage_probe(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    assert reading["population"] == 4
