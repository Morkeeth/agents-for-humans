"""check_docs must catch README drift — the Qwen lesson."""
from pathlib import Path

from magnet.probes import check_docs, check_docs_exit_code


def test_check_docs_catches_wrong_tool_count(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "# test\n\nWe ship 99 tools: run_probe record_week adopt_change check_docs\n",
        encoding="utf-8",
    )
    drifted = [r for r in check_docs(str(tmp_path)) if not r["ok"]]
    assert any(r["claim"] == "tool count" for r in drifted)
    assert check_docs_exit_code(str(tmp_path)) == 1


def test_check_docs_passes_when_claim_matches_source(tmp_path):
    from magnet.constants import TOOL_NAMES

    readme = tmp_path / "README.md"
    readme.write_text(
        f"# test\n\nStrands agent · {len(TOOL_NAMES)} tools\n"
        + " ".join(TOOL_NAMES)
        + "\nMAGNET submits Sep 14. Agent Grinder is a companion product.\n",
        encoding="utf-8",
    )
    (tmp_path / "_NIGHT-SCOPE.md").write_text(
        "**EYES ruling:** MAGNET submits. Agent Grinder is a separate product.\n",
        encoding="utf-8",
    )
    # No screenshots/ dir → freshness claim must not apply (or we skip).
    # Provide a fresh sidecar pair so the new claims can pass in isolation.
    shots = tmp_path / "docs" / "screenshots"
    shots.mkdir(parents=True)
    (shots / "check-docs.txt").write_text(
        "sep14 entry ruling\n14 claims checked. All match source.\n",
        encoding="utf-8",
    )
    (shots / "pytest.txt").write_text("1 passed in 0.01s\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_a.py").write_text("def test_one():\n    pass\n")
    assert check_docs_exit_code(str(tmp_path)) == 0
