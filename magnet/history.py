"""Adoption history — the decision surface over the SQLite log."""
from __future__ import annotations

import json
import sqlite3

from magnet.log import connect, list_readings
from magnet.reporter import format_value_pop, verdict


def list_adoptions(conn: sqlite3.Connection, probe_name: str | None = None) -> list[dict]:
    if probe_name:
        rows = conn.execute(
            "SELECT id, recorded_at, change_type, description, prediction, probe_name, detail "
            "FROM adoptions WHERE probe_name = ? ORDER BY recorded_at",
            (probe_name,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, recorded_at, change_type, description, prediction, probe_name, detail "
            "FROM adoptions ORDER BY recorded_at"
        ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["detail"] = json.loads(d.get("detail") or "{}")
        out.append(d)
    return out


def readings_for_adoption(readings: list[dict], change_id: int) -> list[dict]:
    """The readings a history row is judged on: up to and including the one
    recorded for this adoption (its change_id). Until 2026-09-03 every row was
    judged on the probe's LATEST reading, so an adoption that hurt printed
    `helped` once a later adoption recovered. An adoption with no bound reading
    falls back to the whole series (the old behaviour) so it still shows a verdict.
    """
    for i, r in enumerate(readings):
        if r.get("change_id") == change_id:
            return readings[: i + 1]
    return readings


def render_history(
    conn: sqlite3.Connection,
    *,
    probe_name: str | None = None,
) -> str:
    """Print adoption timeline with readings and verdicts."""
    adoptions = list_adoptions(conn, probe_name)
    lines = ["MAGNET history", ""]

    if not adoptions:
        lines.append("  (no adoptions recorded yet)")
        lines.append("  next: magnet demo")
        return "\n".join(lines)

    probes_seen: set[str] = set()
    for row in adoptions:
        pname = row["probe_name"]
        probes_seen.add(pname)
        readings = readings_for_adoption(list_readings(conn, pname), row["id"])
        label, delta = verdict(readings, direction="up")
        measured = [r for r in readings if r.get("value") is not None]

        lines.append(f"  #{row['id']}  {row['recorded_at']}")
        lines.append(f"    change     [{row['change_type']}] {row['description']}")
        lines.append(f"    probe      {pname}")
        lines.append(f"    predict    {row['prediction']}")
        if measured:
            latest = measured[-1]
            vp = format_value_pop(latest.get("value"), latest.get("population"))
            lines.append(f"    latest     {vp}  ({latest.get('command', '')})")
        lines.append(f"    verdict    {label}" + (f"  (Δ {delta})" if delta is not None else ""))
        pred = (row.get("detail") or {}).get("prediction_check")
        if pred:
            lines.append(
                f"    outcome    {pred.get('outcome')}  "
                f"(intent={pred.get('intent')})"
            )
        lines.append(f"    readings   {len(readings)}")
        lines.append("")

    lines.append(f"  probes     {', '.join(sorted(probes_seen))}")
    lines.append("  repro      magnet history")
    return "\n".join(lines)
