"""Two defects found while recording docs/DEMO-ONE-WORKFLOW.md (2026-09-03).

5. `magnet history` printed the probe's LATEST verdict on every adoption row, so
   the "drop the rule" adoption (whose own reading was hurt) showed `helped`.
   Each row must bind to the reading recorded for its own change_id.
6. The test suite ran `pip install -e .` (via scripts/stranger-pass.sh and
   scripts/judge-demo.sh), repointing the machine's editable `magnet` to
   whichever checkout ran the eval. Under test the scripts must not install.
"""
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from magnet.history import render_history
from magnet.log import adopt_change, connect, record_reading, reset_demo

ROOT = Path(__file__).resolve().parents[1]


def _rows(out: str) -> dict[str, str]:
    """Map adoption description -> verdict line, from rendered history."""
    rows = {}
    for block in re.split(r"\n(?=\s*#\d+\s)", out):
        m_desc = re.search(r"change\s+\[\w+\]\s+(.+)", block)
        m_verdict = re.search(r"verdict\s+(\w+)", block)
        if m_desc and m_verdict:
            rows[m_desc.group(1).strip()] = m_verdict.group(1)
    return rows


# 5 — each history row carries its own adoption's verdict
def test_history_row_binds_to_its_own_reading(tmp_path):
    conn = connect(str(tmp_path / "h.db"))
    reset_demo(conn)
    t = datetime(2026, 9, 2, 22, 13, tzinfo=timezone.utc)
    record_reading(conn, "p", 81, "cmd", population=81, now=t)
    a = adopt_change(conn, "prompt", "drop the rule", "unchanged", "p")
    record_reading(conn, "p", 80, "cmd", population=81, now=t, change_id=a["id"])
    b = adopt_change(conn, "prompt", "restore the rule", "recovers", "p")
    record_reading(conn, "p", 81, "cmd", population=81, now=t, change_id=b["id"])

    rows = _rows(render_history(conn))
    assert rows["drop the rule"] == "hurt", rows
    assert rows["restore the rule"] == "helped", rows


def test_history_row_shows_its_own_latest_value(tmp_path):
    conn = connect(str(tmp_path / "h2.db"))
    reset_demo(conn)
    t = datetime(2026, 9, 2, 22, 13, tzinfo=timezone.utc)
    record_reading(conn, "p", 81, "cmd", population=81, now=t)
    a = adopt_change(conn, "prompt", "drop the rule", "unchanged", "p")
    record_reading(conn, "p", 80, "cmd", population=81, now=t, change_id=a["id"])
    b = adopt_change(conn, "prompt", "restore the rule", "recovers", "p")
    record_reading(conn, "p", 81, "cmd", population=81, now=t, change_id=b["id"])
    out = render_history(conn)
    first = out.split("#2")[0]
    assert "latest     80/81" in first, first


# 6 — the suite never installs anything
def _quick_env() -> dict:
    env = {**os.environ, "MAGNET_STRANGER_QUICK": "1", "MAGNET_JUDGE_QUICK": "1", "PYTEST_CURRENT_TEST": ""}
    env.pop("PYTEST_CURRENT_TEST")
    # pip refuses to install outside a virtualenv with this set: if a script
    # still runs `pip install`, it exits non-zero and the test fails.
    env["PIP_REQUIRE_VIRTUALENV"] = "1"
    return env


def test_stranger_pass_under_test_does_not_pip_install():
    proc = subprocess.run(
        ["bash", str(ROOT / "scripts" / "stranger-pass.sh")],
        cwd=str(ROOT), capture_output=True, text=True, timeout=120, env=_quick_env(),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "stranger pass OK" in proc.stdout
    assert "install skipped" in proc.stdout, proc.stdout


def test_judge_demo_under_test_does_not_pip_install():
    proc = subprocess.run(
        ["bash", str(ROOT / "scripts" / "judge-demo.sh")],
        cwd=str(ROOT), capture_output=True, text=True, timeout=120, env=_quick_env(),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "install skipped" in proc.stdout, proc.stdout
