"""Probes — deterministic eval runners with repro commands."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

DEMO_PROBE = "demo-pass-rate"
CHECK_DOCS_PROBE = "check-docs"
PYTEST_PROBE = "pytest-pass-rate"

BUILTIN_PROBES = (
    {
        "name": DEMO_PROBE,
        "command": "magnet probe demo-pass-rate",
        "direction": "up",
        "description": "Synthetic pass-rate for cold demo (skill_bonus in SQLite)",
    },
    {
        "name": CHECK_DOCS_PROBE,
        "command": "python -m magnet.check_docs",
        "direction": "up",
        "description": "Re-derive README claims; value=passing/total",
    },
    {
        "name": PYTEST_PROBE,
        "command": f"{sys.executable} -m pytest -q --tb=no",
        "direction": "up",
        "description": "Real eval: run pytest and count passed/total",
    },
)


def run_demo_probe(conn, *, command: str | None = None) -> dict:
    """Synthetic pass-rate probe for cold demo.

    Base score 3/5; adopting the demo skill adds +1 via demo_state.skill_bonus.
    """
    from magnet.log import get_demo_bonus

    bonus = get_demo_bonus(conn)
    value = 3 + bonus
    population = 5
    cmd = command or "magnet probe demo-pass-rate"
    return {
        "probe_name": DEMO_PROBE,
        "value": value,
        "population": population,
        "command": cmd,
        "direction": "up",
    }


def run_pytest_probe(*, repo_root: str | None = None, command: str | None = None) -> dict:
    """Run actual pytest — value/pop re-derived from subprocess output, not docs."""
    import os

    from magnet.registry import parse_pytest_summary

    if os.environ.get("PYTEST_CURRENT_TEST") and command is None:
        raise RuntimeError(
            "pytest-pass-rate refuses to run the full suite inside pytest "
            "(recursive). Run `magnet probe pytest-pass-rate` from the CLI, "
            "or pass an explicit command= for a scoped eval."
        )

    root = repo_root or os.getcwd()
    cmd = command or f"{sys.executable} -m pytest -q --tb=no"
    argv = cmd if isinstance(cmd, list) else cmd.split()
    proc = subprocess.run(
        argv,
        cwd=root,
        capture_output=True,
        text=True,
        timeout=300,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    value, population = parse_pytest_summary(combined)
    return {
        "probe_name": PYTEST_PROBE,
        "value": value,
        "population": population,
        "command": cmd,
        "direction": "up",
        "detail": {"exit_code": proc.returncode, "real_eval": True},
    }


def run_probe(conn, probe_name: str, *, repo_root: str | None = None) -> dict:
    root = repo_root or os.getcwd()
    if probe_name in (DEMO_PROBE, "demo-pass-rate", "demo"):
        return run_demo_probe(conn)
    if probe_name in (CHECK_DOCS_PROBE, "check-docs"):
        return run_check_docs_probe(root)
    if probe_name in (PYTEST_PROBE, "pytest-pass-rate"):
        return run_pytest_probe(repo_root=root)
    from magnet.registry import load_registry, run_registry_probe

    registry = load_registry(root)
    if probe_name in registry:
        return run_registry_probe(probe_name, registry[probe_name], repo_root=root)
    raise ValueError(f"unknown probe: {probe_name}")


def run_check_docs_probe(repo_root: str) -> dict:
    """Re-derive README tool count; value=passing claims, pop=total claims."""
    results = check_docs(repo_root)
    total = len(results)
    passing = sum(1 for r in results if r["ok"])
    cmd = "python -m magnet.check_docs"
    return {
        "probe_name": CHECK_DOCS_PROBE,
        "value": passing,
        "population": total,
        "command": cmd,
        "direction": "up",
        "detail": {"failures": [r for r in results if not r["ok"]]},
    }


def _count_pytest_tests(tests_dir: Path) -> int:
    """Re-derive test count from tests/*.py — never carry a number from docs."""
    count = 0
    if not tests_dir.is_dir():
        return 0
    for path in sorted(tests_dir.glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        count += len(re.findall(r"^\s*def test_", text, re.M))
    return count


def check_docs(repo_root: str) -> list[dict]:
    """Doc-drift for THIS repo — re-derive README numbers from source."""
    root = Path(repo_root)
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    results: list[dict] = []

    # Claim: "4 tools" in README vs actual Strands tool count
    tool_count = _count_strands_tools()
    claimed_tools = _first_int(readme, r"(\d+)\s+tools?")
    results.append(
        _result(
            "tool count",
            "README.md",
            claimed_tools,
            tool_count,
            claimed_tools == tool_count,
            f"README claims {claimed_tools} tools, source has {tool_count}",
        )
    )

    # Claim: pytest test count in STRANGER-PASS / REPORT vs actual def test_ count
    actual_tests = _count_pytest_tests(root / "tests")
    for doc_name in ("docs/STRANGER-PASS.md", "docs/REPORT.md"):
        doc_path = root / doc_name
        if not doc_path.is_file():
            continue
        doc_text = doc_path.read_text(encoding="utf-8")
        claimed_tests = _first_int(doc_text, r"(\d+)\s+passed")
        if claimed_tests is not None:
            results.append(
                _result(
                    f"pytest count ({doc_name})",
                    doc_name,
                    claimed_tests,
                    actual_tests,
                    claimed_tests == actual_tests,
                    f"{doc_name} claims {claimed_tests} passed, source has {actual_tests} tests",
                )
            )

    # Claim: probe names listed in README
    for name in ("run_probe", "record_week", "adopt_change", "check_docs"):
        ok = name in readme
        results.append(
            _result(
                f"tool {name}",
                "README.md",
                name if ok else None,
                name,
                ok,
                "listed" if ok else f"{name} missing from README",
            )
        )

    return results


def _count_strands_tools() -> int:
    from magnet.constants import TOOL_NAMES

    return len(TOOL_NAMES)


def _first_int(text: str, pattern: str) -> int | None:
    m = re.search(pattern, text, re.I)
    return int(m.group(1)) if m else None


def _result(claim: str, doc: str, doc_value, source, ok: bool, why: str) -> dict:
    return {
        "claim": claim,
        "doc": doc,
        "doc_value": doc_value,
        "source": source,
        "ok": ok,
        "why": why,
    }


def check_docs_exit_code(repo_root: str) -> int:
    drifted = [r for r in check_docs(repo_root) if not r["ok"]]
    return 1 if drifted else 0
