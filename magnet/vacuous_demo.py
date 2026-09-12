"""vacuous-demo — controls that go RED on empty/missing objects.

Found 2026-09-12 by running:
  magnet probe effort-coverage --stack /tmp/empty-stack  → 0/0 exit 0
  magnet probe hook-coverage --stack <empty allow:[]>   → 1/2 exit 0

Both invented green. A control that has not been watched going RED is not a
control. This demo opens empty/missing objects and prints the RED receipts
beside a real fixture that stays measurable.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from magnet.reporter import format_value_pop
from magnet.stack_bind import effort_coverage, hook_coverage, tools_coverage


def run_vacuous_demo(*, repo_root: str | None = None) -> str:
    root = Path(repo_root or Path(__file__).resolve().parents[1])
    fixture = root / "fixtures" / "stack"

    empty = Path(tempfile.mkdtemp(prefix="magnet-vacuous-empty-"))
    (empty / "skills").mkdir(parents=True, exist_ok=True)

    empty_allow = Path(tempfile.mkdtemp(prefix="magnet-vacuous-allow-"))
    (empty_allow / "settings.json").write_text(
        json.dumps({"permissions": {"allow": [], "deny": []}}, indent=2) + "\n",
        encoding="utf-8",
    )

    missing = str(Path(tempfile.gettempdir()) / "magnet-vacuous-missing-xyz")

    rows = [
        ("empty-skills", "effort-coverage", effort_coverage(str(empty))),
        ("empty-skills", "tools-coverage", tools_coverage(str(empty))),
        ("missing-path", "effort-coverage", effort_coverage(missing)),
        ("empty-allow", "hook-coverage", hook_coverage(str(empty_allow))),
        ("fixture/stack", "effort-coverage", effort_coverage(str(fixture))),
        ("fixture/stack", "hook-coverage", hook_coverage(str(fixture))),
    ]

    lines = [
        "MAGNET vacuous-demo — controls must go RED on empty/missing objects",
        "",
        "  Empty skills used to print 0/0 exit 0. Empty allow:[] used to score",
        "  hook 1/2. Both invented green. Naive arm: treat 0/0 as success.",
        "",
        "  object            probe                 shown     vacuous    exit",
        "  " + "-" * 72,
    ]
    reds = 0
    for obj, probe, reading in rows:
        pop = reading.get("population")
        val = reading.get("value")
        detail = reading.get("detail") or {}
        vacuous = bool(detail.get("vacuous")) or (pop == 0 and val is None)
        shown = format_value_pop(val, pop)
        # Hook empty-allow: not vacuous population, but must not invent 1/2.
        if obj == "empty-allow":
            exit_code = 0 if (val or 0) == 0 else 1
            vacuous_txt = "lie-fixed" if (val or 0) == 0 else "LIE"
            if (val or 0) == 0:
                reds += 1
        elif vacuous:
            exit_code = 1
            vacuous_txt = "yes"
            reds += 1
        else:
            exit_code = 0
            vacuous_txt = "no"
        lines.append(
            f"  {obj:<18}{probe:<22}{shown:<10}{vacuous_txt:<11}{exit_code}"
        )

    # Naive arm: 0/0 counts as success (the pre-Slice-30 lie).
    naive_empty = effort_coverage(str(empty))
    naive_shown = "0/0"  # the lie — never use format_value_pop here
    lines += [
        "",
        f"  naive arm   empty effort as {naive_shown!r} success  ← invents green on outage",
        f"  magnet      empty effort as {format_value_pop(naive_empty.get('value'), naive_empty.get('population'))!r} + exit 1",
        "",
    ]
    if reds >= 3:
        lines.append(
            "  FINDING  vacuous/missing objects go RED (n/a + exit 1); "
            "empty allow:[] no longer invents hook 1/2 without the blocker."
        )
    else:
        lines.append(
            f"  FINDING  only {reds} RED rows — vacuous control drifted; re-open the probe objects."
        )
    lines += [
        "",
        "  repro      magnet vacuous-demo",
        "  repro      magnet probe effort-coverage --stack /tmp/empty-skills   # expect n/a exit 1",
        "  repro      magnet probe hook-coverage --stack <settings allow:[]>   # expect 0/2",
    ]
    return "\n".join(lines)
