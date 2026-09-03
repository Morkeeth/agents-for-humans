"""coverage-delta + frontmatter body fallback."""
from __future__ import annotations

from pathlib import Path

from magnet.coverage_delta import render_coverage_delta, run_coverage_delta
from magnet.stack import _frontmatter_desc, inventory

ROOT = Path(__file__).resolve().parents[1]
CURSOR = ROOT / "fixtures" / "stack-cursor"
AUTHOR = ROOT / "fixtures" / "stack"


def test_frontmatter_empty_description_falls_back_to_body(tmp_path):
    """Live canvas skill had `description:` blank then `metadata:` — must not capture that."""
    skill = tmp_path / "skills" / "blank-desc" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\nname: blank-desc\ndescription: \nmetadata:\n  surfaces:\n    - ide\n---\n\n"
        "A canvas is a durable standalone artifact outside the transcript.\n",
        encoding="utf-8",
    )
    desc = _frontmatter_desc(str(skill))
    assert "metadata" not in desc.lower()
    assert "canvas" in desc.lower() or "durable" in desc.lower()


def test_coverage_delta_attributes_debug_on_cursor_stack():
    result = run_coverage_delta(
        "pdb-navigator",
        "Debug a failing test by driving pdb and bisecting the stack trace",
        stack_dir=str(CURSOR),
        repo_root=str(ROOT),
    )
    assert result["fit_label"] == "fills-gap"
    assert "debug" in result["predicted_caps"]
    assert result["after"]["value"] > result["before"]["value"]
    assert "debug" in result["newly_covered"]
    assert result["verdict"] == "attributed"
    text = render_coverage_delta(result)
    assert "attributed" in text
    assert "before" in text.lower() or "before" in text


def test_coverage_delta_noise_nothing_moved_or_no_signal():
    result = run_coverage_delta(
        "wine-pairing",
        "Recommend wine pairings for a menu",
        stack_dir=str(AUTHOR),
        repo_root=str(ROOT),
    )
    assert result["fit_label"] == "no-signal"
    assert result["verdict"] == "nothing-moved"
    assert result["newly_covered"] == []


def test_coverage_delta_cli(tmp_path):
    from magnet.cli import main

    code = main(
        [
            "--repo",
            str(ROOT),
            "coverage-delta",
            "--name",
            "safe-rename",
            "--text",
            "Refactor across a repo: rename a symbol, extract a function, simplify",
            "--stack",
            str(CURSOR),
        ]
    )
    assert code == 0


def test_cursor_stack_inventory_has_real_descriptions():
    inv = inventory(str(CURSOR))
    names = {s["name"] for s in inv["skills"]}
    assert "env-setup" in names
    assert "canvas" in names
    canvas = next(s for s in inv["skills"] if s["name"] == "canvas")
    assert "metadata" not in canvas["description"].lower()
    assert len(canvas["description"]) > 20
