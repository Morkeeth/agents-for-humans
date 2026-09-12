"""Slice 31 — history/one-workflow sidecars must carry prediction outcome."""
from __future__ import annotations

from pathlib import Path

from magnet.probes import check_docs

ROOT = Path(__file__).resolve().parents[1]


def test_history_sidecar_has_outcome_and_claimed():
    text = (ROOT / "docs" / "screenshots" / "history.txt").read_text(encoding="utf-8")
    assert "outcome" in text
    assert "claimed" in text.lower()


def test_one_workflow_sidecar_has_outcome():
    text = (ROOT / "docs" / "screenshots" / "one-workflow.txt").read_text(
        encoding="utf-8"
    )
    assert "outcome" in text


def test_check_docs_goes_red_when_history_lacks_outcome(tmp_path):
    """Control must go RED — the failure mode that let f690fd0 linger."""
    # Minimal fake repo with history sidecar missing outcome.
    (tmp_path / "README.md").write_text("MAGNET has 4 tools: run_probe record_week adopt_change check_docs\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_a.py").write_text("def test_a():\n    assert True\n")
    shots = tmp_path / "docs" / "screenshots"
    shots.mkdir(parents=True)
    (shots / "history.txt").write_text(
        "$ magnet history\nMAGNET history\n  verdict    helped\n  readings   2\n"
    )
    (shots / "one-workflow.txt").write_text("workflow paste without prediction grade line\n")
    results = {r["claim"]: r for r in check_docs(str(tmp_path))}
    assert results["screenshot history outcome"]["ok"] is False
    assert results["screenshot one-workflow outcome"]["ok"] is False
