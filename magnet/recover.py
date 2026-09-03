"""Recover demo — open the independent-stack loss at its object, then fix the cause.

Found by running `magnet bakeoff --stack fixtures/stack-cursor`:
  magnet top-20 admitted 18 noise items. Every one filled exactly one of
  {planning, writing, design} ("plan a wedding", "draft a listing",
  "colour palette"). Covering those three caps on a temp copy of the same
  stack lifts magnet from LOST (0.25) to WIN (0.625) with 0 noise.

This module re-derives that diagnosis every run. It does not invent a win
on the thin stack — both arms are printed.
"""
from __future__ import annotations

import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path

from magnet.bakeoff import (
    PLANTED,
    _kind_of,
    arm_magnet,
    build_flood,
    render_bakeoff,
    run_bakeoff,
)
from magnet.replicate import INDEPENDENT_STACK
from magnet.stack import gaps, inventory, rank

# Caps that the seeded noise domains actually hit on a thin stack.
# Re-derived: do not edit without re-running diagnose_noise_caps().
NOISE_ATTRACTING_CAPS = ("planning", "writing", "design")

COVER_SKILLS = (
    (
        "plan-slicer",
        "Plan and decompose a roadmap into slices for the week",
    ),
    (
        "writing-coach",
        "Writing rules for draft email prose and copy with a reader",
    ),
    (
        "visual-taste",
        "Design UI with visual typography and colour palette taste",
    ),
)


def diagnose_noise_caps(
    *,
    stack_dir: str,
    noise_n: int = 200,
    top_k: int = 20,
) -> dict:
    """Which capabilities do noise items in magnet's top-k actually fill?"""
    inv = inventory(stack_dir)
    g = gaps(inv)
    flood = build_flood(noise_n=noise_n)
    top = arm_magnet(flood, inv, g, top_k)
    scored = rank(flood, inv, g, top=len(flood))
    byname = {r["name"]: r for r in scored["all_rows"]}
    cap_hits: Counter = Counter()
    noise_rows = []
    for name in top:
        if _kind_of(name) != "noise":
            continue
        row = byname[name]
        for cap in row["fills"]:
            cap_hits[cap] += 1
        noise_rows.append(
            {
                "name": name,
                "score": row["score"],
                "fills": list(row["fills"]),
                "description": next(
                    (c["description"] for c in flood if c["name"] == name),
                    "",
                ),
            }
        )
    return {
        "stack": stack_dir,
        "uncovered": list(g["uncovered"]),
        "empty_surfaces": list(g["empty_surfaces"]),
        "noise_in_top": len(noise_rows),
        "cap_hits": dict(cap_hits),
        "noise_rows": noise_rows,
        "magnet_top": top,
    }


def _cover_noise_caps(stack_dir: str, dest: str) -> list[str]:
    """Copy stack and install skills that cover NOISE_ATTRACTING_CAPS."""
    shutil.copytree(stack_dir, dest)
    installed = []
    for name, desc in COVER_SKILLS:
        skill_dir = Path(dest) / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        safe = desc.replace("\\", "\\\\").replace('"', '\\"')
        (skill_dir / "SKILL.md").write_text(
            f'---\nname: {name}\ndescription: "{safe}"\n---\n\n# {name}\n',
            encoding="utf-8",
        )
        installed.append(name)
    return installed


def run_recover(
    *,
    repo_root: str | None = None,
    stack_rel: str = INDEPENDENT_STACK,
    noise_n: int = 200,
) -> dict:
    root = repo_root or os.getcwd()
    thin = str(Path(root) / stack_rel)
    if not Path(thin).is_dir():
        raise FileNotFoundError(f"independent stack missing: {thin}")

    diagnosis = diagnose_noise_caps(stack_dir=thin, noise_n=noise_n)
    before = run_bakeoff(
        stack_dir=thin, repo_root=root, noise_n=noise_n, write_candidates=False
    )

    with tempfile.TemporaryDirectory(prefix="magnet-recover-") as tmp:
        covered = str(Path(tmp) / "stack")
        installed = _cover_noise_caps(thin, covered)
        after_diag = diagnose_noise_caps(stack_dir=covered, noise_n=noise_n)
        after = run_bakeoff(
            stack_dir=covered,
            repo_root=root,
            noise_n=noise_n,
            write_candidates=False,
        )

    before_m = before["arms"]["magnet"]["recall_at_k"]
    before_n = before["arms"]["naive_stars"]["recall_at_k"]
    after_m = after["arms"]["magnet"]["recall_at_k"]
    after_n = after["arms"]["naive_stars"]["recall_at_k"]

    return {
        "stack": thin,
        "installed": installed,
        "noise_attracting_caps": list(NOISE_ATTRACTING_CAPS),
        "diagnosis": diagnosis,
        "after_diagnosis": after_diag,
        "before": before,
        "after": after,
        "thin_lost": before_m < before_n,
        "covered_wins": after_m > after_n,
        "covered_noise_zero": after["arms"]["magnet"]["noise_in_top"] == 0,
        "wine_liar_ok": (
            not before["wine_liar_in_magnet_primary"]
            and not after["wine_liar_in_magnet_primary"]
        ),
        "token_cost": 0,
    }


def render_recover(result: dict) -> str:
    d = result["diagnosis"]
    b, a = result["before"], result["after"]
    lines = [
        "MAGNET recover — open the independent-stack loss, then cover its cause",
        "",
        f"  thin stack   {result['stack']}",
        f"  diagnosis    {d['noise_in_top']} noise in magnet top-20 fill: "
        f"{d['cap_hits'] or '(none)'}",
        f"  cause caps   {', '.join(result['noise_attracting_caps'])}",
        f"  installed    {', '.join(result['installed'])}  (temp copy only)",
        "",
        "  phase       magnet  naive_stars  best         noise",
        "  " + "-" * 58,
    ]
    for label, r in (("thin", b), ("covered", a)):
        m = r["arms"]["magnet"]
        n = r["arms"]["naive_stars"]
        lines.append(
            f"  {label:<10} {m['recall_at_k']:<7} {n['recall_at_k']:<12} "
            f"{r['best_arm']:<12} {m['noise_in_top']}"
        )

    lines += ["", "  FINDINGS"]
    if result["thin_lost"]:
        lines.append(
            "    · THIN: magnet LOST — noise naming uncovered caps flooded top-k"
        )
    else:
        lines.append("    · THIN: magnet did not lose (unexpected on this fixture)")

    if result["covered_wins"] and result["covered_noise_zero"]:
        lines.append(
            "    · COVERED: magnet WINS with 0 noise after covering "
            f"{', '.join(result['noise_attracting_caps'])}"
        )
    elif result["covered_wins"]:
        lines.append(
            "    · COVERED: magnet wins but still admits "
            f"{a['arms']['magnet']['noise_in_top']} noise"
        )
    else:
        lines.append(
            "    · COVERED: magnet still does not beat naive_stars — investigate"
        )

    # Sample three noise descriptions that caused the thin loss
    samples = d["noise_rows"][:3]
    if samples:
        lines.append("    · sample noise that entered thin top-20:")
        for row in samples:
            lines.append(
                f"        {row['name']}: fills={row['fills']}  "
                f"\"{row['description'][:50]}\""
            )

    lines += [
        "",
        f"  wine-liar quarantined   {result['wine_liar_ok']}  (must be True)",
        f"  tokens                  {result['token_cost']}",
        "",
        "  repro      magnet recover",
    ]
    return "\n".join(lines)


def recover_exit_code(result: dict) -> int:
    """RED if wine-liar escapes, or if the covered arm fails to beat naive."""
    if not result["wine_liar_ok"]:
        return 1
    if not result["covered_wins"]:
        return 1
    if not result["covered_noise_zero"]:
        return 1
    return 0
