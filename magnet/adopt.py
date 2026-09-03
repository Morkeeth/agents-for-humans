"""`magnet adopt` — record a change, re-run probe, print receipt."""
from __future__ import annotations

import os

from magnet.apply import apply_skill
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
    capabilities: list[str] | None = None,
) -> str:
    """Core loop: adopt change → (optional apply to stack) → re-probe → receipt.

    `--apply` writes a skill into the measured stack so stack-coverage can move.
    Without it, fit can say fills-gap while coverage stays unchanged — the defect
    found 2026-09-03 by running adopt --fit --probe stack-coverage.
    """
    path = log_path or os.path.join(os.getcwd(), ".magnet", "log.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = connect(path)
    if reset:
        reset_demo(conn)

    stack = stack_dir or default_stack_dir()
    # Prefer an explicit prose description for fit/apply; fall back to prediction.
    prose = fit_description or prediction

    lines = ["MAGNET adopt", ""]

    # Baseline reading if none exists yet
    prior = list_readings(conn, probe_name)
    if not prior:
        base = tool_record_week(probe_name, log_path=path, stack_dir=stack)
        lines.append(f"  baseline   verdict={base['verdict']}  readings={base['readings']}")

    # Fit BEFORE apply — otherwise the skill scores as a duplicate of itself
    # (found running adopt --apply --fit: label=duplicate at 100% self-overlap).
    fit_result = None
    if fit:
        surface = "agents" if change_type == "model" else "skills"
        fit_result = fit_one(
            description,
            prose,
            stack,
            surface=surface,
            capabilities=capabilities,
        )

    applied = None
    if apply:
        if change_type != "skill":
            lines.append(
                f"  apply      SKIPPED — --apply only writes skills "
                f"(got change_type={change_type})"
            )
        else:
            applied = apply_skill(
                stack,
                description,
                prose,
                capabilities=capabilities,
            )
            lines.append(f"  applied    {applied['path']}")
            if applied["capabilities"]:
                lines.append(f"  caps       {', '.join(applied['capabilities'])}")

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
        stack_dir=stack,
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
        repro_command=(
            f"magnet adopt {change_type} {description!r} {prediction!r} "
            f"--probe {probe_name}"
            + (" --apply" if apply else "")
        ),
    )
    # Only hook/setting are invisible to repo-only builtins. stack-coverage
    # opens the stack — do not print the "measures repo only" lie for it.
    if (
        change_type in STACK_CHANGE_TYPES
        and is_builtin_probe(probe_name)
        and probe_name != STACK_COVERAGE_PROBE
    ):
        receipt += (
            f"\n  measures   repo only — {probe_name} reads this repo, not the stack; "
            f"a {change_type} change is invisible to it. Add a registry probe that "
            f"reads the stack (docs/probes.json.example) to measure this adoption."
        )
    parts = lines + [receipt]

    if fit_result is not None:
        parts += ["", render_fit(fit_result)]

    # Honesty: fit predicted a fill but coverage did not move because nothing
    # was written into the stack the probe opens.
    if (
        fit_result
        and fit_result["label"] == "fills-gap"
        and not apply
        and probe_name == STACK_COVERAGE_PROBE
        and label in ("unchanged", "baseline")
    ):
        parts += [
            "",
            "  NOTE: fit predicted fills-gap but the stack filesystem was not "
            "modified — coverage cannot move. Re-run with --apply to write the "
            "skill into the measured stack.",
        ]

    return "\n".join(parts)
