"""`magnet agent-run` — the four MAGNET tools driven by a real Strands agent loop.

THREE MODES, AND THE MODE IS ALWAYS PRINTED
-------------------------------------------
  local     (default) a real `strands.Agent` event loop over the four @tool
            functions, driven by `ScriptedLocalModel`. No network, no AWS
            credentials, no spend. The loop, the tool registry and the tool
            dispatch are genuine Strands machinery; the token generation is not
            a language model, it replays a fixed plan.

  bedrock   the same real agent loop with the Strands default model provider
            (Amazon Bedrock). This is a language model actually choosing the
            tools. It REQUIRES AWS credentials and IT COSTS MONEY, so it is
            never the default and never runs in CI.

  none      the original deterministic chain: the plain Python tool functions
            called in a fixed order, no Agent involved. Kept as the fallback for
            when no model is reachable.

If an agent mode fails, this module does NOT silently degrade. It prints the
failure and the exact reason, says which mode it fell back to, and marks the
result DEGRADED.
"""
from __future__ import annotations

import os

from magnet.constants import SIMULATED_WEEK_OFFSET_DAYS
from magnet.log import connect, latest_adoption, list_readings, reset_demo
from magnet.probes import DEMO_PROBE
from magnet.reporter import render_receipt, verdict
from magnet.tools import tool_adopt_change, tool_check_docs, tool_record_week, tool_run_probe

MODES = ("local", "bedrock", "none")

DETERMINISTIC_LABEL = "deterministic fallback · no agent, no model (4 tools called in sequence)"
BEDROCK_LABEL = "strands agent loop · Amazon Bedrock (real model — needs AWS credentials, costs money)"

AGENT_TASK = (
    "I just added a new skill to my agent stack called "
    "'agent-run-verification-skill'. I predict it raises the demo-pass-rate probe "
    "by 1 out of 5. Measure the probe now, record the reading, log the change and "
    "its prediction, record a second reading for the following week "
    "(simulate_next_week=true, this is a demo), then check the docs for drift."
)


def _log_path(log_path: str | None, root: str) -> str:
    path = log_path or os.path.join(root, ".magnet", "log.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    return path


def _receipt(conn, probe_name: str, repro: str) -> str:
    readings = list_readings(conn, probe_name)
    row = latest_adoption(conn, probe_name)
    return render_receipt(
        probe_name,
        readings,
        direction="up",
        change_label=row["description"] if row else "",
        repro_command=repro,
    )


# --------------------------------------------------------------------------
# mode: none — the original deterministic chain, unchanged in behaviour
# --------------------------------------------------------------------------
def run_deterministic_loop(
    *, log_path: str | None = None, repo_root: str | None = None, probe_name: str = DEMO_PROBE
) -> str:
    root = repo_root or os.getcwd()
    path = _log_path(log_path, root)
    conn = connect(path)
    reset_demo(conn)

    steps = [f"MAGNET agent-run  [MODE: {DETERMINISTIC_LABEL}]", ""]

    probe = tool_run_probe(probe_name, log_path=path)
    steps.append(f"  [run_probe]     {probe['value']}/{probe['population']}  ({probe['command']})")

    rec1 = tool_record_week(probe_name, log_path=path)
    steps.append(f"  [record_week]   verdict={rec1['verdict']}  readings={rec1['readings']}")

    adoption = tool_adopt_change(
        "skill", "agent-run-verification-skill", "pass rate rises by 1/5",
        probe_name, log_path=path, apply_demo_bonus=True,
    )
    steps.append(f"  [adopt_change]  id={adoption['id']}  {adoption['description']}")

    rec2 = tool_record_week(probe_name, log_path=path, simulate_next_week=True)
    steps.append(
        f"  [record_week]   verdict={rec2['verdict']}  readings={rec2['readings']}  "
        f"(week 2 SIMULATED, +{SIMULATED_WEEK_OFFSET_DAYS}d)"
    )

    docs = tool_check_docs(repo_root=root, log_path=path)
    steps.append(f"  [check_docs]    ok={docs['ok']}  drifted={docs['drifted']}/{docs['checked']}")

    return "\n".join(steps + ["", _receipt(conn, probe_name, "magnet agent-run --model none")])


# --------------------------------------------------------------------------
# modes: local / bedrock — a real strands.Agent event loop
# --------------------------------------------------------------------------
def run_strands_agent(
    *,
    log_path: str | None = None,
    repo_root: str | None = None,
    probe_name: str = DEMO_PROBE,
    mode: str = "local",
) -> str:
    """Run the four tools through a genuine Strands Agent. Raises on failure."""
    from magnet.tools import create_agent

    root = repo_root or os.getcwd()
    path = _log_path(log_path, root)
    conn = connect(path)
    reset_demo(conn)

    if mode == "local":
        from magnet.local_model import ScriptedLocalModel

        model = ScriptedLocalModel()
        label = model.MODE_LABEL
    elif mode == "bedrock":
        model, label = None, BEDROCK_LABEL
    else:
        raise ValueError(f"unknown agent mode: {mode!r}")

    agent = create_agent(model=model, log_path=path, repo_root=root)
    result = agent(AGENT_TASK)

    # Report the tools the SDK's own event loop actually dispatched, read back
    # from the agent's message history -- not from our plan, and not from a claim.
    dispatched = [
        block["toolUse"]["name"]
        for message in agent.messages
        for block in message.get("content", [])
        if "toolUse" in block
    ]

    steps = [
        f"MAGNET agent-run  [MODE: {label}]",
        "",
        f"  agent turns          {len(agent.messages)}",
        f"  tools dispatched     {len(dispatched)}  (by the Strands event loop)",
    ]
    for i, name in enumerate(dispatched, 1):
        steps.append(f"    {i}. {name}")

    if mode == "local":
        steps += [
            "",
            "  NOTE: the agent loop, tool registry and tool dispatch above are real",
            "        Strands. The model is a local scripted provider, not an LLM --",
            "        it replays a fixed plan. For a model that genuinely chooses the",
            "        tools, run: magnet agent-run --model bedrock  (needs AWS creds,",
            "        costs money). This has never been run in CI.",
        ]

    summary = str(result).strip()
    if summary:
        steps += ["", f"  agent said           {summary}"]

    return "\n".join(steps + ["", _receipt(conn, probe_name, f"magnet agent-run --model {mode}")])


# --------------------------------------------------------------------------
# public entry
# --------------------------------------------------------------------------
def run_agent_loop(
    *,
    log_path: str | None = None,
    repo_root: str | None = None,
    probe_name: str = DEMO_PROBE,
    mode: str = "local",
) -> str:
    """Run `magnet agent-run`. Never degrades silently."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, got {mode!r}")

    if mode == "none":
        return run_deterministic_loop(
            log_path=log_path, repo_root=repo_root, probe_name=probe_name
        )

    try:
        return run_strands_agent(
            log_path=log_path, repo_root=repo_root, probe_name=probe_name, mode=mode
        )
    except Exception as exc:  # noqa: BLE001 -- the reason is printed, never swallowed
        banner = [
            "!" * 72,
            f"!! STRANDS AGENT MODE {mode!r} FAILED — FALLING BACK TO THE DETERMINISTIC CHAIN",
            f"!! {type(exc).__name__}: {exc}",
            "!! The result below did NOT come from an agent loop. It is DEGRADED.",
            "!" * 72,
            "",
        ]
        body = run_deterministic_loop(
            log_path=log_path, repo_root=repo_root, probe_name=probe_name
        )
        return "\n".join(banner) + body + "\n\n  status     DEGRADED (agent mode failed; see banner above)"
