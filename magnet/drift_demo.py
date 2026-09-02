"""Live drift demo — check_docs catches fabricated numbers (the Qwen lesson)."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from magnet.constants import TOOL_NAMES
from magnet.probes import _count_pytest_tests, check_docs, check_docs_exit_code


def run_drift_demo(*, repo_root: str | None = None) -> str:
    """Show check_docs failing on wrong claims, passing on re-derived source."""
    root = Path(repo_root or os.getcwd())
    actual_tests = _count_pytest_tests(root / "tests")

    lines = [
        "MAGNET drift-demo — check_docs catches fabricated numbers",
        "",
        "  The Qwen lesson: a doc claimed a number weeks ago; nobody re-ran the command.",
        "  MAGNET re-derives every claim from source at read time.",
        "",
        "  === fake repo (wrong claims) ===",
    ]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "README.md").write_text(
            "# fake\n\nStrands agent · 99 tools\n" + " ".join(TOOL_NAMES) + "\n",
            encoding="utf-8",
        )
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "REPORT.md").write_text("42 passed in 1.0s\n", encoding="utf-8")

        fake_failures = 0
        for row in check_docs(str(tmp_path)):
            mark = "PASS" if row["ok"] else "FAIL"
            if not row["ok"]:
                fake_failures += 1
            lines.append(f"  [{mark}] {row['claim']}: {row['why']}")

        fake_exit = check_docs_exit_code(str(tmp_path))
        lines.append(f"  exit code: {fake_exit}  ({fake_failures} drift(s))")

    lines += [
        "",
        "  === this repo (re-derived from source) ===",
    ]
    real_failures = 0
    for row in check_docs(str(root)):
        mark = "PASS" if row["ok"] else "FAIL"
        if not row["ok"]:
            real_failures += 1
        lines.append(f"  [{mark}] {row['claim']}: {row['why']}")

    real_exit = check_docs_exit_code(str(root))
    lines += [
        f"  exit code: {real_exit}  ({real_failures} drift(s))",
        "",
        f"  source     {actual_tests} test functions in tests/test_*.py",
        "  repro      magnet drift-demo",
    ]
    return "\n".join(lines)
