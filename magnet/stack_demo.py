"""`magnet stack-demo` — cold path that applies skills into a measured stack copy.

The embarrassing finding this exists to print: naive says `helped` when you adopt
wine-pairing noise; magnet says `unchanged` because stack-coverage did not move.

Goes to the real object (the stack filesystem), not demo-pass-rate + --demo-bonus.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from magnet.apply import apply_skill, copy_stack
from magnet.log import connect, list_readings, reset_demo
from magnet.probes import STACK_COVERAGE_PROBE
from magnet.reporter import verdict
from magnet.stack import default_stack_dir, fit_one, stack_coverage
from magnet.tools import tool_adopt_change, tool_record_week


FILLER_NAME = "pdb-navigator"
FILLER_DESC = (
    "Debug a failing test by driving pdb and bisecting the stack trace"
)
NOISE_NAME = "wine-pairing"
NOISE_DESC = "Suggest a wine to pair with dinner"
# Synonym-style: declares refactor, text supports it with extract/rename words
# so the declaration VERIFYIES and coverage can move without the word "refactor".
SYNONYM_NAME = "code-surgeon"
SYNONYM_DESC = (
    "Extract a method and rename identifiers until the module is simpler to read"
)
SYNONYM_CAPS = ["refactor"]
# Liar: declares security, text is flashcards — claimed must NOT buy coverage.
LIAR_NAME = "flashcard-guard"
LIAR_DESC = "Practise flashcards with spaced repetition"
LIAR_CAPS = ["security"]


def _naive_verdict(before: int | None, after: int | None) -> str:
    """Marketplace / two-hour arm: any adoption after a prior reading is 'helped'."""
    if before is None:
        return "baseline"
    return "helped"


def run_stack_demo(
    *,
    repo_root: str | None = None,
    log_path: str | None = None,
    work_dir: str | None = None,
) -> str:
    root = Path(repo_root or os.getcwd())
    src = default_stack_dir(str(root))
    work = Path(work_dir or (root / ".magnet" / "stack-demo-work"))
    log = log_path or str(root / ".magnet" / "stack-demo.db")

    copy_stack(src, str(work))
    os.makedirs(os.path.dirname(log) or ".", exist_ok=True)
    conn = connect(log)
    reset_demo(conn)

    lines: list[str] = [
        "MAGNET stack-demo — apply skills into a measured stack copy",
        "",
        f"  stack      {work}  (copy of {src})",
        f"  probe      {STACK_COVERAGE_PROBE}",
        "",
    ]

    base = tool_record_week(
        STACK_COVERAGE_PROBE, log_path=log, stack_dir=str(work)
    )
    base_val = base.get("value")
    base_pop = base.get("population")
    lines.append(
        f"  baseline   {base_val}/{base_pop}  verdict={base['verdict']}"
    )
    lines.append("")

    # --- A: filler that names an uncovered cap ---
    a = _apply_and_measure(
        log,
        str(work),
        FILLER_NAME,
        FILLER_DESC,
        prediction="coverage rises — debug gap fills",
        capabilities=None,
    )
    lines += [
        "=== A · apply filler that names an uncovered capability ===",
        f"  applied    {FILLER_NAME}",
        f"  fit        {a['fit']['label']}  fills={','.join(a['fit']['fills']) or '—'}",
        f"  coverage   {a['before']}/{base_pop} → {a['after']}/{base_pop}",
        f"  magnet     {a['magnet']}",
        f"  naive      {a['naive']}  ← any adopt after a baseline is helped",
        "",
    ]

    # --- B: noise that fills nothing ---
    mid = a["after"]
    b = _apply_and_measure(
        log,
        str(work),
        NOISE_NAME,
        NOISE_DESC,
        prediction="no coverage change expected",
        capabilities=None,
    )
    lines += [
        "=== B · apply noise (embarrassing case for naive) ===",
        f"  applied    {NOISE_NAME}",
        f"  fit        {b['fit']['label']}",
        f"  coverage   {b['before']}/{base_pop} → {b['after']}/{base_pop}",
        f"  magnet     {b['magnet']}",
        f"  naive      {b['naive']}  ← invents optimism on noise",
        "",
    ]

    # --- C: verified declaration covers a cap without the vocab word ---
    c = _apply_and_measure(
        log,
        str(work),
        SYNONYM_NAME,
        SYNONYM_DESC,
        prediction="refactor coverage rises via verified declaration",
        capabilities=SYNONYM_CAPS,
    )
    lines += [
        "=== C · apply synonym with verified capabilities: [refactor] ===",
        f"  applied    {SYNONYM_NAME}",
        f"  fit        {c['fit']['label']}  fills={','.join(c['fit']['fills']) or '—'}",
        f"  coverage   {c['before']}/{base_pop} → {c['after']}/{base_pop}",
        f"  magnet     {c['magnet']}",
        f"  naive      {c['naive']}",
        "",
    ]

    # --- D: claimed declaration must NOT buy coverage ---
    d = _apply_and_measure(
        log,
        str(work),
        LIAR_NAME,
        LIAR_DESC,
        prediction="security must NOT rise on a claimed-only tag",
        capabilities=LIAR_CAPS,
    )
    cov = stack_coverage(str(work))
    lines += [
        "=== D · apply liar (capabilities: [security], text is flashcards) ===",
        f"  applied    {LIAR_NAME}",
        f"  fit        {d['fit']['label']}",
        f"  coverage   {d['before']}/{base_pop} → {d['after']}/{base_pop}",
        f"  magnet     {d['magnet']}",
        f"  naive      {d['naive']}  ← would call this helped",
        f"  claimed    {', '.join(cov['detail'].get('claimed_only') or []) or '—'}",
        f"  note       claimed (unsupported) declarations never buy coverage",
        "",
    ]

    lines += [
        "FINDING  magnet refuses helped when coverage did not move (B, D).",
        "FINDING  naive helped on wine-pairing and flashcard-guard — marketplace failure.",
        "FINDING  apply moves the real object: extract/rename text covers refactor (C).",
        "FINDING  claimed capabilities never buy coverage (D) — EXP-MAGNET-01 honesty.",
        "",
        f"  final      {cov['value']}/{cov['population']}  "
        f"uncovered={', '.join(cov['detail']['uncovered'])}",
        "  repro      magnet stack-demo",
    ]

    # Keep the work copy for inspection; stranger can rm -rf .magnet/stack-demo-work
    return "\n".join(lines)


def _apply_and_measure(
    log: str,
    stack: str,
    name: str,
    description: str,
    *,
    prediction: str,
    capabilities: list[str] | None,
) -> dict:
    before_reading = stack_coverage(stack)
    before = before_reading["value"]
    fit = fit_one(
        name,
        description,
        stack,
        capabilities=capabilities,
    )
    apply_skill(stack, name, description, capabilities=capabilities)
    adoption = tool_adopt_change(
        "skill",
        name,
        prediction,
        STACK_COVERAGE_PROBE,
        log_path=log,
    )
    rec = tool_record_week(
        STACK_COVERAGE_PROBE,
        log_path=log,
        change_id=adoption["id"],
        simulate_next_week=True,
        stack_dir=stack,
    )
    after = rec.get("value")
    magnet = rec["verdict"]
    naive = _naive_verdict(before, after)
    return {
        "before": before,
        "after": after,
        "magnet": magnet,
        "naive": naive,
        "fit": fit,
        "readings": list_readings(connect(log), STACK_COVERAGE_PROBE),
    }


def cleanup_stack_demo(repo_root: str | None = None) -> None:
    root = Path(repo_root or os.getcwd())
    work = root / ".magnet" / "stack-demo-work"
    if work.exists():
        shutil.rmtree(work)
