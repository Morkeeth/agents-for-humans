"""foreign-bind — Ultimate Guide bind probes on stacks MAGNET did not author.

Opens each stack object (effort / deny / tools / hook / prompt) and prints
magnet vs naive_title. A marketplace README that says "complete" while
effort-coverage is 0/N is the finding — never rank by repo name.
"""
from __future__ import annotations

import os
from pathlib import Path

from magnet.external import naive_title_verdict
from magnet.reporter import format_value_pop
from magnet.stack import default_stack_dir, stack_coverage
from magnet.stack_bind import (
    deny_coverage,
    effort_coverage,
    hook_coverage,
    prompt_consistency,
    tools_coverage,
)

# Offline arms — no network. Numbers re-derived every run.
OFFLINE_STACKS = (
    ("fixtures/stack", "fixture (ours — starts unhardened)"),
    ("fixtures/real-stacks/agentgrinder", "Agent Grinder fixture (companion)"),
)

BIND_MEASURES = (
    ("effort-coverage", effort_coverage),
    ("deny-coverage", deny_coverage),
    ("tools-coverage", tools_coverage),
    ("hook-coverage", hook_coverage),
    ("prompt-consistency", prompt_consistency),
    ("stack-coverage", stack_coverage),
)


def resolve_offline(repo_root: str) -> list[tuple[str, str]]:
    root = Path(repo_root)
    out = []
    for rel, label in OFFLINE_STACKS:
        path = root / rel
        if path.is_dir():
            out.append((str(path), label))
    return out


def measure_bind(stack_dir: str) -> dict:
    """Re-derive every bind probe at the stack object."""
    stack = os.path.expanduser(stack_dir)
    probes = {}
    for name, fn in BIND_MEASURES:
        probes[name] = fn(stack)
    return {
        "stack": stack,
        "probes": probes,
        "naive": naive_title_verdict(stack),
    }


def _hardening_near_zero(probes: dict) -> bool:
    """True when effort+tools+deny are all empty-or-zero (marketplace gap)."""
    for key in ("effort-coverage", "tools-coverage", "deny-coverage"):
        r = probes[key]
        pop = r.get("population") or 0
        val = r.get("value") or 0
        if pop > 0 and val > 0:
            return False
    return True


def render_foreign_bind(results: list[dict]) -> str:
    lines = [
        "MAGNET foreign-bind — Ultimate Guide probes on stacks we did not build",
        "",
        "  probe scores are re-derived at each object — never carried from a prior run",
        "",
    ]
    findings = 0
    for result in results:
        probes = result["probes"]
        naive = result["naive"]
        lines += [
            f"  STACK  {result['stack']}",
            f"  label  {result.get('label', '')}",
            f"  naive_title  {naive['verdict']}  ← {naive['note']}",
            "  probe                  value/pop   object",
            "  ---------------------  ----------  ------",
        ]
        for name, _ in BIND_MEASURES:
            r = probes[name]
            pop = r.get("population")
            if not pop:
                vp = "n/a"
                note = "object missing"
            else:
                vp = format_value_pop(r.get("value"), pop)
                note = (r.get("detail") or {}).get("object", "")
            lines.append(f"  {name:<22} {vp:<11} {note}")

        if naive["verdict"] == "complete" and _hardening_near_zero(probes):
            findings += 1
            effort = probes["effort-coverage"]
            tools = probes["tools-coverage"]
            deny = probes["deny-coverage"]
            lines.append(
                f"  FINDING  naive_title=complete but hardening is near-zero "
                f"(effort {format_value_pop(effort.get('value'), effort.get('population'))}, "
                f"tools {format_value_pop(tools.get('value'), tools.get('population'))}, "
                f"deny {format_value_pop(deny.get('value'), deny.get('population'))}) "
                f"— title is not the object."
            )
        elif naive["verdict"] == "complete":
            cov = probes["stack-coverage"]
            if (cov.get("value") or 0) < (cov.get("population") or 0):
                findings += 1
                lines.append(
                    f"  FINDING  naive_title=complete; stack-coverage "
                    f"{format_value_pop(cov.get('value'), cov.get('population'))}."
                )
        lines.append("")

    lines += [
        f"  findings   {findings}/{len(results)} stacks embarrassed naive_title",
        "  repro      magnet foreign-bind",
        "  repro      magnet foreign-bind --stack /path/to/clone",
        "  repro      bash scripts/foreign-stack.sh",
    ]
    if findings == 0 and results:
        lines.append(
            "  FINDING  no stack embarrassed naive_title — unexpected on "
            "marketplace clones; re-check probes open the object."
        )
    return "\n".join(lines)


def run_foreign_bind(
    *,
    repo_root: str | None = None,
    stacks: list[str] | None = None,
) -> str:
    root = repo_root or os.getcwd()
    pairs: list[tuple[str, str]] = []
    if stacks:
        for s in stacks:
            pairs.append((os.path.expanduser(s), "cli --stack"))
    else:
        pairs = resolve_offline(root)
        # Optional network clones via env (comma-separated), never required.
        extra = os.environ.get("MAGNET_FOREIGN_BIND", "").strip()
        if extra:
            for part in extra.split(","):
                part = part.strip()
                if part and Path(part).is_dir():
                    pairs.append((part, "MAGNET_FOREIGN_BIND"))

    if not pairs:
        return (
            "MAGNET foreign-bind — no stacks found\n"
            "  tip: fixtures/stack · fixtures/real-stacks/agentgrinder\n"
            "  tip: MAGNET_FOREIGN_BIND=/tmp/anthropics-skills,/tmp/superpowers"
        )

    results = []
    for path, label in pairs:
        row = measure_bind(path)
        row["label"] = label
        results.append(row)
    return render_foreign_bind(results)
