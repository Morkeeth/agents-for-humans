"""Independent-stack replication — EXP-MAGNET S4 partial.

Runs the bakeoff on (1) the author fixture stack and (2) an independent stack
the filter author did not design (`fixtures/stack-cursor`, copied from live
Cursor skills). Numbers are re-derived every run.

If magnet loses on the independent stack, that is the finding — printed, not
papered over. Author-fixture magnet must still beat naive_stars (product claim);
losing there is a RED control.
"""
from __future__ import annotations

import os
from pathlib import Path

from magnet.bakeoff import run_bakeoff

AUTHOR_STACK = "fixtures/stack"
INDEPENDENT_STACK = "fixtures/stack-cursor"


def _stack_path(repo_root: str, rel: str) -> str:
    return str(Path(repo_root) / rel)


def run_replicate(
    *,
    repo_root: str | None = None,
    noise_n: int = 200,
) -> dict:
    root = repo_root or os.getcwd()
    author = run_bakeoff(
        stack_dir=_stack_path(root, AUTHOR_STACK),
        repo_root=root,
        noise_n=noise_n,
        write_candidates=False,
    )
    independent = run_bakeoff(
        stack_dir=_stack_path(root, INDEPENDENT_STACK),
        repo_root=root,
        noise_n=noise_n,
        write_candidates=False,
    )

    author_magnet = author["arms"]["magnet"]["recall_at_k"]
    author_stars = author["arms"]["naive_stars"]["recall_at_k"]
    ind_magnet = independent["arms"]["magnet"]["recall_at_k"]
    ind_stars = independent["arms"]["naive_stars"]["recall_at_k"]

    author_beats = author_magnet > author_stars
    independent_lost = ind_magnet < ind_stars
    liar_ok = (
        not author["wine_liar_in_magnet_primary"]
        and not independent["wine_liar_in_magnet_primary"]
    )

    findings = []
    if not author_beats:
        findings.append(
            "AUTHOR FIXTURE REGRESSION: magnet recall does not beat naive_stars "
            "on fixtures/stack — product claim broken."
        )
    else:
        findings.append(
            f"author fixture: magnet {author_magnet} beats naive_stars {author_stars}"
        )

    if independent_lost:
        findings.append(
            f"INDEPENDENT STACK: magnet LOST "
            f"({ind_magnet} < naive_stars {ind_stars}) on fixtures/stack-cursor — "
            "EXP-MAGNET caveat re-derived: precision depends on which caps are "
            "uncovered; a thin real stack admits noise into the shortlist."
        )
    elif ind_magnet == ind_stars:
        findings.append(
            f"independent stack: magnet TIED naive_stars at {ind_magnet}"
        )
    else:
        findings.append(
            f"independent stack: magnet {ind_magnet} beats naive_stars {ind_stars}"
        )

    if independent["arms"]["magnet"]["noise_in_top"] > 0:
        findings.append(
            f"independent magnet admitted "
            f"{independent['arms']['magnet']['noise_in_top']} noise into top-k "
            f"(uncovered caps: {', '.join(independent['gaps']['uncovered'][:6])}…)"
        )

    if not liar_ok:
        findings.append("CONSTITUTION FAIL: wine-liar bought primary rank")

    return {
        "author": author,
        "independent": independent,
        "author_magnet_beats_naive": author_beats,
        "independent_magnet_lost": independent_lost,
        "wine_liar_ok": liar_ok,
        "findings": findings,
        "token_cost": 0,
    }


def render_replicate(result: dict) -> str:
    a, i = result["author"], result["independent"]
    lines = [
        "MAGNET replicate — author fixture vs independent Cursor stack",
        "",
        "  EXP-MAGNET S4 partial: same planted flood, stack the filter author "
        "did not write.",
        "  Planted set is still authored — stated limit, not hidden.",
        "",
        "  stack                  magnet  naive_stars  best         noise",
        "  " + "-" * 66,
    ]
    for label, r in (("author/fixture", a), ("independent/cursor", i)):
        m = r["arms"]["magnet"]
        n = r["arms"]["naive_stars"]
        lines.append(
            f"  {label:<22} {m['recall_at_k']:<7} {n['recall_at_k']:<12} "
            f"{r['best_arm']:<12} {m['noise_in_top']}"
        )

    lines += ["", "  FINDINGS"]
    for f in result["findings"]:
        lines.append(f"    · {f}")

    lines += [
        "",
        f"  wine-liar quarantined   {result['wine_liar_ok']}  (must be True)",
        f"  author must-beat        {result['author_magnet_beats_naive']}  (must be True)",
        f"  tokens                  {result['token_cost']}",
        "",
        "  repro      magnet replicate",
    ]
    return "\n".join(lines)


def replicate_exit_code(result: dict) -> int:
    """RED only on constitution breaks / author-fixture regression.

    Independent-stack loss exits 0 — that finding is the product.
    """
    if not result["wine_liar_ok"]:
        return 1
    if not result["author_magnet_beats_naive"]:
        return 1
    return 0
