"""Receipt reporter — ported from measurement-bench / helicon.measure science.

Rules carried forward:
  - value/pop, never bare integers (`3/5`, never `3`)
  - baseline when len(measured) < 2 — a first reading is not a trend
  - helped/hurt only when two real readings exist and direction is known
  - unmeasured is NULL, never zero
  - a reading flagged `detail.simulated` NEVER prints in a `read_at` field;
    it prints as `simulated ... (SIMULATED week - not a real read time)`
"""
from __future__ import annotations

from typing import Literal

Verdict = Literal["baseline", "helped", "hurt", "unchanged"]


def format_value_pop(value: int | None, population: int | None) -> str:
    """Render value with population when one is declared."""
    if value is None:
        return "unmeasured"
    if population is not None:
        return f"{value}/{population}"
    return str(value)


def delta_arrow(delta: int | None) -> str:
    if delta is None:
        return ""
    if delta > 0:
        return "↑"
    if delta < 0:
        return "↓"
    return "→"


def verdict(
    readings: list[dict],
    *,
    direction: str = "up",
) -> tuple[Verdict, int | None]:
    """Label helped/hurt/baseline from a series of probe readings.

    `readings` items carry `value` (int|None). Only measured rows count.
    """
    measured = [r for r in readings if r.get("value") is not None]
    if len(measured) < 2:
        return "baseline", None
    before = measured[-2]["value"]
    after = measured[-1]["value"]
    delta = after - before
    if delta == 0:
        return "unchanged", 0
    good = (direction == "up" and delta > 0) or (direction == "down" and delta < 0)
    return ("helped" if good else "hurt"), delta


def render_receipt(
    probe_name: str,
    readings: list[dict],
    *,
    direction: str = "up",
    change_label: str = "",
    repro_command: str = "magnet demo",
) -> str:
    """Human-readable receipt with repro command."""
    measured = [r for r in readings if r.get("value") is not None]
    label, delta = verdict(readings, direction=direction)
    lines = ["MAGNET receipt", ""]
    if change_label:
        lines.append(f"  change     {change_label}")
    if not measured:
        lines.append(f"  probe      {probe_name}")
        lines.append("  verdict    baseline (no readings yet)")
        lines.append(f"  repro      {repro_command}")
        return "\n".join(lines)

    latest = measured[-1]
    value_txt = format_value_pop(latest.get("value"), latest.get("population"))
    cmd = latest.get("command") or repro_command
    read_at = latest.get("recorded_at") or latest.get("read_at") or ""
    simulated = bool((latest.get("detail") or {}).get("simulated"))

    lines.append(f"  probe      {probe_name}")
    lines.append(f"  latest     {value_txt}  ({cmd})")
    if read_at:
        if simulated:
            # A made-up clock must never be printed in a field called read_at.
            lines.append(f"  simulated  {read_at}  (SIMULATED week — not a real read time)")
        else:
            lines.append(f"  read_at    {read_at}")

    if label == "baseline":
        lines.append("  verdict    baseline — need two measured readings for helped/hurt")
    elif label == "unchanged":
        lines.append("  verdict    unchanged (0 vs prior)")
    else:
        arrow = delta_arrow(delta)
        sign = "+" if delta and delta > 0 else ""
        lines.append(f"  verdict    {label}  {arrow} {sign}{delta} vs prior")

    lines.append(f"  repro      {repro_command}")
    return "\n".join(lines)


def naive_verdict(readings: list[dict]) -> str:
    """Naive baseline arm: always says helped if the last value rose.

    Included so evals can beat us honestly — this is the two-hour team version.
    """
    measured = [r for r in readings if r.get("value") is not None]
    if len(measured) < 2:
        return "helped"  # the naive bug: invents optimism on one reading
    return "helped" if measured[-1]["value"] >= measured[-2]["value"] else "hurt"
