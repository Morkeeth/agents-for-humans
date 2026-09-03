"""bedrock-live-or-blocked.sh — controls that cannot go green on empty input.

Found pattern (week of 2026-09-02): `grep -qv` returns 1 on empty stdin, so a
"no AWS" inverted check read green during an outage. These tests pin the
script's positive-evidence path and the empty-grep trap itself.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bedrock-live-or-blocked.sh"


def test_empty_grep_qv_is_not_a_control():
    """Document the trap: inverted grep on empty input exits 1 (looks like 'found')."""
    proc = subprocess.run(
        ["bash", "-c", "printf '' | grep -qv AWS_; echo ec=$?"],
        capture_output=True, text=True, check=True,
    )
    assert "ec=1" in proc.stdout, proc.stdout


def test_bedrock_script_blocked_without_credentials(tmp_path, monkeypatch):
    """No AWS material → exit 2 BLOCKED, names exact missing env, never claims LIVE."""
    env = os.environ.copy()
    for k in list(env):
        if k.startswith("AWS_") or k.startswith("AMAZON_"):
            env.pop(k)
    env["MAGNET_BEDROCK_OUT"] = str(tmp_path / "out")
    env["MAGNET_BEDROCK_STAMP"] = "test-stamp"
    # Ensure PATH can find python3; script uses python3 -m magnet.cli only after STS.
    env["PATH"] = os.environ.get("PATH", "/usr/bin:/bin")

    proc = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 2, out
    assert "VERDICT: BLOCKED" in out, out
    assert "AWS_ACCESS_KEY_ID" in out and "MISSING" in out, out
    assert "NOT claimed: live Bedrock output" in out, out
    assert "VERDICT: LIVE" not in out
    report = Path(env["MAGNET_BEDROCK_OUT"]) / "probe.txt"
    assert report.is_file(), report
    body = report.read_text()
    assert "exact_missing:" in body
    assert "NoCredentialsError" in body or "sts_exit: 2" in body


def test_bedrock_script_is_executable():
    assert SCRIPT.is_file()
    assert os.access(SCRIPT, os.X_OK), f"{SCRIPT} not executable"
