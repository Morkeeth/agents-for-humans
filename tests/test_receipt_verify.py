"""Slice 33 — Grinder receipt --verify re-probes at the object."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.demo import run_demo
from magnet.log import connect
from magnet.receipt import render_receipt_json, run_receipt_demo, verify_receipt

ROOT = Path(__file__).resolve().parents[1]


def test_verify_green_after_demo(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    conn = connect(log, announce=False)
    check = verify_receipt(conn, repo_root=str(ROOT))
    assert check["ok"] is True
    assert check["stored"]["value"] == check["live"]["value"]
    assert check["stored"]["population"] == check["live"]["population"]


def test_verify_red_when_stored_value_planted(tmp_path):
    log = str(tmp_path / "log.db")
    run_adopt(
        "skill",
        "verify-plant",
        "pass rate recovers by 1",
        "demo-pass-rate",
        log_path=log,
        apply_demo_bonus=True,
        reset=True,
    )
    conn = connect(log, announce=False)
    assert verify_receipt(conn, repo_root=str(ROOT))["ok"] is True
    rid, old = conn.execute(
        "SELECT id, value FROM probe_readings ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.execute(
        "UPDATE probe_readings SET value = ? WHERE id = ?",
        (int(old) + 99, rid),
    )
    conn.commit()
    check = verify_receipt(conn, repo_root=str(ROOT))
    assert check["ok"] is False
    assert check["stored"]["value"] != check["live"]["value"]
    assert "verify RED" in check["note"]


def test_cli_receipt_verify_exit_codes(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    green = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "receipt", "--verify"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert green.returncode == 0, green.stderr
    data = json.loads(green.stdout)
    assert data["verify"]["ok"] is True

    conn = connect(log, announce=False)
    rid, old = conn.execute(
        "SELECT id, value FROM probe_readings ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.execute(
        "UPDATE probe_readings SET value = ? WHERE id = ?",
        (int(old) + 50, rid),
    )
    conn.commit()
    red = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "receipt", "--verify"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert red.returncode == 1
    data = json.loads(red.stdout)
    assert data["verify"]["ok"] is False


def test_receipt_demo_finding(tmp_path):
    text = run_receipt_demo(log_path=str(tmp_path / "rd.db"), repo_root=str(ROOT))
    assert "arm GREEN" in text
    assert "arm RED" in text
    assert "FINDING" in text
    assert "ok=True" in text.split("arm GREEN")[1].split("\n")[0]
    assert "ok=False" in text.split("arm RED")[1].split("\n")[0]


def test_cli_receipt_demo_exit_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "receipt-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "FINDING" in proc.stdout


def test_cli_receipt_json_alias(tmp_path):
    """--json used to be unrecognized; stranger docs expected it."""
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "receipt", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["schema"] == "magnet.receipt/v1"
