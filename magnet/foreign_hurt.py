"""foreign-hurt — embarrassment arm: magnet hurt while naive invents helped.

Closes the honesty gap left by foreign-harden (which only shows helped):
  1. Harden a foreign working copy (UG apply) → magnet helped
  2. Strip effort:/allowed-tools (and optionally deny/hooks) → magnet hurt
  3. Naive invents helped from the strip TITLE ("simplify skill frontmatter")

A demo that can only print helped is a demo. This arm can print a result we
would not want on a marketing slide.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from magnet.foreign_bind import resolve_offline
from magnet.prediction import check_prediction
from magnet.reporter import format_value_pop
from magnet.stack_bind import (
    apply_allowed_tools_frontmatter,
    apply_deny_patterns,
    apply_effort_frontmatter,
    apply_hook_hardening,
    copy_stack,
    deny_coverage,
    effort_coverage,
    hook_coverage,
    strip_allowed_tools_frontmatter,
    strip_deny_patterns,
    strip_effort_frontmatter,
    strip_hook_hardening,
    tools_coverage,
)

# Rows that can hurt after a harden. Title is for the naive arm only.
HURT_ROWS = (
    {
        "id": "hurt-effort",
        "title": "simplify skill frontmatter (drop effort: fields)",
        "probe": "effort-coverage",
        "measure": effort_coverage,
        "harden": apply_effort_frontmatter,
        "strip": strip_effort_frontmatter,
    },
    {
        "id": "hurt-tools",
        "title": "streamline allowed-tools declarations",
        "probe": "tools-coverage",
        "measure": tools_coverage,
        "harden": apply_allowed_tools_frontmatter,
        "strip": strip_allowed_tools_frontmatter,
    },
    {
        "id": "hurt-deny",
        "title": "relax permissions.deny for developer velocity",
        "probe": "deny-coverage",
        "measure": deny_coverage,
        "harden": apply_deny_patterns,
        "strip": strip_deny_patterns,
    },
    {
        "id": "hurt-hook",
        "title": "remove noisy PreToolUse blocker hooks",
        "probe": "hook-coverage",
        "measure": hook_coverage,
        "harden": apply_hook_hardening,
        "strip": strip_hook_hardening,
    },
)


def _delta_label(before: dict, after: dict) -> str:
    pop = before.get("population") or 0
    if not pop:
        return "cannot-measure"
    b = before.get("value")
    a = after.get("value")
    if b is None or a is None:
        return "baseline"
    d = int(a) - int(b)
    if d > 0:
        return "helped"
    if d < 0:
        return "hurt"
    return "unchanged"


def hurt_one(source: str, *, label: str = "") -> dict:
    """Harden then strip on a working copy. Source untouched."""
    work = tempfile.mkdtemp(prefix="magnet-foreign-hurt-")
    stack = copy_stack(source, os.path.join(work, "stack"))
    rows_out: list[dict] = []
    naive_helped_on_hurt = 0
    magnet_hurt = 0

    for row in HURT_ROWS:
        before = row["measure"](stack)
        if not before.get("population"):
            rows_out.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "probe": row["probe"],
                    "before": before,
                    "hardened": before,
                    "after": before,
                    "harden_label": "cannot-measure",
                    "hurt_label": "cannot-measure",
                    "naive": "helped",
                    "prediction": check_prediction(row["title"], "baseline"),
                }
            )
            continue
        # Ensure there is something to strip — harden first if needed.
        if (before.get("value") or 0) < (before.get("population") or 0):
            row["harden"](stack)
        hardened = row["measure"](stack)
        harden_label = _delta_label(before, hardened)
        row["strip"](stack)
        after = row["measure"](stack)
        hurt_label = _delta_label(hardened, after)
        # Grade the strip TITLE as a prediction against magnet's hurt verdict.
        # Naive still invents helped; prediction-held means the title admitted fall.
        pred = check_prediction(row["title"], hurt_label)
        if hurt_label == "hurt":
            magnet_hurt += 1
            # Naive invents helped from the strip title every time.
            naive_helped_on_hurt += 1
        rows_out.append(
            {
                "id": row["id"],
                "title": row["title"],
                "probe": row["probe"],
                "before": before,
                "hardened": hardened,
                "after": after,
                "harden_label": harden_label,
                "hurt_label": hurt_label,
                "naive": "helped",
                "prediction": pred,
            }
        )

    return {
        "source": source,
        "label": label,
        "working": stack,
        "rows": rows_out,
        "magnet_hurt": magnet_hurt,
        "naive_helped_on_hurt": naive_helped_on_hurt,
    }


def render_foreign_hurt(results: list[dict]) -> str:
    lines = [
        "MAGNET foreign-hurt — strip hardening; naive invents helped from the title",
        "",
        "  HARDEN  UG apply on a temporary copy (so there is something to strip)",
        "  STRIP   remove effort/tools/deny/hook signals — magnet must print hurt",
        "  NAIVE   invents helped from every strip title without opening SKILL.md",
        "",
    ]
    findings = 0
    for result in results:
        lines += [
            f"  STACK    {result['source']}",
            f"  label    {result.get('label', '')}",
            f"  working  {result['working']}  (temporary copy — source untouched)",
            "",
            "  #   probe              before   hardened after    magnet-hurt  naive",
            "  --  -----------------  -------  -------- -------  -----------  ------",
        ]
        for i, row in enumerate(result["rows"], start=1):
            b = format_value_pop(row["before"].get("value"), row["before"].get("population"))
            h = format_value_pop(
                row["hardened"].get("value"), row["hardened"].get("population")
            )
            a = format_value_pop(row["after"].get("value"), row["after"].get("population"))
            lines.append(
                f"  {i:<3}{row['probe']:<19}{b:<9}{h:<9}{a:<9}"
                f"{row['hurt_label']:<13}{row['naive']}"
            )
        lines.append("")
        lines.append("  strip titles (naive=helped always; prediction grades the title):")
        held = 0
        graded = 0
        for row in result["rows"]:
            pred = row.get("prediction") or {}
            outcome = pred.get("outcome", "unmeasured")
            intent = pred.get("intent", "unknown")
            if row["hurt_label"] == "hurt":
                graded += 1
                if outcome == "prediction-held":
                    held += 1
            lines.append(
                f"    {row['id']:<12} naive={row['naive']:<8} "
                f"magnet={row['hurt_label']:<16} "
                f"pred={outcome:<20} intent={intent:<8}  {row['title']}"
            )

        if result["naive_helped_on_hurt"] >= 1 and result["magnet_hurt"] >= 1:
            findings += 1
            lines.append(
                f"  FINDING  naive invented helped on {result['naive_helped_on_hurt']}/"
                f"{result['magnet_hurt']} magnet-hurt rows — title is not the object."
            )
            if graded and held == graded:
                lines.append(
                    f"  FINDING  prediction-held on {held}/{graded} hurt rows "
                    f"(strip titles admit fall) while naive still invents helped."
                )
            elif graded:
                lines.append(
                    f"  note      prediction-held {held}/{graded} hurt rows "
                    f"(strip titles that lack fall intent stay no-direction)."
                )
        elif result["magnet_hurt"] == 0:
            lines.append(
                "  FINDING  magnet printed no hurt rows — strip did not open the "
                "object, or stack had nothing measurable to strip."
            )
            findings += 1  # still a finding (product defect signal)
        lines.append("")

    lines += [
        f"  findings   {findings}/{len(results)} stacks embarrassed naive-on-hurt",
        "  repro      magnet foreign-hurt",
        "  repro      magnet foreign-hurt --stack /path/to/clone",
        "  repro      magnet foreign-harden   # helped arm",
        "  repro      magnet probe hooks-layout --stack fixtures/real-stacks/superpowers-hooks",
    ]
    if findings == 0 and results:
        lines.append(
            "  FINDING  no stack embarrassed naive-on-hurt — unexpected; "
            "re-check strip opens SKILL.md / settings.json."
        )
    return "\n".join(lines)


def run_foreign_hurt(
    *,
    repo_root: str | None = None,
    stacks: list[str] | None = None,
) -> str:
    root = repo_root or os.getcwd()
    if stacks:
        pairs = [(os.path.expanduser(s), "cli --stack") for s in stacks]
    else:
        # Prefer stacks with skills so effort/tools can hurt. Skip hooks-only extract.
        pairs = [
            (p, lab)
            for p, lab in resolve_offline(root)
            if "superpowers-hooks" not in p
        ]
        extra = os.environ.get("MAGNET_FOREIGN_BIND", "").strip()
        if extra:
            for part in extra.split(","):
                part = part.strip()
                if part and Path(part).is_dir():
                    pairs.append((part, "MAGNET_FOREIGN_BIND"))
    if not pairs:
        return (
            "MAGNET foreign-hurt — no stacks found\n"
            "  tip: fixtures/stack · fixtures/real-stacks/agentgrinder"
        )
    results = [hurt_one(path, label=label) for path, label in pairs if Path(path).is_dir()]
    if not results:
        return "MAGNET foreign-hurt — no usable stack directories"
    return render_foreign_hurt(results)
