"""Slice 26 — adopt receipt binds to THIS adoption; marketing RED control."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.log import connect, latest_adoption

ROOT = Path(__file__).resolve().parents[1]


def test_same_second_second_adopt_receipt_names_second_change(tmp_path):
    """Pre-fix: latest_adoption by recorded_at tied → receipt said FIRST."""
    log = str(tmp_path / "log.db")
    out1 = run_adopt(
        "skill",
        "FIRST",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=False,
    )
    assert "change     FIRST" in out1
    out2 = run_adopt(
        "skill",
        "SECOND",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=log,
        reset=False,
        apply_demo_bonus=False,
        simulate_next_week=False,
    )
    assert "recorded   [skill] SECOND" in out2
    assert "change     SECOND" in out2
    assert "change     FIRST" not in out2


def test_latest_adoption_orders_by_id_not_timestamp_tie(tmp_path):
    log = str(tmp_path / "log.db")
    run_adopt(
        "skill",
        "FIRST",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=False,
    )
    run_adopt(
        "skill",
        "SECOND",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=log,
        reset=False,
        apply_demo_bonus=False,
        simulate_next_week=False,
    )
    conn = connect(log)
    # Force a timestamp tie the way SQLite stored them, then ask latest.
    conn.execute(
        "UPDATE adoptions SET recorded_at = (SELECT recorded_at FROM adoptions WHERE id = 1)"
    )
    conn.commit()
    row = latest_adoption(conn, "demo-pass-rate")
    assert row is not None
    assert row["description"] == "SECOND"
    assert row["id"] == 2


def test_foreign_hurt_cli_requires_marketing_finding():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "foreign-hurt"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "marketing rise-speak prediction-missed" in proc.stdout
