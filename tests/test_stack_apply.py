"""Slice 15 — adopt --apply moves stack-coverage; claimed tags never buy coverage."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.apply import apply_skill, copy_stack, remove_skill, skill_dir
from magnet.probes import run_stack_coverage_probe
from magnet.stack import CAPABILITIES, gaps, inventory, stack_coverage
from magnet.stack_demo import run_stack_demo

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"


def test_apply_skill_raises_coverage_on_debug_gap(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    before = stack_coverage(str(work))
    assert "debug" in before["detail"]["uncovered"]
    apply_skill(
        str(work),
        "pdb-navigator",
        "Debug a failing test by driving pdb and bisecting the stack trace",
    )
    after = stack_coverage(str(work))
    assert after["value"] == before["value"] + 1
    assert "debug" not in after["detail"]["uncovered"]
    assert "debug" in after["detail"]["covered_caps"]


def test_apply_noise_does_not_raise_coverage(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    before = stack_coverage(str(work))
    apply_skill(str(work), "wine-pairing", "Suggest a wine to pair with dinner")
    after = stack_coverage(str(work))
    assert after["value"] == before["value"]
    assert after["detail"]["uncovered"] == before["detail"]["uncovered"]


def test_claimed_capability_does_not_buy_coverage(tmp_path):
    """capabilities: [security] + flashcard text → claimed, coverage unchanged."""
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    before = stack_coverage(str(work))
    assert "security" in before["detail"]["uncovered"]
    apply_skill(
        str(work),
        "flashcard-guard",
        "Practise flashcards with spaced repetition",
        capabilities=["security"],
    )
    after = stack_coverage(str(work))
    assert after["value"] == before["value"]
    assert "security" in after["detail"]["uncovered"]
    assert "security" in after["detail"]["claimed_only"]


def test_verified_capability_counts_toward_coverage(tmp_path):
    """capabilities: [refactor] + extract/rename text → verified → covered."""
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    before = stack_coverage(str(work))
    assert "refactor" in before["detail"]["uncovered"]
    apply_skill(
        str(work),
        "code-surgeon",
        "Extract a method and rename identifiers until the module is simpler",
        capabilities=["refactor"],
    )
    after = stack_coverage(str(work))
    assert after["value"] == before["value"] + 1
    assert "refactor" not in after["detail"]["uncovered"]
    assert "refactor" in after["detail"]["verified_caps"] or "refactor" in after[
        "detail"
    ]["covered_caps"]


def test_adopt_apply_prints_helped_on_filler(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "pdb-navigator",
        "coverage rises",
        "stack-coverage",
        log_path=log,
        reset=True,
        apply=True,
        simulate_next_week=True,
        stack_dir=str(work),
        fit=True,
        fit_description="Debug a failing test by driving pdb and bisecting the stack trace",
    )
    assert "applied" in out.lower() or "SKILL.md" in out
    assert "helped" in out
    assert "fills-gap" in out or "fills" in out.lower()
    assert "NOTE: fit predicted" not in out


def test_adopt_without_apply_warns_when_fit_fills_but_coverage_unchanged(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "pdb-navigator",
        "coverage rises",
        "stack-coverage",
        log_path=log,
        reset=True,
        apply=False,
        simulate_next_week=True,
        stack_dir=str(work),
        fit=True,
        fit_description="Debug a failing test by driving pdb and bisecting the stack trace",
    )
    assert "fills-gap" in out
    assert "unchanged" in out or "baseline" in out
    assert "--apply" in out
    assert "fit predicted fills-gap" in out


def test_adopt_apply_noise_stays_unchanged(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "wine-pairing",
        "no change",
        "stack-coverage",
        log_path=log,
        reset=True,
        apply=True,
        simulate_next_week=True,
        stack_dir=str(work),
        fit=True,
        fit_description="Suggest a wine to pair with dinner",
    )
    assert "unchanged" in out
    assert "no-signal" in out


def test_stack_demo_embarrasses_naive(tmp_path):
    out = run_stack_demo(
        repo_root=str(ROOT),
        log_path=str(tmp_path / "demo.db"),
        work_dir=str(tmp_path / "work"),
    )
    assert "wine-pairing" in out
    assert "magnet     unchanged" in out or "magnet     unchanged" in out.lower()
    # Naive invents helped on the noise arm
    assert "naive      helped" in out
    assert "FINDING" in out
    assert "claimed" in out.lower()
    # Must not mutate committed fixtures
    fixture_cov = run_stack_coverage_probe(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    assert fixture_cov["value"] == len(CAPABILITIES) - len(
        gaps(inventory(str(FIXTURE)))["uncovered"]
    )


def test_cli_stack_demo_exit_0():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "stack-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "MAGNET stack-demo" in proc.stdout
    assert "wine-pairing" in proc.stdout
    assert "naive      helped" in proc.stdout
    # Cleanup work dir so the suite does not leave skills in fixtures
    work = ROOT / ".magnet" / "stack-demo-work"
    if work.exists():
        shutil.rmtree(work)


def test_remove_skill_restores_coverage(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    before = stack_coverage(str(work))["value"]
    apply_skill(
        str(work),
        "pdb-navigator",
        "Debug a failing test by driving pdb and bisecting the stack trace",
    )
    assert stack_coverage(str(work))["value"] == before + 1
    remove_skill(str(work), "pdb-navigator")
    assert not skill_dir(str(work), "pdb-navigator").exists()
    assert stack_coverage(str(work))["value"] == before


def test_inventory_parses_capabilities_frontmatter(tmp_path):
    work = tmp_path / "stack"
    copy_stack(str(FIXTURE), str(work))
    apply_skill(
        str(work),
        "code-surgeon",
        "Extract a method and rename identifiers",
        capabilities=["refactor"],
    )
    inv = inventory(str(work))
    row = next(s for s in inv["skills"] if s["name"] == "code-surgeon")
    assert row["capabilities"] == ["refactor"]
    assert row["capability_verdicts"]["refactor"] == "verified"


def test_document_extracting_does_not_cover_refactor():
    """Found opening anthropics/skills: docx description says 'extracting
    content from .docx' and bare term 'extract' matched via startswith —
    falsely covering refactor. Term is now 'extract method'."""
    from magnet.stack import CAPABILITIES, _mentions

    docx_blob = (
        "docx Use this skill whenever the user wants to create, read, edit, "
        "or manipulate Word documents. Also use when extracting or "
        "reorganizing content from .docx files."
    )
    assert not _mentions(docx_blob, CAPABILITIES["refactor"])
    assert _mentions(
        "Extract a method and rename identifiers until simpler",
        CAPABILITIES["refactor"],
    )
