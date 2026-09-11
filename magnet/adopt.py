"""`magnet adopt` — record a change, re-run probe, print receipt."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from magnet.constants import STACK_CHANGE_TYPES
from magnet.log import connect, list_readings, reset_demo, set_adoption_detail
from magnet.prediction import check_prediction, render_prediction_check
from magnet.probes import STACK_COVERAGE_PROBE, is_builtin_probe
from magnet.stack_bind import STACK_BIND_PROBES
from magnet.reporter import render_receipt, verdict
from magnet.stack import (
    fit_one,
    install_skill,
    read_skill_source,
    render_fit,
    resolve_stack_dir,
)
from magnet.stack_demo import naive_install_verdict
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
    install_from: str | None = None,
) -> str:
    """Core loop: adopt change → (optional install into stack) → re-probe → receipt."""
    path = log_path or os.path.join(os.getcwd(), ".magnet", "log.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = connect(path)
    if reset:
        reset_demo(conn)

    source_stack = resolve_stack_dir(stack_dir)
    work_stack = source_stack
    installed_meta = None
    skill_prose = fit_description

    if install_from:
        if change_type != "skill":
            return "magnet adopt --install requires change_type=skill"
        work = Path(os.getcwd()) / ".magnet" / "adopt-work-stack"
        if work.exists():
            shutil.rmtree(work)
        shutil.copytree(source_stack, work)
        work_stack = str(work)
        src = read_skill_source(install_from)
        skill_prose = fit_description or src["description"] or prediction
        description = src["name"] or description

    if probe_name in (STACK_COVERAGE_PROBE, "stack-coverage") or install_from or probe_name in STACK_BIND_PROBES:
        probe_stack: str | None = work_stack
    else:
        probe_stack = stack_dir  # may be None → default / MAGNET_STACK

    lines = ["MAGNET adopt", ""]

    # Baseline reading if none exists yet — BEFORE install so delta is real.
    prior = list_readings(conn, probe_name)
    if not prior:
        base = tool_record_week(probe_name, log_path=path, stack_dir=probe_stack)
        lines.append(f"  baseline   verdict={base['verdict']}  readings={base['readings']}")

    if install_from:
        src = read_skill_source(install_from)
        installed_meta = install_skill(
            work_stack,
            name=src["name"] or description,
            description=skill_prose or src["description"],
            body=src["body"],
        )
        lines.append(f"  installed  {installed_meta['path']}")

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
        stack_dir=probe_stack,
    )
    sim_note = "  (SIMULATED week)" if rec.get("simulated") else ""
    lines.append(
        f"  reading    verdict={rec['verdict']}  "
        f"{rec['readings']} readings{sim_note}"
    )
    lines.append("")

    readings = list_readings(conn, probe_name)
    label, delta = verdict(readings, direction="up")
    # Bind to THIS adoption's description — never latest_adoption by timestamp
    # (same-second tie printed FIRST on a SECOND receipt, 2026-09-11).
    receipt = render_receipt(
        probe_name,
        readings,
        direction="up",
        change_label=description,
        repro_command=(
            f"magnet adopt {change_type} {description!r} {prediction!r} "
            f"--probe {probe_name}"
            + (f" --install {install_from}" if install_from else "")
        ),
    )
    if (
        change_type in STACK_CHANGE_TYPES
        and is_builtin_probe(probe_name)
        and probe_name not in (STACK_COVERAGE_PROBE, "stack-coverage")
        and probe_name not in STACK_BIND_PROBES
    ):
        receipt += (
            f"\n  measures   repo only — {probe_name} reads this repo, not the stack; "
            f"a {change_type} change is invisible to it. Add a registry probe that "
            f"reads the stack (docs/probes.json.example) to measure this adoption."
        )
    elif probe_name in STACK_BIND_PROBES or probe_name in (STACK_COVERAGE_PROBE, "stack-coverage"):
        receipt += f"\n  measures   stack — {probe_name} opens the stack object"
    parts = lines + [receipt]

    if install_from:
        parts += [
            "",
            "MAGNET naive install arm (baseline we did not invent as our best)",
            f"  naive      {naive_install_verdict(installed=True)}  ← any install = helped",
            f"  magnet     {label}",
        ]

    if fit or install_from:
        # Fit against the PRE-install stack so fills-gap is not erased by install.
        surface = "agents" if change_type == "model" else "skills"
        prose = skill_prose or prediction
        fit_result = fit_one(description, prose, source_stack, surface=surface)
        parts += ["", render_fit(fit_result)]

    # Grade the free-text prediction against the measured verdict (helicon S3).
    pred_check = check_prediction(prediction, label, delta)
    set_adoption_detail(conn, adoption["id"], {"prediction_check": pred_check})
    parts += ["", render_prediction_check(pred_check)]

    return "\n".join(parts)
