"""Slice 32 — pytest paste 'N passed, M skipped' equals suite size N+M."""
from __future__ import annotations

from pathlib import Path

from magnet.probes import _suite_size_from_pytest_paste, check_docs


def test_suite_size_sums_passed_and_skipped():
    assert _suite_size_from_pytest_paste("252 passed, 1 skipped in 11.68s") == 253
    assert _suite_size_from_pytest_paste("7 failed, 247 passed, 1 skipped in 7.76s") == 255
    assert _suite_size_from_pytest_paste("10 passed in 0.1s") is None


def test_check_docs_accepts_honest_pytest_paste(tmp_path):
    (tmp_path / "README.md").write_text(
        "MAGNET has 4 tools: run_probe record_week adopt_change check_docs\n"
    )
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_a.py").write_text(
        "def test_one():\n    pass\ndef test_two():\n    pass\ndef test_three():\n    pass\n"
    )
    shots = tmp_path / "docs" / "screenshots"
    shots.mkdir(parents=True)
    (shots / "pytest.txt").write_text("2 passed, 1 skipped in 0.5s\n")
    (shots / "history.txt").write_text(
        "outcome    prediction-held\nclaimed Δ  amount=1\n"
    )
    (shots / "one-workflow.txt").write_text("outcome    prediction-held\n")
    results = {r["claim"]: r for r in check_docs(str(tmp_path))}
    assert results["screenshot pytest (docs/screenshots/pytest.txt)"]["ok"] is True
    assert results["screenshot pytest (docs/screenshots/pytest.txt)"]["doc_value"] == 3


def test_check_docs_accepts_failed_plus_passed_plus_skipped(tmp_path):
    (tmp_path / "README.md").write_text(
        "MAGNET has 4 tools: run_probe record_week adopt_change check_docs\n"
    )
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_a.py").write_text(
        "\n".join(f"def test_{i}():\n    pass\n" for i in range(5))
    )
    shots = tmp_path / "docs" / "screenshots"
    shots.mkdir(parents=True)
    (shots / "pytest.txt").write_text("2 failed, 2 passed, 1 skipped in 1.0s\n")
    (shots / "history.txt").write_text(
        "outcome    prediction-held\nclaimed Δ  amount=1\n"
    )
    (shots / "one-workflow.txt").write_text("outcome    prediction-held\n")
    results = {r["claim"]: r for r in check_docs(str(tmp_path))}
    assert results["screenshot pytest (docs/screenshots/pytest.txt)"]["ok"] is True
    assert results["screenshot pytest (docs/screenshots/pytest.txt)"]["doc_value"] == 5
