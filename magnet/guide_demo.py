"""guide-demo — Ultimate Guide closed loop (embarrassment arm).

Applies all five Ultimate Guide recommendations from
docs/ULTIMATE-GUIDE-MAGNET-2026-09-02.md to a TEMPORARY copy of fixtures/stack,
then prints the 5-row verdict table the audit could not:

  repo-blind   check-docs (THIS repo — cannot see stack changes)
  stack-bind   effort / deny / tools / hook / prompt probes (open the object)
  naive        invents "helped" from each recommendation TITLE

If the 2026-09-02 audit printed cannot-measure five times, this demo must show
magnet moving on the four stack-bound items (and prompt-consistency once the
CLAUDE.md object exists in the fixture). A title-only arm that helps on every
row is the marketplace failure mode.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from magnet.log import connect, list_readings, record_reading, reset_demo
from magnet.probes import run_check_docs_probe
from magnet.reporter import format_value_pop, verdict
from magnet.stack import default_stack_dir
from magnet.stack_bind import (
    DENY_PROBE,
    EFFORT_PROBE,
    HOOK_PROBE,
    PROMPT_PROBE,
    TOOLS_PROBE,
    apply_allowed_tools_frontmatter,
    apply_deny_patterns,
    apply_effort_frontmatter,
    apply_hook_hardening,
    apply_prompt_consistency,
    copy_stack,
    deny_coverage,
    effort_coverage,
    hook_coverage,
    prompt_consistency,
    tools_coverage,
)

# Ultimate Guide rows — probe opens the object named in `object`.
# Never ranked by the recommendation title.
GUIDE_ROWS = (
    {
        "id": "ug-1",
        "title": "permissions.deny for .env/.pem/.key/credentials",
        "probe": DENY_PROBE,
        "measure": deny_coverage,
        "apply": lambda stack: apply_deny_patterns(stack),
        "change_type": "setting",
    },
    {
        "id": "ug-2",
        "title": "effort: frontmatter on every SKILL.md",
        "probe": EFFORT_PROBE,
        "measure": effort_coverage,
        "apply": lambda stack: apply_effort_frontmatter(stack),
        "change_type": "skill",
    },
    {
        "id": "ug-3",
        "title": "allowed-tools: frontmatter on every SKILL.md",
        "probe": TOOLS_PROBE,
        "measure": tools_coverage,
        "apply": lambda stack: apply_allowed_tools_frontmatter(stack),
        "change_type": "skill",
    },
    {
        "id": "ug-4",
        "title": "align post-compact-reinject.txt with CLAUDE.md",
        "probe": PROMPT_PROBE,
        "measure": prompt_consistency,
        "apply": lambda stack: apply_prompt_consistency(stack),
        "change_type": "prompt",
    },
    {
        "id": "ug-5",
        "title": "remove Bash(rm -rf *); add dangerous-actions-blocker.sh",
        "probe": HOOK_PROBE,
        "measure": hook_coverage,
        "apply": lambda stack: apply_hook_hardening(stack),
        "change_type": "hook",
    },
)


def run_guide_demo(
    *,
    repo_root: str | None = None,
    stack_dir: str | None = None,
    log_path: str | None = None,
) -> str:
    root = Path(repo_root or os.getcwd())
    source = stack_dir or default_stack_dir(str(root))
    if not Path(source).is_dir():
        return f"MAGNET guide-demo — no stack at {source}\n  tip: fixtures/stack"

    work = tempfile.mkdtemp(prefix="magnet-guide-")
    stack = copy_stack(source, os.path.join(work, "stack"))
    db = log_path or os.path.join(work, "guide.db")
    conn = connect(db)
    reset_demo(conn)

    lines = [
        "MAGNET guide-demo — Ultimate Guide recommendations, measured",
        "",
        f"  source     {source}",
        f"  working    {stack}  (temporary copy — source untouched)",
        f"  log        {db}",
        f"  audit      docs/ULTIMATE-GUIDE-MAGNET-2026-09-02.md",
        "",
        "  #   change_type  probe                 before   after    magnet      naive",
        "  --  ------------  --------------------  -------  -------  ----------  ------",
    ]

    before_repo = run_check_docs_probe(str(root))
    record_reading(
        conn,
        before_repo["probe_name"],
        before_repo.get("value"),
        before_repo["command"],
        population=before_repo.get("population"),
    )

    moved = 0
    cannot = 0
    rows_out: list[dict] = []

    for i, row in enumerate(GUIDE_ROWS, start=1):
        before = row["measure"](stack)
        record_reading(
            conn,
            before["probe_name"],
            before.get("value"),
            before["command"],
            population=before.get("population"),
            change_id=i * 10,
        )

        # Population 0 means the object is missing — honest cannot-measure.
        if not before.get("population"):
            magnet_label = "cannot-measure"
            cannot += 1
            after = before
            naive = "helped"  # title invents optimism anyway
            delta = None
        else:
            row["apply"](stack)
            after = row["measure"](stack)
            record_reading(
                conn,
                after["probe_name"],
                after.get("value"),
                after["command"],
                population=after.get("population"),
                change_id=i * 10 + 1,
            )
            readings = list_readings(conn, row["probe"])
            magnet_label, delta = verdict(readings, direction="up")
            naive = "helped"  # every UG title sounds like a win
            if magnet_label == "helped":
                moved += 1
            elif magnet_label == "baseline" and (
                before.get("value") == after.get("value")
            ):
                # Applied but nothing moved — still a product defect signal.
                cannot += 1

        before_s = format_value_pop(before.get("value"), before.get("population"))
        after_s = format_value_pop(after.get("value"), after.get("population"))
        # format_value_pop returns "n/a" when population is 0 — pad labels so
        # "cannot-measure" never concatenates into "cannot-measurehelped".
        lines.append(
            f"  {i:<3}{row['change_type']:<14}{row['probe']:<22}"
            f"{before_s:<9}{after_s:<9}{magnet_label:<14}{naive}"
        )
        rows_out.append(
            {
                "id": row["id"],
                "title": row["title"],
                "magnet": magnet_label,
                "naive": naive,
                "delta": delta,
            }
        )

    after_repo = run_check_docs_probe(str(root))
    record_reading(
        conn,
        after_repo["probe_name"],
        after_repo.get("value"),
        after_repo["command"],
        population=after_repo.get("population"),
        change_id=99,
    )
    repo_readings = list_readings(conn, "check-docs")
    repo_label, repo_delta = verdict(repo_readings, direction="up")

    lines += [
        "",
        "  REPO-BLIND CONTROL",
        f"    check-docs   before {format_value_pop(before_repo.get('value'), before_repo.get('population'))}"
        f"  after {format_value_pop(after_repo.get('value'), after_repo.get('population'))}"
        f"  → {repo_label}  Δ {repo_delta if repo_delta is not None else '—'}",
        "",
        "  NAIVE ARM  invents helped from every recommendation title without opening the stack",
        f"  MAGNET     moved={moved}/{len(GUIDE_ROWS)}  cannot-measure={cannot}/{len(GUIDE_ROWS)}",
        "",
    ]

    repo_blind = repo_label in ("unchanged", "baseline") or (repo_delta == 0)
    if repo_blind and moved >= 4:
        finding = (
            "FINDING  repo-blind check-docs stayed flat while "
            f"{moved}/5 Ultimate Guide stack-bind probes moved. "
            "The 2026-09-02 audit printed cannot-measure five times because "
            "pytest could not see the stack — guide-demo opens the object."
        )
    elif moved >= 4:
        finding = (
            "FINDING  stack-bind probes moved, but repo-blind also moved — "
            "re-check whether check_docs accidentally reads the temp stack."
        )
    else:
        finding = (
            f"FINDING  only {moved}/5 guide probes moved after apply. "
            "This is a product defect — guide-demo must fail loud."
        )

    lines += [
        f"  {finding}",
        "",
        "  per-row titles (for the naive arm — NOT used to rank):",
    ]
    for r in rows_out:
        lines.append(f"    {r['id']}  naive={r['naive']:<8} magnet={r['magnet']:<16}  {r['title']}")

    lines += [
        "",
        "  repro      magnet guide-demo",
        f"  repro      magnet probe {EFFORT_PROBE} --stack {source}",
        f"  repro      magnet probe {DENY_PROBE} --stack {source}",
        f"  repro      magnet probe {TOOLS_PROBE} --stack {source}",
        f"  repro      magnet probe {HOOK_PROBE} --stack {source}",
        f"  repro      magnet probe {PROMPT_PROBE} --stack {source}",
    ]
    return "\n".join(lines)
