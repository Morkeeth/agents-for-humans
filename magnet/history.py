"""Adoption history — the decision surface over the SQLite log."""
from __future__ import annotations

import sqlite3

from magnet.log import connect, list_readings
from magnet.reporter import format_value_pop, verdict


def list_adoptions(conn: sqlite3.Connection, probe_name: str | None = None) -> list[dict]:
    if probe_name:
        rows = conn.execute(
            "SELECT id, recorded_at, change_type, description, prediction, probe_name "
            "FROM adoptions WHERE probe_name = ? ORDER BY recorded_at",
            (probe_name,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, recorded_at, change_type, description, prediction, probe_name "
            "FROM adoptions ORDER BY recorded_at"
        ).fetchall()
    return [dict(r) for r in rows]


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
        readings = list_readings(conn, pname)
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
        lines.append(f"    readings   {len(readings)}")
        lines.append("")

    lines.append(f"  probes     {', '.join(sorted(probes_seen))}")
    lines.append("  repro      magnet history")
    return "\n".join(lines)
