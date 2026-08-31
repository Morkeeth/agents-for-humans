"""Control: the Strands agent loop must actually run, and the mode must be honest.

Before this slice, `create_agent()` was defined and exported and had ZERO call
sites in the whole repo -- `grep -rn create_agent magnet/ tests/` found only the
definition and the re-export. The four tools carried @tool decorators and the
agent that would use them was never constructed. Against the competition's
criterion 1 ("How thoroughly and skillfully does the project use Strands
Agents?") that was the entry requirement, unmet.

These tests fail if it regresses to decoration.
"""
import subprocess
import sys
from pathlib import Path

import pytest
from strands import Agent

from magnet.agent_run import MODES, run_agent_loop, run_strands_agent
from magnet.local_model import DEFAULT_PLAN, ScriptedLocalModel
from magnet.tools import build_strands_tools, create_agent

ROOT = Path(__file__).resolve().parents[1]


def _db(tmp_path, name="agent.db"):
    return str(tmp_path / name)


# -- create_agent is real, and is actually called -------------------------
def test_create_agent_returns_a_real_strands_agent():
    agent = create_agent(model=ScriptedLocalModel())
    assert isinstance(agent, Agent), type(agent)
    assert len(agent.tool_names) == 4, agent.tool_names


def test_agent_loop_dispatches_all_four_tools_through_strands(tmp_path):
    """The SDK's event loop -- not our code -- must call the four tools."""
    model = ScriptedLocalModel()
    agent = create_agent(model=model, log_path=_db(tmp_path), repo_root=str(ROOT))
    agent("Measure the stack change.")

    dispatched = [
        b["toolUse"]["name"]
        for m in agent.messages
        for b in m.get("content", [])
        if "toolUse" in b
    ]
    assert dispatched == [name for name, _ in DEFAULT_PLAN], dispatched
    assert set(dispatched) == {
        "run_probe_tool", "record_week_tool", "adopt_change_tool", "check_docs_tool",
    }
    # tool RESULTS came back too -- a dispatch that errored is not a working loop
    results = [
        b["toolResult"]
        for m in agent.messages
        for b in m.get("content", [])
        if "toolResult" in b
    ]
    assert len(results) == len(DEFAULT_PLAN)
    assert all(r.get("status") == "success" for r in results), results


def test_agent_run_local_mode_uses_the_agent_and_says_so(tmp_path):
    out = run_agent_loop(log_path=_db(tmp_path), repo_root=str(ROOT), mode="local")
    assert "strands agent loop" in out
    assert "local scripted model" in out
    assert "tools dispatched     5" in out
    assert "verdict    helped" in out
    # honesty: it must not let a reader think an LLM chose the tools
    assert "not an LLM" in out
    assert "DEGRADED" not in out


def test_agent_run_writes_readings_the_receipt_can_use(tmp_path):
    """The loop must really move data, not just emit step lines."""
    from magnet.log import connect, list_readings

    path = _db(tmp_path)
    run_agent_loop(log_path=path, repo_root=str(ROOT), mode="local")
    readings = list_readings(connect(path), "demo-pass-rate")
    assert len(readings) == 2, readings
    assert [r["value"] for r in readings] == [3, 4]
    assert readings[1]["detail"].get("simulated") is True


# -- the mode is never silently swapped -----------------------------------
def test_deterministic_mode_is_labelled_as_not_an_agent(tmp_path):
    out = run_agent_loop(log_path=_db(tmp_path), repo_root=str(ROOT), mode="none")
    assert "deterministic fallback" in out
    assert "no agent, no model" in out
    assert "strands agent loop" not in out


def test_a_failing_agent_mode_shouts_instead_of_degrading_quietly(tmp_path, monkeypatch):
    """If the agent cannot run, the fallback must be impossible to miss."""
    import magnet.agent_run as ar

    def boom(**_):
        raise RuntimeError("no credentials")

    monkeypatch.setattr(ar, "run_strands_agent", boom)
    out = ar.run_agent_loop(log_path=_db(tmp_path), repo_root=str(ROOT), mode="bedrock")
    assert "FAILED" in out and "DEGRADED" in out
    assert "RuntimeError: no credentials" in out
    assert "deterministic fallback" in out


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError):
        run_agent_loop(mode="totally-not-a-mode")
    assert MODES == ("local", "bedrock", "none")


# -- guards on the local provider -----------------------------------------
def test_scripted_model_refuses_a_tool_the_agent_never_registered():
    """A typo'd plan must explode, not look like a model that chose nothing."""
    model = ScriptedLocalModel(plan=[("no_such_tool", {})])
    agent = create_agent(model=model)
    with pytest.raises(Exception) as exc:
        agent("go")
    assert "not a registered tool" in str(exc.value)


def test_local_mode_never_constructs_a_bedrock_model(tmp_path, monkeypatch):
    """Hard guard against accidental spend: Bedrock must never be instantiated."""
    import strands.models

    def boom(*a, **k):
        raise AssertionError("local mode constructed a BedrockModel -- possible spend")

    monkeypatch.setattr(strands.models, "BedrockModel", boom)
    out = run_agent_loop(log_path=_db(tmp_path), repo_root=str(ROOT), mode="local")
    assert "tools dispatched     5" in out
    assert "DEGRADED" not in out


def test_local_mode_opens_no_network_socket(tmp_path, monkeypatch):
    """Second spend guard, at the socket. Imports are warmed first so this
    measures the RUN, not strands' import-time machinery."""
    import socket

    run_agent_loop(log_path=_db(tmp_path, "warm.db"), repo_root=str(ROOT), mode="local")

    opened = []
    real = socket.socket

    class Watched(real):
        def __init__(self, *a, **k):
            opened.append(a)
            super().__init__(*a, **k)

    monkeypatch.setattr(socket, "socket", Watched)
    out = run_agent_loop(log_path=_db(tmp_path), repo_root=str(ROOT), mode="local")
    assert "tools dispatched     5" in out
    assert "DEGRADED" not in out

    # asyncio's own event loop makes AF_UNIX socketpairs; those reach nothing.
    # An AF_INET/AF_INET6 socket is the one that could reach Bedrock and spend.
    internet = [
        a for a in opened
        if a and a[0] in (socket.AF_INET, socket.AF_INET6)
    ]
    assert internet == [], f"local mode opened internet socket(s): {internet}"


def test_cli_agent_run_defaults_to_local_and_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "agent-run"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "strands agent loop" in proc.stdout
    assert "bedrock" not in proc.stdout.split("NOTE:")[0].lower()
