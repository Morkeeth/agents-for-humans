"""The deterministic fallback chain — 4 tools, no agent, no model.

This was `magnet agent-run`'s only behaviour until the Strands agent loop was
wired in. It is kept as the fallback for when no model is reachable, so it keeps
its test. The DEFAULT path (a real Strands agent loop) is covered by
tests/test_agent_loop.py.
"""
import subprocess
import sys
from pathlib import Path

from magnet.agent_run import run_agent_loop

ROOT = Path(__file__).resolve().parents[1]


def test_deterministic_chain_prints_four_tool_steps():
    out = run_agent_loop(repo_root=str(ROOT), mode="none")
    assert "[run_probe]" in out
    assert "[record_week]" in out
    assert "[adopt_change]" in out
    assert "[check_docs]" in out
    assert "MAGNET receipt" in out
    assert "verdict    helped" in out


def test_deterministic_chain_declares_it_is_not_an_agent():
    """It must never be mistaken for the Strands loop."""
    out = run_agent_loop(repo_root=str(ROOT), mode="none")
    assert "deterministic fallback" in out
    assert "no agent, no model" in out


def test_agent_run_cli_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "agent-run", "--model", "none"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "agent-run" in proc.stdout
