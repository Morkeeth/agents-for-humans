"""bind-demo — the embarrassment arm for stack vs repo probes.

Applies Ultimate Guide recommendations (effort: frontmatter + permissions.deny)
to a TEMPORARY copy of fixtures/stack, then measures:

  repo-blind arm   check-docs (reads THIS repo — cannot see the stack change)
  stack-bind arms  effort-coverage + deny-coverage (open the stack object)
  naive arm        invents "helped" from the change title without opening anything

If the repo-blind arm stays unchanged while stack-bind arms move, that is the
product finding: "re-runs YOUR eval" is only true when YOUR eval opens the
object you changed.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from magnet.log import connect, list_readings, record_reading, reset_demo
from magnet.probes import run_check_docs_probe
from magnet.reporter import format_value_pop, naive_verdict, verdict
from magnet.stack import default_stack_dir
from magnet.stack_bind import (
    DENY_PROBE,
    EFFORT_PROBE,
    apply_deny_patterns,
    apply_effort_frontmatter,
    copy_stack,
    deny_coverage,
    effort_coverage,
)


def run_bind_demo(
    *,
    repo_root: str | None = None,
    stack_dir: str | None = None,
    log_path: str | None = None,
) -> str:
    root = Path(repo_root or os.getcwd())
    source = stack_dir or default_stack_dir(str(root))
    if not Path(source).is_dir():
        return f"MAGNET bind-demo — no stack at {source}\n  tip: fixtures/stack"

    work = tempfile.mkdtemp(prefix="magnet-bind-")
    stack = copy_stack(source, os.path.join(work, "stack"))
    db = log_path or os.path.join(work, "bind.db")
    conn = connect(db)
    reset_demo(conn)

    lines = [
        "MAGNET bind-demo — does YOUR eval open the object you changed?",
        "",
        f"  source     {source}",
        f"  working    {stack}  (temporary copy — source untouched)",
        f"  log        {db}",
        "",
        "  change A   add effort: frontmatter to every SKILL.md missing it",
        "  change B   add permissions.deny for .env/.pem/.key/credentials",
        "",
    ]

    # --- BEFORE ---
    before_repo = run_check_docs_probe(str(root))
    before_effort = effort_coverage(stack)
    before_deny = deny_coverage(stack)

    for reading in (before_repo, before_effort, before_deny):
        record_reading(
            conn,
            reading["probe_name"],
            reading.get("value"),
            reading["command"],
            population=reading.get("population"),
        )

    lines += [
        "  BEFORE (re-derived at object)",
        f"    check-docs       {format_value_pop(before_repo.get('value'), before_repo.get('population'))}"
        f"  ← repo object",
        f"    effort-coverage  {format_value_pop(before_effort.get('value'), before_effort.get('population'))}"
        f"  ← stack SKILL.md",
        f"    deny-coverage    {format_value_pop(before_deny.get('value'), before_deny.get('population'))}"
        f"  ← stack settings.json",
        "",
    ]

    # --- APPLY ---
    touched_effort = apply_effort_frontmatter(stack)
    touched_deny = apply_deny_patterns(stack)
    lines += [
        f"  APPLIED    effort: → {len(touched_effort)} skills  {touched_effort}",
        f"  APPLIED    deny    → {len(touched_deny)} patterns {touched_deny}",
        "",
    ]

    # --- AFTER ---
    after_repo = run_check_docs_probe(str(root))
    after_effort = effort_coverage(stack)
    after_deny = deny_coverage(stack)

    for reading in (after_repo, after_effort, after_deny):
        record_reading(
            conn,
            reading["probe_name"],
            reading.get("value"),
            reading["command"],
            population=reading.get("population"),
            # Same-day second reading must carry a distinct change_id so it
            # survives the week-key replace rule (MAGNET-BUGS #2).
            change_id=hash(reading["probe_name"]) & 0x7FFFFFFF,
        )

    lines += [
        "  AFTER (re-derived at object)",
        f"    check-docs       {format_value_pop(after_repo.get('value'), after_repo.get('population'))}",
        f"    effort-coverage  {format_value_pop(after_effort.get('value'), after_effort.get('population'))}",
        f"    deny-coverage    {format_value_pop(after_deny.get('value'), after_deny.get('population'))}",
        "",
    ]

    # --- VERDICTS ---
    def _arm(name: str) -> tuple[str, int | None]:
        readings = list_readings(conn, name)
        return verdict(readings, direction="up")

    repo_label, repo_delta = _arm("check-docs")
    effort_label, effort_delta = _arm(EFFORT_PROBE)
    deny_label, deny_delta = _arm(DENY_PROBE)

    # Naive: invents helped from the change TITLE without opening the stack.
    naive_title = "security-hardening effort: permissions.deny for secrets"
    naive = "helped"  # title contains security + effort → marketplace optimism

    lines += [
        "  VERDICTS",
        f"    repo-blind (check-docs)     {repo_label}"
        f"  Δ {repo_delta if repo_delta is not None else '—'}",
        f"    stack-bind (effort)         {effort_label}"
        f"  Δ {effort_delta if effort_delta is not None else '—'}",
        f"    stack-bind (deny)           {deny_label}"
        f"  Δ {deny_delta if deny_delta is not None else '—'}",
        f"    naive (title only)          {naive}"
        f"  ← invented from {naive_title!r}",
        "",
    ]

    # FINDING — the product claim that can embarrass us
    repo_blind = repo_label in ("unchanged", "baseline") or (repo_delta == 0)
    stack_moved = effort_label == "helped" or deny_label == "helped"
    if repo_blind and stack_moved:
        finding = (
            "FINDING  repo-blind check-docs stayed flat while stack-bind probes "
            "moved. A stack change is invisible to a repo eval — MAGNET only "
            "keeps its promise when YOUR probe opens the object you changed."
        )
    elif stack_moved:
        finding = (
            "FINDING  stack-bind probes moved. Repo-blind also moved — re-check "
            "whether check-docs accidentally reads the temp stack."
        )
    else:
        finding = (
            "FINDING  stack-bind probes did NOT move after applying effort/deny. "
            "This is a product defect — bind-demo must fail loud."
        )

    lines += [
        f"  {finding}",
        "",
        f"  naive vs magnet on effort series: "
        f"naive={naive_verdict(list_readings(conn, EFFORT_PROBE))}  "
        f"magnet={effort_label}",
        "",
        "  repro      magnet bind-demo",
        f"  repro      magnet probe {EFFORT_PROBE} --stack {source}",
        f"  repro      magnet probe {DENY_PROBE} --stack {source}",
    ]
    return "\n".join(lines)
