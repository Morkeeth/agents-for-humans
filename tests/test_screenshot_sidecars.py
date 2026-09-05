"""Slice 17 — screenshot sidecars must not stay green while the suite moves."""
from __future__ import annotations

from pathlib import Path

from magnet.probes import SCREENSHOT_CHECK_DOCS, check_docs

ROOT = Path(__file__).resolve().parents[1]


def test_check_docs_fails_on_stale_screenshot_sidecar(tmp_path):
    (tmp_path / "README.md").write_text(
        "# MAGNET\nStrands agent · 4 tools\n"
        "run_probe record_week adopt_change check_docs\n"
        "MAGNET submits Sep 14. Companion: Agent Grinder.\n",
        encoding="utf-8",
    )
    (tmp_path / "_NIGHT-SCOPE.md").write_text(
        "**EYES ruling:** MAGNET submits.\n", encoding="utf-8"
    )
    shots = tmp_path / "docs" / "screenshots"
    shots.mkdir(parents=True)
    (shots / "check-docs.txt").write_text(
        "$ magnet check-docs\n"
        "[PASS] pytest count (docs/REPORT.md): claims 113 tests, source has 113 tests\n"
        "11 claims checked. All match source.\n",
        encoding="utf-8",
    )
    (shots / "pytest.txt").write_text(
        "$ python3 -m pytest -q\n113 passed in 1.0s\n", encoding="utf-8"
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_a.py").write_text("def test_one():\n    pass\n")
    results = {r["claim"]: r for r in check_docs(str(tmp_path))}
    assert results["screenshot check-docs sidecar"]["ok"] is False
    assert results["pytest count (docs/screenshots/pytest.txt)"]["ok"] is False


def test_real_repo_screenshot_sidecars_match_after_capture():
    results = {r["claim"]: r for r in check_docs(str(ROOT))}
    assert "screenshot check-docs sidecar" in results
    assert results["screenshot check-docs sidecar"]["ok"] is True, results[
        "screenshot check-docs sidecar"
    ]
    key = "pytest count (docs/screenshots/pytest.txt)"
    assert key in results
    assert results[key]["ok"] is True, results[key]
