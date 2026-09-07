"""Measure a stack MAGNET did not author — inventory + coverage + naive arm.

Numbers are re-derived at the object. A title-only scanner that sees
"Agent Skills" / "superpowers" invents a pass; MAGNET opens every SKILL.md.
"""
from __future__ import annotations

import os
from pathlib import Path

from magnet.stack import (
    TAG_VOCAB_VERSION,
    fit_one,
    gaps,
    inventory,
    stack_coverage,
)


def naive_title_verdict(stack_dir: str) -> dict:
    """Two-hour marketplace arm: README mentions skills → invents complete.

    Does not open SKILL.md files. Exists so we can lose to it when the title
    looks finished and the object is not.
    """
    root = Path(os.path.expanduser(stack_dir))
    blob = ""
    for name in ("README.md", "README", "CLAUDE.md", "AGENTS.md"):
        path = root / name
        if path.is_file():
            try:
                blob += path.read_text(encoding="utf-8", errors="replace")[:8000]
            except OSError:
                pass
    low = blob.lower()
    looks_complete = any(
        w in low for w in ("agent skills", "skills framework", "superpowers", "skill.md")
    ) or (root / "skills").is_dir()
    return {
        "arm": "naive_title",
        "verdict": "complete" if looks_complete else "unknown",
        "opened_skill_md": False,
        "note": "title/README only — never opens SKILL.md",
    }


# Candidates aimed at common gaps — plus wine noise. Fit is against THEIR gaps.
FOREIGN_FIT_CASES = (
    ("sql-migrator", "SQL dataframe ETL schema migration for the warehouse"),
    ("secrets-gate", "Block credential and secret leaks; sandbox injection attacks"),
    ("plan-slicer", "Decompose a roadmap into slices of work"),
    ("code-reviewer", "Review and critique a pull request; lint the diff"),
    (
        "pdb-navigator",
        "Debug a failing test by driving pdb and bisecting the stack trace",
    ),
    ("wine-pairing", "Suggest a wine to pair with dinner"),
)


def measure_external_stack(stack_dir: str) -> dict:
    """Open the stack object. Return inventory, coverage, naive arm, fit rows."""
    stack = os.path.expanduser(stack_dir)
    inv = inventory(stack)
    g = gaps(inv)
    cov = stack_coverage(stack)
    naive = naive_title_verdict(stack)
    fits = []
    for name, desc in FOREIGN_FIT_CASES:
        fits.append(fit_one(name, desc, stack))
    return {
        "stack": stack,
        "tag_vocab_version": TAG_VOCAB_VERSION,
        "inventory": inv,
        "gaps": g,
        "coverage": cov,
        "naive": naive,
        "fits": fits,
    }


def render_external(result: dict) -> str:
    inv = result["inventory"]
    g = result["gaps"]
    cov = result["coverage"]
    naive = result["naive"]
    lines = [
        "MAGNET external-stack — measure a stack you did not build",
        "",
        f"  stack      {result['stack']}",
        f"  tag_vocab  {result['tag_vocab_version']}",
        f"  inventory  {g['counts']['skills']} skills · "
        f"{g['counts']['commands']} commands · "
        f"{g['counts']['agents']} agents · "
        f"{g['counts']['hooks']} hooks",
        f"  empty      {', '.join(g['empty_surfaces']) or '(none)'}",
        f"  uncovered  {', '.join(g['uncovered']) or '(none)'}",
        f"  coverage   {cov['value']}/{cov['population']}",
        f"  command    {cov['command']}",
        "",
        f"  naive_title  {naive['verdict']}  ← {naive['note']}",
        f"  magnet       {cov['value']}/{cov['population']}  ← opened every SKILL.md",
        "",
    ]
    if not inv.get("present"):
        lines.append("  FINDING    stack path has no enumerable surfaces")
    elif naive["verdict"] == "complete" and cov["value"] < cov["population"]:
        lines.append(
            f"  FINDING    naive_title says complete; magnet prints "
            f"{cov['value']}/{cov['population']} — title is not the object."
        )
    lines.append("")
    lines.append("  FIT against THEIR gaps (not fixtures/stack):")
    for f in result["fits"]:
        fills = ",".join(f["fills"]) if f["fills"] else "—"
        lines.append(
            f"    {f['label']:<12} {f['name']:<16} fills={fills}"
        )
    lines += [
        "",
        "  repro      magnet external-stack --stack " + result["stack"],
        "  repro      bash scripts/foreign-stack.sh",
    ]
    return "\n".join(lines)
