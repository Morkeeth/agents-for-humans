"""Eval harness — naive vs MAGNET vs always-baseline (silent null).

Scores each arm against explicit ground truth, not against itself.
The silent-null arm always returns baseline; it beats naive on one-reading
cases and loses when a real trend exists — that asymmetry is the finding.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

from magnet.reporter import naive_verdict, verdict

VerdictLabel = Literal["baseline", "helped", "hurt", "unchanged"]


@dataclass(frozen=True)
class Scenario:
    name: str
    readings: list[dict]
    truth: VerdictLabel
    direction: str = "up"
    note: str = ""


def silent_null_verdict(_readings: list[dict]) -> str:
    """Trivial arm: always baseline. Correct when n<2; wrong when trend is real."""
    return "baseline"


ARMS: dict[str, Callable[[list[dict]], str]] = {
    "naive": naive_verdict,
    "magnet": lambda rs: verdict(rs, direction="up")[0],
    "silent_null": silent_null_verdict,
}


SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        "one_reading",
        [{"value": 3, "population": 5}],
        "baseline",
        note="first reading is not a trend",
    ),
    Scenario(
        "helped",
        [{"value": 3, "population": 5}, {"value": 4, "population": 5}],
        "helped",
        note="adoption raised pass rate",
    ),
    Scenario(
        "hurt",
        [{"value": 4, "population": 5}, {"value": 2, "population": 5}],
        "hurt",
        note="change made things worse",
    ),
    Scenario(
        "unchanged",
        [{"value": 3, "population": 5}, {"value": 3, "population": 5}],
        "unchanged",
        note="no delta — naive still says helped",
    ),
    Scenario(
        "gap_week",
        [
            {"value": 2, "population": 5},
            {"value": None, "population": 5},
            {"value": 4, "population": 5},
        ],
        "helped",
        note="unmeasured middle week skipped",
    ),
)


def _score_arm(name: str, fn: Callable[[list[dict]], str]) -> tuple[int, int, list[str]]:
    correct = 0
    lines: list[str] = []
    for sc in SCENARIOS:
        got = fn(sc.readings) if name != "magnet" else verdict(sc.readings, direction=sc.direction)[0]
        ok = got == sc.truth
        if ok:
            correct += 1
        mark = "✓" if ok else "✗"
        lines.append(f"    {mark} {sc.name:<14} truth={sc.truth:<10} got={got}")
    return correct, len(SCENARIOS), lines


def run_eval() -> str:
    """Print scenario matrix and arm scores."""
    lines = [
        "MAGNET eval — arms scored against explicit ground truth",
        "",
        "  scenario       truth      naive   magnet  silent_null",
        "  " + "-" * 58,
    ]
    for sc in SCENARIOS:
        n = naive_verdict(sc.readings)
        m = verdict(sc.readings, direction=sc.direction)[0]
        s = silent_null_verdict(sc.readings)
        lines.append(
            f"  {sc.name:<14} {sc.truth:<10} {n:<7} {m:<7} {s}"
        )

    lines += ["", "  arm scores (correct / total):", ""]
    best_name, best_score = "", -1
    for arm_name in ("naive", "magnet", "silent_null"):
        fn = ARMS[arm_name]
        correct, total, detail = _score_arm(arm_name, fn)
        lines.append(f"  {arm_name:<12} {correct}/{total}")
        lines.extend(detail)
        lines.append("")
        if correct > best_score:
            best_score = correct
            best_name = arm_name

    lines.append(f"  best arm     {best_name} ({best_score}/{len(SCENARIOS)})")
    lines.append("")
    lines.append("  repro        magnet eval")
    if best_name == "silent_null":
        lines.append(
            "  finding      silent_null beats naive/magnet on conservative cases — "
            "MAGNET must not invent trends AND must detect real ones"
        )
    return "\n".join(lines)
