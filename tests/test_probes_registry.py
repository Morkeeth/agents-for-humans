"""Real pytest probe + registry + history tests."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from magnet.history import list_adoptions, render_history
from magnet.log import adopt_change, connect, list_readings, record_reading, reset_demo
from magnet.probes import PYTEST_PROBE, run_probe, run_pytest_probe
from magnet.registry import load_registry, parse_pytest_summary, run_registry_probe

ROOT = Path(__file__).resolve().parents[1]


def test_parse_pytest_summary_pass_only():
    value, pop = parse_pytest_summary("................................................  [100%]\n48 passed in 2.28s\n")
    assert value == 48
    assert pop == 48


def test_parse_pytest_summary_pass_and_fail():
    value, pop = parse_pytest_summary("45 passed, 3 failed in 1.2s\n")
    assert value == 45
    assert pop == 48


def test_pytest_probe_runs_real_pytest(tmp_path):
    """The probe must execute pytest on a scoped suite, not read a hardcoded count."""
    mini = tmp_path / "mini_tests"
    mini.mkdir()
    (mini / "test_a.py").write_text(
        "def test_one(): assert True\ndef test_two(): assert True\n",
        encoding="utf-8",
    )
    cmd = f"{sys.executable} -m pytest -q --tb=no mini_tests"
    conn = connect(str(tmp_path / "log.db"))
    result = run_pytest_probe(repo_root=str(tmp_path), command=cmd)
    assert result["value"] == 2
    assert result["population"] == 2
    assert result["detail"].get("real_eval") is True


def test_pytest_probe_refuses_recursion_inside_pytest(tmp_path):
    conn = connect(str(tmp_path / "log.db"))
    with pytest.raises(RuntimeError, match="refuses to run"):
        run_probe(conn, PYTEST_PROBE, repo_root=str(ROOT))


def test_registry_probe_exit_code_parser(tmp_path):
    spec = {"command": f"{sys.executable} -c \"print('ok')\"", "parser": "exit_code"}
    out = run_registry_probe("t", spec, repo_root=str(ROOT))
    assert out["value"] == 1
    assert out["population"] == 1


def test_load_registry_from_file(tmp_path):
    reg = tmp_path / ".magnet" / "probes.json"
    reg.parent.mkdir()
    reg.write_text(
        json.dumps({"probes": {"custom": {"command": "echo 3/5", "parser": "value_pop"}}}),
        encoding="utf-8",
    )
    loaded = load_registry(str(tmp_path))
    assert "custom" in loaded


def test_custom_registry_probe_value_pop(tmp_path):
    reg = tmp_path / ".magnet" / "probes.json"
    reg.parent.mkdir()
    reg.write_text(
        json.dumps({"probes": {"score": {"command": "echo 4/5", "parser": "value_pop"}}}),
        encoding="utf-8",
    )
    conn = connect(str(tmp_path / "log.db"))
    result = run_probe(conn, "score", repo_root=str(tmp_path))
    assert result["value"] == 4
    assert result["population"] == 5


def test_history_shows_adoptions(tmp_path):
    from datetime import datetime, timedelta

    conn = connect(str(tmp_path / "h.db"))
    reset_demo(conn)
    adopt_change(conn, "skill", "my-skill", "up 1/5", "demo-pass-rate")
    record_reading(
        conn, "demo-pass-rate", 3, "cmd", population=5,
        now=datetime(2026, 8, 1),
    )
    record_reading(
        conn, "demo-pass-rate", 4, "cmd", population=5,
        now=datetime(2026, 8, 8),
    )
    out = render_history(conn)
    assert "my-skill" in out
    assert "verdict    helped" in out
    assert len(list_adoptions(conn)) == 1


def test_list_probes_cli_includes_pytest():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "list-probes"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "pytest-pass-rate" in proc.stdout
    assert "demo-pass-rate" in proc.stdout


def test_history_cli_after_demo(tmp_path):
    log = str(tmp_path / "hist.db")
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    hist = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "history"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert hist.returncode == 0, hist.stderr
    assert "demo-verification-skill" in hist.stdout
