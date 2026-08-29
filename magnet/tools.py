"""Strands tool surface — run_probe, record_week, adopt_change, check_docs."""
from __future__ import annotations

import json
from typing import Any

from magnet.constants import TOOL_NAMES
from magnet.ledger import connect, list_readings, record_reading
from magnet.probes import check_docs, check_docs_exit_code, run_probe
from magnet.reporter import verdict


def tool_run_probe(probe_name: str, *, ledger_path: str | None = None) -> dict:
    conn = connect(ledger_path)
    result = run_probe(conn, probe_name)
    return result


def tool_record_week(
    probe_name: str,
    *,
    ledger_path: str | None = None,
    change_id: int | None = None,
) -> dict:
    conn = connect(ledger_path)
    probe = run_probe(conn, probe_name)
    row = record_reading(
        conn,
        probe_name,
        probe.get("value"),
        probe["command"],
        population=probe.get("population"),
        change_id=change_id,
    )
    readings = list_readings(conn, probe_name)
    label, delta = verdict(readings, direction=probe.get("direction", "up"))
    return {
        "recorded": row,
        "readings": len(readings),
        "verdict": label,
        "delta": delta,
    }


def tool_adopt_change(
    change_type: str,
    description: str,
    prediction: str,
    probe_name: str,
    *,
    ledger_path: str | None = None,
    apply_demo_bonus: bool = False,
) -> dict:
    from magnet.ledger import adopt_change, set_demo_bonus

    conn = connect(ledger_path)
    if apply_demo_bonus or probe_name in ("demo-pass-rate", "demo"):
        set_demo_bonus(conn, 1)
    adoption = adopt_change(
        conn,
        change_type,
        description,
        prediction,
        probe_name,
    )
    return adoption


def tool_check_docs(*, repo_root: str | None = None, ledger_path: str | None = None) -> dict:
    root = repo_root or "."
    results = check_docs(root)
    drifted = [r for r in results if not r["ok"]]
    exit_code = check_docs_exit_code(root)
    return {
        "ok": exit_code == 0,
        "exit_code": exit_code,
        "checked": len(results),
        "drifted": len(drifted),
        "results": results,
    }


def build_strands_tools():
    """Return @tool-decorated callables for Strands Agent."""
    try:
        from strands import tool
    except ImportError as exc:
        raise ImportError("strands-agents is required for build_strands_tools()") from exc

    @tool
    def run_probe_tool(probe_name: str) -> dict:
        """Run an eval probe and return value/pop with the repro command."""
        return tool_run_probe(probe_name)

    @tool
    def record_week_tool(probe_name: str) -> dict:
        """Run probe, store this week's reading, return helped/hurt/baseline."""
        return tool_record_week(probe_name)

    @tool
    def adopt_change_tool(
        change_type: str,
        description: str,
        prediction: str,
        probe_name: str,
    ) -> dict:
        """Record a stack change and its testable prediction."""
        return tool_adopt_change(change_type, description, prediction, probe_name)

    @tool
    def check_docs_tool() -> dict:
        """Re-derive README numbers from source; non-zero exit on drift."""
        return tool_check_docs()

    return [run_probe_tool, record_week_tool, adopt_change_tool, check_docs_tool]


def create_agent(system_prompt: str | None = None):
    """Construct a Strands Agent wired to MAGNET tools."""
    from strands import Agent

    prompt = system_prompt or (
        "You are MAGNET, the adoption ledger for an agent stack. "
        "After the user changes a prompt, model, or skill, re-run their eval "
        "and report helped, hurt, or baseline — never invent a trend from one reading."
    )
    return Agent(tools=build_strands_tools(), system_prompt=prompt)


def tools_json_schema() -> list[dict[str, Any]]:
    """Machine-readable tool list for docs/tests."""
    return [
        {"name": "run_probe", "params": ["probe_name"]},
        {"name": "record_week", "params": ["probe_name"]},
        {"name": "adopt_change", "params": ["change_type", "description", "prediction", "probe_name"]},
        {"name": "check_docs", "params": []},
    ]
