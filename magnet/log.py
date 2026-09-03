"""In-repo SQLite adoption LOG — NOT Helicon-only.

Named `log`, never "ledger": that word is a standing house ruling. `magnet/ledger.py`
remains as a deprecated import shim, and an existing `.magnet/ledger.db` is migrated
in place on first connect so no one loses data. See migrate_legacy_database().
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG = ".magnet/log.db"
LEGACY_LOG = ".magnet/ledger.db"  # pre-rename name, migrated on first connect

SCHEMA = """
CREATE TABLE IF NOT EXISTS probe_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    probe_name TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    week TEXT NOT NULL,
    value INTEGER,
    population INTEGER,
    command TEXT NOT NULL,
    unmeasured TEXT DEFAULT '',
    change_id INTEGER,
    detail TEXT DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_probe_week ON probe_readings(probe_name, week);

CREATE TABLE IF NOT EXISTS adoptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TEXT NOT NULL,
    change_type TEXT NOT NULL,
    description TEXT NOT NULL,
    prediction TEXT NOT NULL,
    probe_name TEXT NOT NULL,
    detail TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS demo_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def default_log_path(cwd: str | None = None) -> str:
    root = Path(cwd or os.getcwd())
    return str(root / DEFAULT_LOG)


def legacy_log_path(cwd: str | None = None) -> str:
    root = Path(cwd or os.getcwd())
    return str(root / LEGACY_LOG)


def migrate_legacy_database(path: str) -> str | None:
    """Move a pre-rename `ledger.db` to the new `log.db` name, once.

    Returns the path migrated from, or None if there was nothing to do. Never
    overwrites an existing new-name database -- if both exist the new one wins
    and the old file is left untouched for the user to inspect.
    """
    target = Path(path)
    if target.name != "log.db" or target.exists():
        return None
    legacy = target.with_name("ledger.db")
    if not legacy.exists():
        return None
    legacy.rename(target)
    return str(legacy)


def connect(path: str | None = None, *, announce: bool = True) -> sqlite3.Connection:
    path = path or default_log_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    migrated = migrate_legacy_database(path)
    if migrated and announce:
        print(f"MAGNET: migrated {migrated} -> {path} (renamed 'ledger' to 'log')")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    ensure_schema(conn)
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def _week(now: datetime) -> str:
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _now() -> datetime:
    """Aware UTC. Every stamp this module writes carries its zone (+00:00)."""
    return datetime.now(timezone.utc)


def _aware(now: datetime) -> datetime:
    """A naive `now` is taken as UTC so no stamp is ever written without a zone."""
    return now if now.tzinfo is not None else now.replace(tzinfo=timezone.utc)


def record_reading(
    conn: sqlite3.Connection,
    probe_name: str,
    value: int | None,
    command: str,
    *,
    population: int | None = None,
    unmeasured: str = "",
    change_id: int | None = None,
    detail: dict | None = None,
    now: datetime | None = None,
    simulated: bool = False,
) -> dict:
    """Store one probe reading.

    A same-week re-record of the SAME run (same change_id, or both baseline)
    replaces the prior row — weekly cadence. A baseline read and a post-adoption
    read taken the same day are different runs and both survive, so two real
    reads in one sitting can yield helped/hurt without a simulated clock.
    (Until 2026-09-03 the DELETE ignored change_id and the honest path could
    never print a verdict inside one ISO week.)

    `simulated=True` marks a row whose `now` is a made-up clock (the demo
    advances a week so a helped/hurt verdict is possible in one run). The flag
    is persisted in `detail` so every surface can refuse to print it as a real
    read time. See tests/test_no_fabricated_clock.py.
    """
    now = _aware(now) if now else _now()
    detail = dict(detail or {})
    if simulated:
        detail['simulated'] = True
    week = _week(now)
    stamp = now.isoformat(timespec="seconds")
    conn.execute(
        "DELETE FROM probe_readings WHERE week = ? AND probe_name = ? AND change_id IS ?",
        (week, probe_name, change_id),
    )
    conn.execute(
        "INSERT INTO probe_readings "
        "(probe_name, recorded_at, week, value, population, command, "
        "unmeasured, change_id, detail) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (
            probe_name,
            stamp,
            week,
            value,
            population,
            command,
            unmeasured,
            change_id,
            json.dumps(detail or {}),
        ),
    )
    conn.commit()
    return {
        "probe_name": probe_name,
        "week": week,
        "recorded_at": stamp,
        "value": value,
        "population": population,
        "command": command,
        "unmeasured": unmeasured,
        "change_id": change_id,
        "simulated": bool(simulated),
    }


def record_week(conn: sqlite3.Connection, probe_name: str, reading: dict) -> dict:
    """Alias used by the Strands tool surface."""
    return record_reading(
        conn,
        probe_name,
        reading.get("value"),
        reading.get("command", f"magnet probe {probe_name}"),
        population=reading.get("population"),
        unmeasured=reading.get("unmeasured", ""),
        change_id=reading.get("change_id"),
        detail=reading.get("detail"),
    )


def adopt_change(
    conn: sqlite3.Connection,
    change_type: str,
    description: str,
    prediction: str,
    probe_name: str,
    *,
    detail: dict | None = None,
) -> dict:
    now = _now()
    stamp = now.isoformat(timespec="seconds")
    cur = conn.execute(
        "INSERT INTO adoptions (recorded_at, change_type, description, "
        "prediction, probe_name, detail) VALUES (?,?,?,?,?,?)",
        (stamp, change_type, description, prediction, probe_name, json.dumps(detail or {})),
    )
    conn.commit()
    return {
        "id": cur.lastrowid,
        "recorded_at": stamp,
        "change_type": change_type,
        "description": description,
        "prediction": prediction,
        "probe_name": probe_name,
    }

def list_readings(conn: sqlite3.Connection, probe_name: str) -> list[dict]:
    rows = conn.execute(
        "SELECT probe_name, recorded_at, week, value, population, command, "
        "unmeasured, change_id, detail FROM probe_readings "
        "WHERE probe_name = ? ORDER BY recorded_at",
        (probe_name,),
    ).fetchall()
    out = []
    for r in rows:
        out.append(
            {
                "probe_name": r["probe_name"],
                "recorded_at": r["recorded_at"],
                "week": r["week"],
                "value": r["value"],
                "population": r["population"],
                "command": r["command"],
                "unmeasured": r["unmeasured"],
                "change_id": r["change_id"],
                "detail": json.loads(r["detail"] or "{}"),
            }
        )
    return out


def latest_adoption(conn: sqlite3.Connection, probe_name: str) -> dict | None:
    row = conn.execute(
        "SELECT id, recorded_at, change_type, description, prediction, probe_name "
        "FROM adoptions WHERE probe_name = ? ORDER BY recorded_at DESC LIMIT 1",
        (probe_name,),
    ).fetchone()
    if row is None:
        return None
    return dict(row)


def get_demo_bonus(conn: sqlite3.Connection) -> int:
    row = conn.execute(
        "SELECT value FROM demo_state WHERE key = 'skill_bonus'"
    ).fetchone()
    return int(row["value"]) if row else 0


def set_demo_bonus(conn: sqlite3.Connection, bonus: int) -> None:
    conn.execute(
        "INSERT INTO demo_state (key, value) VALUES ('skill_bonus', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (str(bonus),),
    )
    conn.commit()


def reset_demo(conn: sqlite3.Connection) -> None:
    conn.executescript(
        "DELETE FROM probe_readings; DELETE FROM adoptions; DELETE FROM demo_state;"
    )
    conn.commit()


def default_ledger_path(cwd: str | None = None) -> str:
    """Deprecated alias for default_log_path(). Kept so old callers keep working."""
    return default_log_path(cwd)
