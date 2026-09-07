"""Tests for redact-scan (must go RED) and extract-method foreign-object fix."""
from __future__ import annotations

from pathlib import Path

from magnet.external import measure_external_stack, naive_title_verdict, render_external
from magnet.redact import run_redact_scan, scan_tree
from magnet.stack import CAPABILITIES, _mentions, inventory, stack_coverage

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"
REAL_AG = ROOT / "fixtures" / "real-stacks" / "agentgrinder"


def test_extract_method_not_bare_extract():
    """Bare 'extract' invented refactor on anthropics docx/pdf (2026-09-07)."""
    assert "extract" not in CAPABILITIES["refactor"]
    assert "extract method" in CAPABILITIES["refactor"]
    assert _mentions("extracting content from .docx", CAPABILITIES["refactor"]) is False
    assert _mentions("rename and extract method across modules", CAPABILITIES["refactor"]) is True
    # safe-rename planted prose still hits via refactor/rename/simplify
    assert _mentions(
        "Refactor across a repo: rename a symbol, extract a function, simplify nested conditionals",
        CAPABILITIES["refactor"],
    )


def test_document_extracting_does_not_cover_refactor(tmp_path):
    """Re-derive the anthropics false positive on a planted skill."""
    skills = tmp_path / "skills" / "docx"
    skills.mkdir(parents=True)
    (skills / "SKILL.md").write_text(
        "---\nname: docx\n"
        "description: extracting content from .docx files\n"
        "---\nExtract text from Word.\n",
        encoding="utf-8",
    )
    cov = stack_coverage(str(tmp_path))
    assert "refactor" in cov["detail"]["uncovered"]
    assert cov["value"] == 0


def test_redact_scan_clean_on_this_repo():
    text, code = run_redact_scan(repo_root=str(ROOT))
    assert code == 0, text
    assert "findings   0" in text
    assert "clean" in text


def test_redact_scan_goes_red_on_planted_secret(tmp_path):
    """Control must go RED — assembled at runtime so this file stays clean."""
    planted = tmp_path / "leak.txt"
    # Build a fake AWS access key shape without storing a real credential.
    key = "AKIA" + ("A" * 16)
    planted.write_text(f"aws_access_key_id = {key}\n", encoding="utf-8")
    findings = scan_tree(tmp_path)
    assert findings, "planted AKIA shape must match"
    assert findings[0]["kind"] == "aws_access_key"
    text, code = run_redact_scan(repo_root=str(tmp_path))
    assert code == 1
    assert "FINDINGS" in text


def test_redact_scan_example_marker_allowlist(tmp_path):
    key = "AKIA" + ("B" * 16)
    (tmp_path / "docs.md").write_text(
        f"example credential shape only: {key}\n", encoding="utf-8"
    )
    assert scan_tree(tmp_path) == []


def test_redact_scan_allowlist_not_substring_of_key(tmp_path):
    """'example' inside EXAMPLEKEY must not skip a planted secret."""
    # Assemble at runtime so this test file never matches scan_tree(ROOT).
    marker = "EXAMPLE" + "KEY"
    value = f"{marker}_NOT_A_MARKER_XX"
    (tmp_path / "cfg.env").write_text(
        "api" + "_key = \"" + value + "\"\n", encoding="utf-8"
    )
    findings = scan_tree(tmp_path)
    assert findings, "substring example inside key must not allowlist"


def test_naive_title_invents_complete_without_opening_skills(tmp_path):
    (tmp_path / "README.md").write_text("# Agent Skills framework\n", encoding="utf-8")
    (tmp_path / "skills").mkdir()
    naive = naive_title_verdict(str(tmp_path))
    assert naive["verdict"] == "complete"
    assert naive["opened_skill_md"] is False


def test_external_stack_on_fixture_and_real_grinder():
    fixture = measure_external_stack(str(FIXTURE))
    assert fixture["coverage"]["value"] == 8
    assert fixture["coverage"]["population"] == 12
    assert fixture["naive"]["verdict"] == "complete"  # has skills/
    text = render_external(fixture)
    assert "8/12" in text
    assert "naive_title" in text

    grinder = measure_external_stack(str(REAL_AG))
    assert grinder["coverage"]["value"] == 1
    assert grinder["coverage"]["population"] == 12
    assert "writing" in grinder["coverage"]["detail"]["covered_caps"]
    wine = next(f for f in grinder["fits"] if f["name"] == "wine-pairing")
    assert wine["label"] == "no-signal"


def test_fixture_inventory_still_present():
    inv = inventory(str(FIXTURE))
    assert inv["present"] is True
    assert len(inv["skills"]) >= 3
