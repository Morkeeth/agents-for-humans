"""Deterministic agent loop — 4 tools in sequence, no Bedrock.

Simulates what the Strands agent does after a stack change: baseline reading,
adopt change, post-change reading, doc check, receipt.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta

from magnet.ledger import connect, latest_adoption, list_readings, record_reading, reset_demo
from magnet.demo import SIMULATED_WEEK_OFFSET_DAYS
from magnet.probes import DEMO_PROBE, run_demo_probe
from magnet.reporter import render_receipt, verdict
from magnet.tools import tool_adopt_change, tool_check_docs, tool_record_week, tool_run_probe


def run_agent_loop(
    *,
    ledger_path: str | None = None,
    repo_root: str | None = None,
    probe_name: str = DEMO_PROBE,
) -> str:
    """Execute the 4-tool chain and return a step log + receipt."""
    root = repo_root or os.getcwd()
    path = ledger_path or os.path.join(root, ".magnet", "ledger.db")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    conn = connect(path)
    reset_demo(conn)
    steps: list[str] = ["MAGNET agent-run (deterministic, no Bedrock)", ""]

    # 1. run_probe — baseline
    probe = tool_run_probe(probe_name, ledger_path=path)
    steps.append(f"  [run_probe]     {probe['value']}/{probe['population']}  ({probe['command']})")

    # 2. record_week — store baseline
    rec1 = tool_record_week(probe_name, ledger_path=path)
    steps.append(f"  [record_week]   verdict={rec1['verdict']}  readings={rec1['readings']}")

    # 3. adopt_change — fake skill adoption
    adoption = tool_adopt_change(
        "skill",
        "agent-run-verification-skill",
        "pass rate rises by 1/5",
        probe_name,
        ledger_path=path,
        apply_demo_bonus=True,
    )
    steps.append(f"  [adopt_change]  id={adoption['id']}  {adoption['description']}")

    # 4. run_probe + record_week — post-adoption (next week)
    post = run_demo_probe(conn)
    record_reading(
        conn,
        probe_name,
        post["value"],
        post["command"],
        population=post["population"],
        change_id=adoption["id"],
        # SIMULATED next week — flagged so it never prints as a real read time.
        now=datetime.now() + timedelta(days=SIMULATED_WEEK_OFFSET_DAYS),
        simulated=True,
    )
    readings = list_readings(conn, probe_name)
    label, _ = verdict(readings, direction="up")
    steps.append(
        f"  [record_week]   verdict={label}  readings={len(readings)}  "
        f"(week 2 SIMULATED, +{SIMULATED_WEEK_OFFSET_DAYS}d)"
    )

    # 5. check_docs
    docs = tool_check_docs(repo_root=root, ledger_path=path)
    steps.append(f"  [check_docs]    ok={docs['ok']}  drifted={docs['drifted']}/{docs['checked']}")

    adoption_row = latest_adoption(conn, probe_name)
    receipt = render_receipt(
        probe_name,
        readings,
        direction="up",
        change_label=adoption_row["description"] if adoption_row else "",
        repro_command="magnet agent-run",
    )

    # render_receipt already emits the repro line; do not print it twice.
    return "\n".join(steps + ["", receipt])
