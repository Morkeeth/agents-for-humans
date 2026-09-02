"""check_docs scans all judge/devpost docs for pytest count drift."""
from pathlib import Path

from magnet.probes import DOCS_WITH_PYTEST_COUNTS, check_docs, check_docs_exit_code


def test_judge_docs_listed_in_constant():
    assert "docs/JUDGE-SCORECARD-2026-09-02.md" in DOCS_WITH_PYTEST_COUNTS
    assert "docs/DEVPOST-READY.md" in DOCS_WITH_PYTEST_COUNTS


def test_check_docs_catches_wrong_count_in_judge_scorecard(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_a.py").write_text("def test_one():\n    pass\n")
    docs = tmp_path / "docs"
    docs.mkdir()
    for name in DOCS_WITH_PYTEST_COUNTS:
        sub = tmp_path / name
        sub.parent.mkdir(parents=True, exist_ok=True)
        sub.write_text("99 pytest tests\n", encoding="utf-8")
    drifted = [r for r in check_docs(str(tmp_path)) if not r["ok"]]
    assert len(drifted) >= len(DOCS_WITH_PYTEST_COUNTS)
    assert check_docs_exit_code(str(tmp_path)) == 1


def test_real_repo_judge_docs_match_source():
    root = Path(__file__).resolve().parents[1]
    drifted = [r for r in check_docs(str(root)) if not r["ok"]]
    assert not drifted, drifted
