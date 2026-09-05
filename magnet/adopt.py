"""`magnet adopt` — record a change, re-run probe, print receipt."""
from __future__ import annotations

import os

from magnet.apply import apply_skill_to_stack, default_apply_dest
from magnet.constants import STACK_CHANGE_TYPES
from magnet.log import connect, latest_adoption, list_readings, reset_demo
from magnet.probes import STACK_COVERAGE_PROBE, is_builtin_probe
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
    apply: bool = False,
    apply_dest: str | None = None,
    repo_root: str | None = None,
) -> str:
    """Core loop: adopt change → (optional apply) → re-probe → receipt (+ fit)."""
    root = repo_root or os.getcwd()
    path = log_path or os.path.join(root, ".magnet", "log.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = connect(path)
    if reset:
        reset_demo(conn)

    source_stack = stack_dir or default_stack_dir(root)
    probe_stack = source_stack
    applied_info: dict | None = None

    lines = ["MAGNET adopt", ""]

    # Baseline reading if none exists yet — must see the pre-apply stack.
    prior = list_readings(conn, probe_name)
    if not prior:
        base = tool_record_week(
            probe_name, log_path=path, stack_dir=probe_stack, repo_root=root
        )
        lines.append(f"  baseline   verdict={base['verdict']}  readings={base['readings']}")

    if apply:
        if change_type != "skill":
            return (
                f"magnet adopt --apply currently supports change_type=skill "
                f"(got {change_type!r})"
            )
        prose = fit_description or prediction
        dest = apply_dest or default_apply_dest(root)
        applied_info = apply_skill_to_stack(
            source_stack,
            description,
            prose,
            dest=dest,
            repo_root=root,
        )
        probe_stack = applied_info["stack"]
        lines.append(
            f"  APPLIED    skills/{applied_info['slug']}/SKILL.md → {probe_stack}"
        )
        lines.append(f"  source     {source_stack}  (untouched)")

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

    # --apply measures a real stack mutation in the same sitting; do not invent a week
    # unless the caller explicitly kept simulate_next_week=True.
    rec = tool_record_week(
        probe_name,
        log_path=path,
        change_id=adoption["id"],
        simulate_next_week=simulate_next_week,
        stack_dir=probe_stack,
        repo_root=root,
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
    repro = (
        f"magnet adopt {change_type} {description!r} {prediction!r} "
        f"--probe {probe_name}"
    )
    if apply:
        repro += " --apply --no-simulate"
    receipt = render_receipt(
        probe_name,
        readings,
        direction="up",
        change_label=row["description"] if row else description,
        repro_command=repro,
    )
    if (
        change_type in STACK_CHANGE_TYPES
        and is_builtin_probe(probe_name)
        and probe_name != STACK_COVERAGE_PROBE
    ):
        # Say what the probe can see instead of printing a silent 0-delta.
        receipt += (
            f"\n  measures   repo only — {probe_name} reads this repo, not the stack; "
            f"a {change_type} change is invisible to it. Add a registry probe that "
            f"reads the stack (docs/probes.json.example) to measure this adoption."
        )
    parts = lines + [receipt]

    prose = fit_description or prediction
    fit_result = None
    if fit:
        surface = "agents" if change_type == "model" else "skills"
        # Fit against the SOURCE stack (pre-apply gaps) — that is the prediction.
        fit_result = fit_one(description, prose, source_stack, surface=surface)
        parts += ["", render_fit(fit_result)]

    if (
        not apply
        and probe_name == STACK_COVERAGE_PROBE
        and fit_result
        and fit_result["label"] == "fills-gap"
        and label == "unchanged"
    ):
        parts.append(
            "  note       fit predicts fills-gap but the skill was not written "
            "to the stack — pass --apply to measure coverage after the write"
        )

    return "\n".join(parts)
