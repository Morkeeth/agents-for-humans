"""check_docs re-derives pytest count from tests/*.py."""
from pathlib import Path

from magnet.probes import _count_pytest_tests, check_docs, check_docs_exit_code


def test_count_pytest_tests_matches_collection(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_a.py").write_text("def test_one():\n    pass\ndef test_two():\n    pass\n")
    (tests / "test_b.py").write_text("def test_three():\n    pass\n")
    assert _count_pytest_tests(tests) == 3


def test_check_docs_catches_wrong_pytest_count(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_x.py").write_text("def test_only():\n    pass\n")
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "STRANGER-PASS.md").write_text("17 passed in 0.69s\n", encoding="utf-8")
    drifted = [r for r in check_docs(str(tmp_path)) if not r["ok"]]
    assert any("pytest count" in r["claim"] for r in drifted)
    assert check_docs_exit_code(str(tmp_path)) == 1
