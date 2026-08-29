"""Demo + check_docs integration tests."""
import subprocess
import sys
from pathlib import Path

from magnet.demo import run_demo
from magnet.probes import check_docs
from magnet.tools import TOOL_NAMES


ROOT = Path(__file__).resolve().parents[1]


def test_demo_prints_helped_verdict():
    out = run_demo(repo_root=str(ROOT))
    assert "MAGNET receipt" in out
    assert "verdict    helped" in out
    assert "3/5" in out and "4/5" in out
    assert "naive verdict" in out


def test_four_strands_tools_exist():
    assert len(TOOL_NAMES) == 4
    assert set(TOOL_NAMES) == {"run_probe", "record_week", "adopt_change", "check_docs"}


def test_check_docs_passes_on_clean_readme():
    drifted = [r for r in check_docs(str(ROOT)) if not r["ok"]]
    assert not drifted, drifted


def test_magnet_demo_cli_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "helped" in proc.stdout
