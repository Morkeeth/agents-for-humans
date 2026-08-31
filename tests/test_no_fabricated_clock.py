"""Control: no surface may print a fabricated clock as if it were a real reading.

MAGNET's whole constraint is "no number without the command, the population, and
when it was read". The demo simulates a second week so that a helped/hurt verdict
is possible from one run. Simulating is fine. Printing the simulated instant in a
field called `read_at`, unlabelled, is not -- a judge reading the receipt on
31 Aug saw `read_at 2026-09-08`.

These tests fail if that regresses.
"""
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from magnet.agent_run import run_agent_loop
from magnet.demo import run_demo
from magnet.log import connect, list_readings, record_reading, reset_demo

ROOT = Path(__file__).resolve().parents[1]

READ_AT = re.compile(r"^\s*read_at\s+(\S+)", re.MULTILINE)


def _read_at_stamps(text: str) -> list[datetime]:
    return [datetime.fromisoformat(m) for m in READ_AT.findall(text)]


def _assert_no_future_read_at(text: str) -> None:
    """Every `read_at` a surface prints must be a real, already-elapsed clock."""
    ceiling = datetime.now() + timedelta(minutes=5)  # tolerance for clock skew only
    for stamp in _read_at_stamps(text):
        assert stamp <= ceiling, (
            f"read_at {stamp.isoformat()} is in the future "
            f"(now={datetime.now().isoformat()}). A field named read_at must never "
            f"carry a fabricated clock.\n\n{text}"
        )


def test_demo_read_at_is_never_in_the_future():
    _assert_no_future_read_at(run_demo(repo_root=str(ROOT)))


def test_agent_run_read_at_is_never_in_the_future():
    _assert_no_future_read_at(run_agent_loop(repo_root=str(ROOT)))


def test_demo_labels_its_simulated_week():
    """A simulated reading must say so on screen, in words."""
    out = run_demo(repo_root=str(ROOT))
    assert "simulated" in out.lower(), (
        "demo advances the clock by 8 days but never tells the reader.\n\n" + out
    )


def test_agent_run_labels_its_simulated_week():
    out = run_agent_loop(repo_root=str(ROOT))
    assert "simulated" in out.lower(), (
        "agent-run advances the clock by 8 days but never tells the reader.\n\n" + out
    )


def test_cli_demo_prints_no_future_read_at():
    """Same control at the CLI surface a judge actually runs."""
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "demo"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    _assert_no_future_read_at(proc.stdout)


def test_simulated_rows_are_flagged_in_the_database():
    """The flag is stored, not just printed -- so any future surface can honour it."""
    conn = connect(str(ROOT / ".magnet" / "test-clock.db"))
    reset_demo(conn)
    record_reading(conn, "p", 1, "cmd", population=2)
    record_reading(
        conn, "p", 2, "cmd", population=2,
        now=datetime.now() + timedelta(days=8), simulated=True,
    )
    rows = list_readings(conn, "p")
    assert rows[0]["detail"].get("simulated") is not True
    assert rows[1]["detail"].get("simulated") is True
