"""Slice 20 — Ultimate Guide bind probes + guide-demo."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from magnet.guide_demo import run_guide_demo
from magnet.stack_bind import (
    HOOK_SIGNALS,
    apply_allowed_tools_frontmatter,
    apply_hook_hardening,
    apply_prompt_consistency,
    copy_stack,
    hook_coverage,
    prompt_consistency,
    skill_has_allowed_tools,
    tools_coverage,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"


def test_fixture_tools_starts_at_zero():
    reading = tools_coverage(str(FIXTURE))
    assert reading["probe_name"] == "tools-coverage"
    assert reading["population"] == 7
    assert reading["value"] == 0


def test_fixture_hook_starts_below_full():
    reading = hook_coverage(str(FIXTURE))
    assert reading["probe_name"] == "hook-coverage"
    assert reading["population"] == len(HOOK_SIGNALS)
    assert reading["value"] < reading["population"]
    assert "dangerous-actions-blocker" in reading["detail"]["missing"]
    assert "no-rm-rf-star-allow" in reading["detail"]["missing"]


def test_fixture_prompt_starts_inconsistent():
    reading = prompt_consistency(str(FIXTURE))
    assert reading["probe_name"] == "prompt-consistency"
    assert reading["population"] == 3  # MUST lines in fixtures/stack/CLAUDE.md
    assert reading["value"] == 0


def test_apply_tools_then_probe_moves(tmp_path):
    stack = copy_stack(str(FIXTURE), str(tmp_path / "stack"))
    before = tools_coverage(stack)
    touched = apply_allowed_tools_frontmatter(stack)
    after = tools_coverage(stack)
    assert len(touched) == before["population"]
    assert after["value"] == after["population"]
    assert after["value"] > before["value"]
    for child in (Path(stack) / "skills").iterdir():
        assert skill_has_allowed_tools(child / "SKILL.md")


def test_apply_hook_then_probe_moves(tmp_path):
    stack = copy_stack(str(FIXTURE), str(tmp_path / "stack"))
    before = hook_coverage(stack)
    applied = apply_hook_hardening(stack)
    after = hook_coverage(stack)
    assert applied
    assert after["value"] == after["population"]
    assert after["value"] > before["value"]
    settings = json.loads((Path(stack) / "settings.json").read_text())
    allow = settings.get("permissions", {}).get("allow") or []
    assert "Bash(rm -rf *)" not in allow
    assert (Path(stack) / "hooks" / "dangerous-actions-blocker.sh").is_file()


def test_apply_prompt_then_probe_moves(tmp_path):
    stack = copy_stack(str(FIXTURE), str(tmp_path / "stack"))
    before = prompt_consistency(stack)
    applied = apply_prompt_consistency(stack)
    after = prompt_consistency(stack)
    assert len(applied) == before["population"]
    assert after["value"] == after["population"]
    assert after["value"] > before["value"]


def test_guide_demo_moves_five_and_keeps_repo_blind():
    text = run_guide_demo(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    assert "repo-blind check-docs stayed flat while" in text
    assert "Ultimate Guide stack-bind probes moved" in text
    assert "moved=5/5" in text
    assert "naive" in text.lower()
    # Source fixture must be untouched
    assert tools_coverage(str(FIXTURE))["value"] == 0
    assert hook_coverage(str(FIXTURE))["value"] == 0
    assert prompt_consistency(str(FIXTURE))["value"] == 0


def test_cli_guide_demo_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "guide-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FINDING" in proc.stdout
    assert "moved=5/5" in proc.stdout


def test_cli_probe_new_bind_probes():
    for name in ("tools-coverage", "hook-coverage", "prompt-consistency"):
        proc = subprocess.run(
            [sys.executable, "-m", "magnet.cli", "probe", name],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert name in proc.stdout


def test_check_docs_scans_screenshot_sidecars():
    """Control must watch screenshot sidecars — the 113 drift lived there."""
    from magnet.probes import check_docs

    results = check_docs(str(ROOT))
    shot_claims = [r for r in results if r["claim"].startswith("screenshot pytest")]
    assert shot_claims, "check_docs must scan docs/screenshots/*.txt"
