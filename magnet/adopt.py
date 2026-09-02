"""`magnet adopt` — record a change, re-run probe, print receipt."""
from __future__ import annotations

import os

from magnet.log import connect, latest_adoption, list_readings, reset_demo
from magnet.reporter import render_receipt, verdict
from magnet.stack import default_stack_dir, fit_one, render_fit
from magnet.tools import tool_adopt_change, tool_record_week


def run_adopt(
    change_type: str,
    description: str,
    prediction: str,
    probe_name: str,
    *,
    log_path: str | None = None,
    apply_demo_bonus: bool = False,
    simulate_next_week: bool = True,
    reset: bool = False,
    fit: bool = False,
    stack_dir: str | None = None,
    fit_description: str | None = None,
) -> str:
    """Core loop: adopt change → re-probe → receipt (+ optional stack fit)."""
    path = log_path or os.path.join(os.getcwd(), ".magnet", "log.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = connect(path)
    if reset:
        reset_demo(conn)

    lines = ["MAGNET adopt", ""]

    # Baseline reading if none exists yet
    prior = list_readings(conn, probe_name)
    if not prior:
        base = tool_record_week(probe_name, log_path=path)
        lines.append(f"  baseline   verdict={base['verdict']}  readings={base['readings']}")

    adoption = tool_adopt_change(
        change_type,
        description,
        prediction,
        probe_name,
        log_path=path,
        apply_demo_bonus=apply_demo_bonus,
    )
    lines.append(f"  recorded   [{change_type}] {description}  (id={adoption['id']})")
    lines.append(f"  predict    {prediction}")

    rec = tool_record_week(
        probe_name,
        log_path=path,
        change_id=adoption["id"],
        simulate_next_week=simulate_next_week,
    )
    sim_note = "  (SIMULATED week)" if rec.get("simulated") else ""
    lines.append(
        f"  reading    verdict={rec['verdict']}  "
        f"{rec['readings']} readings{sim_note}"
    )
    lines.append("")

    row = latest_adoption(conn, probe_name)
    readings = list_readings(conn, probe_name)
    label, _ = verdict(readings, direction="up")
    receipt = render_receipt(
        probe_name,
        readings,
        direction="up",
        change_label=row["description"] if row else description,
        repro_command=f"magnet adopt {change_type} {description!r} {prediction!r} --probe {probe_name}",
    )
    parts = lines + [receipt]

    if fit:
        stack = stack_dir or default_stack_dir()
        surface = "agents" if change_type == "model" else "skills"
        # Prefer an explicit prose description for fit; fall back to prediction.
        prose = fit_description or prediction
        fit_result = fit_one(description, prose, stack, surface=surface)
        parts += ["", render_fit(fit_result)]

    return "\n".join(parts)
