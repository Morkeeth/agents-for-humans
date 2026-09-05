"""Apply-eval — naive-fit vs magnet vs silent_null on real stack applies.

naive_fit believes the fit label without opening the stack object:
  fills-gap → helped, anything else → unchanged.
magnet re-probes coverage after optional --apply and uses the measured verdict.
silent_null always says baseline.

The embarrassment case is required: fit can say fills-gap while coverage stays
flat when the skill was never written. If magnet invents helped there, we lose.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

from magnet.apply import apply_skill_to_stack
from magnet.reporter import verdict
from magnet.stack import default_stack_dir, fit_one, stack_coverage

VerdictLabel = Literal["baseline", "helped", "hurt", "unchanged"]


@dataclass(frozen=True)
class ApplyScenario:
    name: str
    skill: str
    prose: str
    do_apply: bool
    truth: VerdictLabel
    note: str = ""


SCENARIOS: tuple[ApplyScenario, ...] = (
    ApplyScenario(
        "apply_fills_security",
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
        True,
        "helped",
        note="writing the skill must move coverage",
    ),
    ApplyScenario(
        "apply_noise_wine",
        "wine-pairing",
        "suggest a bottle for dinner",
        True,
        "unchanged",
        note="noise must not raise coverage",
    ),
    ApplyScenario(
        "fit_without_apply",
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
        False,
        "unchanged",
        note="fit fills-gap is not a measured trend",
    ),
)


def naive_fit_verdict(fit_label: str, _readings: list[dict]) -> str:
    """Marketplace failure mode: trust the ranking label, skip the probe."""
    if fit_label == "fills-gap":
        return "helped"
    if fit_label == "duplicate":
        return "unchanged"
    return "unchanged"


def silent_null_verdict(_readings: list[dict]) -> str:
    return "baseline"


def _run_scenario(
    sc: ApplyScenario,
    *,
    source_stack: str,
    work_root: Path,
) -> dict:
    fit = fit_one(sc.skill, sc.prose, source_stack)
    before = stack_coverage(source_stack)
    readings = [
        {
            "value": before["value"],
            "population": before["population"],
        }
    ]
    if sc.do_apply:
        dest = work_root / sc.name
        applied = apply_skill_to_stack(
            source_stack, sc.skill, sc.prose, dest=str(dest)
        )
        after = stack_coverage(applied["stack"])
    else:
        after = stack_coverage(source_stack)
    readings.append(
        {
            "value": after["value"],
            "population": after["population"],
        }
    )
    magnet_label, delta = verdict(readings, direction="up")
    return {
        "name": sc.name,
        "truth": sc.truth,
        "fit_label": fit["label"],
        "fills": fit["fills"],
        "readings": readings,
        "magnet": magnet_label,
        "naive_fit": naive_fit_verdict(fit["label"], readings),
        "silent_null": silent_null_verdict(readings),
        "delta": delta,
        "note": sc.note,
    }


def _score(rows: list[dict], arm: str) -> dict:
    correct = sum(1 for r in rows if r[arm] == r["truth"])
    return {"correct": correct, "total": len(rows), "arm": arm}


def score_arms(
    *,
    repo_root: str | None = None,
    stack_dir: str | None = None,
) -> dict[str, dict]:
    rows = _collect(repo_root=repo_root, stack_dir=stack_dir)
    return {
        "naive_fit": _score(rows, "naive_fit"),
        "magnet": _score(rows, "magnet"),
        "silent_null": _score(rows, "silent_null"),
    }


def _collect(
    *,
    repo_root: str | None = None,
    stack_dir: str | None = None,
) -> list[dict]:
    root = repo_root or os.getcwd()
    source = stack_dir or default_stack_dir(root)
    rows: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="magnet-apply-eval-") as tmp:
        work = Path(tmp)
        for sc in SCENARIOS:
            rows.append(_run_scenario(sc, source_stack=source, work_root=work))
    return rows


def run_apply_eval(
    *,
    repo_root: str | None = None,
    stack_dir: str | None = None,
) -> str:
    rows = _collect(repo_root=repo_root, stack_dir=stack_dir)
    lines = [
        "MAGNET apply-eval — arms scored on real stack applies",
        "",
        "  scenario              truth      naive_fit  magnet   silent_null",
        "  " + "-" * 66,
    ]
    for r in rows:
        lines.append(
            f"  {r['name']:<22} {r['truth']:<10} "
            f"{r['naive_fit']:<10} {r['magnet']:<8} {r['silent_null']}"
        )

    lines += ["", "  arm scores (correct / total):", ""]
    scores = {
        "naive_fit": _score(rows, "naive_fit"),
        "magnet": _score(rows, "magnet"),
        "silent_null": _score(rows, "silent_null"),
    }
    best_name, best_score = "", -1
    for arm_name, sc in scores.items():
        lines.append(f"  {arm_name:<12} {sc['correct']}/{sc['total']}")
        for r in rows:
            ok = r[arm_name] == r["truth"]
            mark = "✓" if ok else "✗"
            lines.append(
                f"    {mark} {r['name']:<22} truth={r['truth']:<10} got={r[arm_name]}"
            )
        lines.append("")
        if sc["correct"] > best_score:
            best_score = sc["correct"]
            best_name = arm_name

    # Detail the embarrassment case so the finding is visible without reading code.
    fit_row = next(r for r in rows if r["name"] == "fit_without_apply")
    lines.append(
        f"  FINDING  fit_without_apply: fit={fit_row['fit_label']} "
        f"fills={fit_row['fills'] or '[]'} but coverage "
        f"{fit_row['readings'][0]['value']}/{fit_row['readings'][0]['population']} "
        f"→ {fit_row['readings'][1]['value']}/{fit_row['readings'][1]['population']} "
        f"(naive_fit={fit_row['naive_fit']}, magnet={fit_row['magnet']})"
    )
    lines.append(f"  best arm     {best_name} ({best_score}/{len(rows)})")
    lines.append("")
    lines.append("  repro        magnet apply-eval")
    return "\n".join(lines)
