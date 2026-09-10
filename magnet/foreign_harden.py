"""foreign-harden — apply Ultimate Guide hardening to stacks MAGNET did not build.

Closes the loop foreign-bind left open:
  1. Open a foreign stack (offline fixtures; optional live clones)
  2. BEFORE — naive_title=complete while hardening is near-zero (the lie)
  3. APPLY Ultimate Guide recommendations to a WORKING COPY (source untouched)
  4. AFTER  — magnet prints helped with value/pop; naive never measured a delta

guide-demo already applies UG to fixtures/stack. This command insists the source
is a stack we did not author, prints the before-lie, and keeps a naive arm that
invents helped from titles without opening SKILL.md or settings.json.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from magnet.foreign_bind import (
    BIND_MEASURES,
    OFFLINE_STACKS,
    _hardening_near_zero,
    measure_bind,
    resolve_offline,
)
from magnet.guide_demo import GUIDE_ROWS
from magnet.reporter import format_value_pop
from magnet.stack_bind import copy_stack


def resolve_targets(
    repo_root: str,
    stacks: list[str] | None = None,
) -> list[tuple[str, str]]:
    """Offline fixtures by default; --stack / MAGNET_FOREIGN_BIND for live clones."""
    if stacks:
        return [(os.path.expanduser(s), "cli --stack") for s in stacks]
    pairs = resolve_offline(repo_root)
    # Prefer the companion fixture first — we did not author its SKILL.md body.
    extra = os.environ.get("MAGNET_FOREIGN_BIND", "").strip()
    if extra:
        for part in extra.split(","):
            part = part.strip()
            if part and Path(part).is_dir():
                pairs.append((part, "MAGNET_FOREIGN_BIND"))
    return pairs


def _apply_measurable_rows(stack: str) -> list[dict]:
    """Apply each UG row that has a measurable population; return row results."""
    rows_out: list[dict] = []
    for row in GUIDE_ROWS:
        before = row["measure"](stack)
        pop = before.get("population") or 0
        if not pop:
            rows_out.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "probe": row["probe"],
                    "change_type": row["change_type"],
                    "before": before,
                    "after": before,
                    "magnet": "cannot-measure",
                    "naive": "helped",
                    "delta": None,
                    "touched": [],
                }
            )
            continue
        touched = row["apply"](stack)
        after = row["measure"](stack)
        # Local two-reading series for this probe (before + after).
        # Use an ephemeral connection per call site — caller records if needed.
        delta_val = None
        if before.get("value") is not None and after.get("value") is not None:
            delta_val = int(after["value"]) - int(before["value"])
        if delta_val is None:
            magnet_label = "baseline"
        elif delta_val > 0:
            magnet_label = "helped"
        elif delta_val < 0:
            magnet_label = "hurt"
        else:
            magnet_label = "unchanged"
        rows_out.append(
            {
                "id": row["id"],
                "title": row["title"],
                "probe": row["probe"],
                "change_type": row["change_type"],
                "before": before,
                "after": after,
                "magnet": magnet_label,
                "naive": "helped",  # title invents optimism — never opens object
                "delta": delta_val,
                "touched": touched,
            }
        )
    return rows_out


def harden_one(
    source: str,
    *,
    label: str = "",
    work_root: str | None = None,
) -> dict:
    """Copy source → apply UG → return before/after bind + per-row magnet verdicts."""
    before_bind = measure_bind(source)
    before_bind["label"] = label
    naive = before_bind["naive"]

    work = work_root or tempfile.mkdtemp(prefix="magnet-foreign-harden-")
    stack = copy_stack(source, os.path.join(work, "stack"))
    rows = _apply_measurable_rows(stack)
    after_bind = measure_bind(stack)
    after_bind["label"] = label

    moved = sum(1 for r in rows if r["magnet"] == "helped")
    cannot = sum(1 for r in rows if r["magnet"] == "cannot-measure")
    return {
        "source": source,
        "label": label,
        "working": stack,
        "naive": naive,
        "before": before_bind,
        "after": after_bind,
        "rows": rows,
        "moved": moved,
        "cannot": cannot,
        "before_near_zero": _hardening_near_zero(before_bind["probes"]),
        "after_near_zero": _hardening_near_zero(after_bind["probes"]),
    }


def render_foreign_harden(results: list[dict]) -> str:
    lines = [
        "MAGNET foreign-harden — Ultimate Guide apply on stacks we did not build",
        "",
        "  BEFORE  naive_title may say complete while bind probes are near-zero",
        "  APPLY   UG hardening on a temporary copy (source untouched)",
        "  AFTER   magnet prints helped with value/pop; naive invents helped from titles",
        "",
    ]
    findings = 0
    for result in results:
        naive = result["naive"]
        before_p = result["before"]["probes"]
        after_p = result["after"]["probes"]
        lines += [
            f"  STACK    {result['source']}",
            f"  label    {result.get('label', '')}",
            f"  working  {result['working']}  (temporary copy — source untouched)",
            f"  naive_title  {naive['verdict']}  ← {naive['note']}",
            "",
            "  probe                  before     after      magnet object",
            "  ---------------------  ---------  ---------  ------ ------",
        ]
        for name, _ in BIND_MEASURES:
            b = before_p[name]
            a = after_p[name]
            b_pop = b.get("population")
            a_pop = a.get("population")
            if not b_pop and not a_pop:
                bv, av = "n/a", "n/a"
                note = "object missing"
            else:
                bv = format_value_pop(b.get("value"), b_pop)
                av = format_value_pop(a.get("value"), a_pop)
                note = (a.get("detail") or b.get("detail") or {}).get("object", "")
            # Magnet label for the probe series (before→after on working copy).
            if not b_pop:
                mlabel = "cannot-measure"
            elif (a.get("value") or 0) > (b.get("value") or 0):
                mlabel = "helped"
            elif (a.get("value") or 0) < (b.get("value") or 0):
                mlabel = "hurt"
            else:
                mlabel = "unchanged"
            lines.append(
                f"  {name:<22} {bv:<10} {av:<10} {mlabel:<6} {note}"
            )

        lines += [
            "",
            "  UG row apply (naive invents helped from every title):",
            "  #   type     probe                 before   after    magnet         naive",
            "  --  -------- --------------------  -------  -------  -------------  ------",
        ]
        for i, row in enumerate(result["rows"], start=1):
            bv = format_value_pop(
                row["before"].get("value"), row["before"].get("population")
            )
            av = format_value_pop(
                row["after"].get("value"), row["after"].get("population")
            )
            lines.append(
                f"  {i:<3}{row['change_type']:<9}{row['probe']:<22}"
                f"{bv:<9}{av:<9}{row['magnet']:<15}{row['naive']}"
            )

        # FINDING: title said complete at near-zero, then apply moved the object.
        if (
            naive["verdict"] == "complete"
            and result["before_near_zero"]
            and result["moved"] >= 3
        ):
            findings += 1
            effort_b = before_p["effort-coverage"]
            effort_a = after_p["effort-coverage"]
            lines.append(
                f"  FINDING  naive_title=complete at hardening near-zero "
                f"(effort {format_value_pop(effort_b.get('value'), effort_b.get('population'))}); "
                f"after UG apply magnet moved={result['moved']}/5 "
                f"(effort {format_value_pop(effort_a.get('value'), effort_a.get('population'))}) "
                f"— title never measured the delta."
            )
        elif naive["verdict"] == "complete" and result["before_near_zero"]:
            findings += 1
            lines.append(
                f"  FINDING  naive_title=complete at near-zero, but only "
                f"moved={result['moved']}/5 after apply — product defect or missing objects."
            )
        elif result["moved"] >= 3:
            findings += 1
            lines.append(
                f"  FINDING  magnet moved={result['moved']}/5 on foreign stack; "
                f"naive still invents helped from titles without opening the object."
            )
        lines.append("")

    lines += [
        f"  findings   {findings}/{len(results)} stacks closed the title→apply→helped loop",
        f"  offline    {[rel for rel, _ in OFFLINE_STACKS]}",
        "  repro      magnet foreign-harden",
        "  repro      magnet foreign-harden --stack /path/to/clone",
        "  repro      bash scripts/foreign-stack.sh",
    ]
    if findings == 0 and results:
        lines.append(
            "  FINDING  no stack closed the foreign-harden loop — unexpected; "
            "re-check apply opens the object and hook control is not green-on-outage."
        )
    return "\n".join(lines)


def run_foreign_harden(
    *,
    repo_root: str | None = None,
    stacks: list[str] | None = None,
) -> str:
    root = repo_root or os.getcwd()
    pairs = resolve_targets(root, stacks)
    if not pairs:
        return (
            "MAGNET foreign-harden — no stacks found\n"
            "  tip: fixtures/stack · fixtures/real-stacks/agentgrinder\n"
            "  tip: MAGNET_FOREIGN_BIND=/tmp/anthropics-skills,/tmp/superpowers"
        )
    results = []
    for path, label in pairs:
        if not Path(path).is_dir():
            continue
        results.append(harden_one(path, label=label))
    if not results:
        return "MAGNET foreign-harden — no usable stack directories"
    return render_foreign_harden(results)
