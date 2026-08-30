"""Deterministic agent-run loop — 4 tools without Bedrock."""
import subprocess
import sys
from pathlib import Path

from magnet.agent_run import run_agent_loop

ROOT = Path(__file__).resolve().parents[1]


def test_agent_run_prints_four_tool_steps():
    out = run_agent_loop(repo_root=str(ROOT))
    assert "[run_probe]" in out
    assert "[record_week]" in out
    assert "[adopt_change]" in out
    assert "[check_docs]" in out
    assert "MAGNET receipt" in out
    assert "verdict    helped" in out


def test_agent_run_cli_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "agent-run"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "agent-run" in proc.stdout
