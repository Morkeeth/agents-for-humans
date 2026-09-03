"""Four defects found 2026-09-02 by running MAGNET on a real stack change.

Each test was written before the fix and failed against main @ c359b0a.
See docs/ULTIMATE-GUIDE-MAGNET-2026-09-02.md for the receipts that found them.

1. `magnet adopt hook|setting` exited 2: an adoption is anything that changes the
   stack, so the verb must accept it and the receipt must say when the probe
   cannot see it.
2. log.py deleted the same-week row regardless of change_id, so a baseline read
   and a post-adoption read taken on the same day collapsed to one reading and
   `--no-simulate` could never print helped/hurt.
3. `read_at` printed a UTC instant with no zone (two hours off a CEST wall clock).
4. `magnet list-probes` advertised `-m "not slow"` for pytest-pass-rate but
   `run_probe` executed the probe without it.
"""
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.log import adopt_change, connect, list_readings, record_reading, reset_demo
from magnet.probes import BUILTIN_PROBES, PYTEST_PROBE, run_probe

ROOT = Path(__file__).resolve().parents[1]


# 1 — the verb accepts a hook or a setting, and the receipt says what the probe can see
def _cli_adopt(tmp_path, change_type):
    return subprocess.run(
        [
            sys.executable, "-m", "magnet.cli", "--log", str(tmp_path / "a.db"),
            "adopt", change_type, f"{change_type}-under-test", "no change expected",
            "--probe", "demo-pass-rate", "--no-simulate", "--reset",
        ],
        cwd=str(ROOT), capture_output=True, text=True,
    )


def test_adopt_accepts_hook_and_setting(tmp_path):
    for kind in ("hook", "setting"):
        proc = _cli_adopt(tmp_path, kind)
        assert proc.returncode == 0, f"{kind}: {proc.stderr}"
        assert f"[{kind}] {kind}-under-test" in proc.stdout, proc.stdout


def test_receipt_says_when_a_builtin_probe_cannot_see_a_stack_change(tmp_path):
    """A built-in probe measures this repo. A hook/setting lives outside it.
    The receipt must say so instead of printing a silent 0-delta."""
    out = run_adopt(
        "hook", "PreToolUse secrets gate", "no change expected", "demo-pass-rate",
        log_path=str(tmp_path / "b.db"), simulate_next_week=False, reset=True,
    )
    assert re.search(r"^\s*measures\s+repo only", out, re.M), out
    # a skill/prompt/model change against the same probe carries no such line
    out2 = run_adopt(
        "skill", "some-skill", "no change expected", "demo-pass-rate",
        log_path=str(tmp_path / "c.db"), simulate_next_week=False, reset=True,
    )
    assert not re.search(r"^\s*measures\s+repo only", out2, re.M), out2


# 2 — same-day baseline + post-adoption readings are two readings
def test_same_day_baseline_and_post_adoption_readings_both_survive(tmp_path):
    conn = connect(str(tmp_path / "d.db"))
    reset_demo(conn)
    now = datetime(2026, 9, 2, 21, 54, tzinfo=timezone.utc)
    record_reading(conn, "p", 3, "cmd", population=5, now=now)
    adoption = adopt_change(conn, "skill", "s", "up", "p")
    record_reading(conn, "p", 4, "cmd", population=5, now=now, change_id=adoption["id"])
    rows = list_readings(conn, "p")
    assert [r["value"] for r in rows] == [3, 4], rows


def test_same_week_re_record_of_the_same_run_still_replaces(tmp_path):
    """The weekly-cadence rule survives: same week, same change_id → one row."""
    conn = connect(str(tmp_path / "e.db"))
    reset_demo(conn)
    now = datetime(2026, 9, 2, 21, 54, tzinfo=timezone.utc)
    record_reading(conn, "p", 3, "cmd", population=5, now=now, change_id=7)
    record_reading(conn, "p", 4, "cmd", population=5, now=now, change_id=7)
    rows = list_readings(conn, "p")
    assert len(rows) == 1 and rows[0]["value"] == 4, rows


def test_no_simulate_adopt_prints_a_verdict_not_baseline(tmp_path):
    """The honest path: two real reads in one sitting yield helped/hurt/unchanged."""
    out = run_adopt(
        "skill", "demo-skill", "pass rate rises by 1/5", "demo-pass-rate",
        log_path=str(tmp_path / "f.db"), apply_demo_bonus=True,
        simulate_next_week=False, reset=True,
    )
    assert "verdict    helped" in out, out
    assert "SIMULATED" not in out, out


# 3 — every stamp carries its zone
def test_read_at_and_recorded_at_carry_a_zone(tmp_path):
    out = run_adopt(
        "skill", "zone-skill", "up", "demo-pass-rate",
        log_path=str(tmp_path / "g.db"), apply_demo_bonus=True,
        simulate_next_week=False, reset=True,
    )
    stamps = re.findall(r"^\s*read_at\s+(\S+)", out, re.M)
    assert stamps, out
    for s in stamps:
        parsed = datetime.fromisoformat(s)
        assert parsed.tzinfo is not None, f"read_at {s} has no zone\n\n{out}"
    conn = connect(str(tmp_path / "g.db"))
    for r in list_readings(conn, "demo-pass-rate"):
        assert datetime.fromisoformat(r["recorded_at"]).tzinfo is not None, r
    row = conn.execute("SELECT recorded_at FROM adoptions").fetchone()
    assert datetime.fromisoformat(row["recorded_at"]).tzinfo is not None, dict(row)


# 4 — the executed command is the advertised command
def test_run_probe_executes_the_advertised_pytest_command(tmp_path, monkeypatch):
    advertised = next(p["command"] for p in BUILTIN_PROBES if p["name"] == PYTEST_PROBE)
    seen = {}

    class _Proc:
        returncode = 0
        stdout = "72 passed, 1 deselected in 9.0s\n"
        stderr = ""

    def fake_run(argv, **kwargs):
        seen["argv"] = argv
        return _Proc()

    import magnet.probes as probes

    monkeypatch.setattr(probes.subprocess, "run", fake_run)
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    conn = connect(str(tmp_path / "h.db"))
    result = run_probe(conn, PYTEST_PROBE, repo_root=str(ROOT))
    assert result["command"] == advertised, (result["command"], advertised)
    assert "not slow" in seen["argv"], seen["argv"]  # one argv element, not two
    assert "-m" in seen["argv"]
    assert result["value"] == 72 and result["population"] == 72  # deselected tests are not in the population
