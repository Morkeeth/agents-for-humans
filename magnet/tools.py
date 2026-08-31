"""Strands tool surface — run_probe, record_week, adopt_change, check_docs."""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

from magnet.constants import SIMULATED_WEEK_OFFSET_DAYS, TOOL_NAMES
from magnet.log import connect, list_readings, record_reading
from magnet.probes import check_docs, check_docs_exit_code, run_probe
from magnet.reporter import verdict


def tool_run_probe(probe_name: str, *, log_path: str | None = None) -> dict:
    conn = connect(log_path)
    result = run_probe(conn, probe_name)
    return result


def tool_record_week(
    probe_name: str,
    *,
    log_path: str | None = None,
    change_id: int | None = None,
    simulate_next_week: bool = False,
) -> dict:
    """Run the probe and store this week's reading.

    `simulate_next_week=True` is a DEMO affordance: it advances the stored clock
    so the reading lands in the following ISO week, which is what lets a single
    run produce a helped/hurt verdict instead of a lone baseline. The row is
    flagged `simulated` in the database and every surface prints it as SIMULATED
    rather than as a real read time.
    """
    conn = connect(log_path)
    probe = run_probe(conn, probe_name)
    now = None
    if simulate_next_week:
        now = datetime.now() + timedelta(days=SIMULATED_WEEK_OFFSET_DAYS)
    row = record_reading(
        conn,
        probe_name,
        probe.get("value"),
        probe["command"],
        population=probe.get("population"),
        change_id=change_id,
        now=now,
        simulated=simulate_next_week,
    )
    readings = list_readings(conn, probe_name)
    label, delta = verdict(readings, direction=probe.get("direction", "up"))
    return {
        "recorded": row,
        "readings": len(readings),
        "verdict": label,
        "delta": delta,
        "simulated": bool(simulate_next_week),
    }


def tool_adopt_change(
    change_type: str,
    description: str,
    prediction: str,
    probe_name: str,
    *,
    log_path: str | None = None,
    apply_demo_bonus: bool = False,
) -> dict:
    from magnet.log import adopt_change, set_demo_bonus

    conn = connect(log_path)
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


def tool_check_docs(*, repo_root: str | None = None, log_path: str | None = None) -> dict:
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


SYSTEM_PROMPT = (
    "You are MAGNET, the adoption log for an agent stack. "
    "After the user changes a prompt, model, or skill, re-run their eval "
    "and report helped, hurt, or baseline — never invent a trend from one reading. "
    "Always use the tools; never guess a number. Call run_probe to measure, "
    "record_week to store the reading, adopt_change to log the change and its "
    "prediction, record_week again after the change, and check_docs to confirm "
    "the documented numbers still match source."
)


def build_strands_tools(*, log_path: str | None = None, repo_root: str | None = None):
    """Return @tool-decorated callables for a Strands Agent.

    `log_path`/`repo_root` are bound into the closures so an Agent run writes
    to the same database the caller is reading, instead of whatever the process
    working directory happens to be.
    """
    try:
        from strands import tool
    except ImportError as exc:
        raise ImportError("strands-agents is required for build_strands_tools()") from exc

    @tool
    def run_probe_tool(probe_name: str) -> dict:
        """Run an eval probe and return value/pop with the repro command."""
        return tool_run_probe(probe_name, log_path=log_path)

    @tool
    def record_week_tool(probe_name: str, simulate_next_week: bool = False) -> dict:
        """Run probe, store this week's reading, return helped/hurt/baseline.

        Set simulate_next_week=true ONLY in a demo, to place this reading in the
        following week so a two-reading verdict is possible. The reading is
        marked SIMULATED everywhere it is shown.
        """
        return tool_record_week(
            probe_name, log_path=log_path, simulate_next_week=simulate_next_week
        )

    @tool
    def adopt_change_tool(
        change_type: str,
        description: str,
        prediction: str,
        probe_name: str,
    ) -> dict:
        """Record a stack change and its testable prediction."""
        return tool_adopt_change(
            change_type, description, prediction, probe_name, log_path=log_path
        )

    @tool
    def check_docs_tool() -> dict:
        """Re-derive README numbers from source; non-zero exit on drift."""
        return tool_check_docs(repo_root=repo_root, log_path=log_path)

    return [run_probe_tool, record_week_tool, adopt_change_tool, check_docs_tool]


def create_agent(
    system_prompt: str | None = None,
    *,
    model=None,
    log_path: str | None = None,
    repo_root: str | None = None,
):
    """Construct a Strands Agent wired to the four MAGNET tools.

    `model` is any Strands model provider. Pass `magnet.local_model.ScriptedLocalModel`
    to run the real agent loop with no network and no spend. Leave it None to use
    the Strands default (Amazon Bedrock), which REQUIRES AWS credentials and COSTS
    MONEY — callers should make that choice explicit and visible on screen.
    """
    from strands import Agent

    return Agent(
        tools=build_strands_tools(log_path=log_path, repo_root=repo_root),
        system_prompt=system_prompt or SYSTEM_PROMPT,
        # Silence the SDK's default stdout printer: agent_run reports the tools it
        # dispatched by reading them back out of agent.messages instead.
        callback_handler=None,
        **({"model": model} if model is not None else {}),
    )


def tools_json_schema() -> list[dict[str, Any]]:
    """Machine-readable tool list for docs/tests."""
    return [
        {"name": "run_probe", "params": ["probe_name"]},
        {"name": "record_week", "params": ["probe_name"]},
        {"name": "adopt_change", "params": ["change_type", "description", "prediction", "probe_name"]},
        {"name": "check_docs", "params": []},
    ]
