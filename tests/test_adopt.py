"""magnet adopt — core adoption loop."""
import os
import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt

ROOT = Path(__file__).resolve().parents[1]


def test_adopt_prints_receipt(tmp_path):
    out = run_adopt(
        "skill",
        "adopt-test-skill",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=str(tmp_path / "a.db"),
        apply_demo_bonus=True,
        reset=True,
    )
    assert "MAGNET adopt" in out
    assert "adopt-test-skill" in out
    assert "MAGNET receipt" in out


def test_adopt_cli_exits_zero():
    proc = subprocess.run(
        [
            sys.executable, "-m", "magnet.cli", "adopt",
            "skill", "cli-skill", "pass rate rises by 1/5",
            "--probe", "demo-pass-rate", "--demo-bonus", "--reset",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "cli-skill" in proc.stdout


def test_stranger_pass_script_exits_zero():
    script = ROOT / "scripts" / "stranger-pass.sh"
    assert script.is_file()
    env = {**dict(os.environ), "MAGNET_STRANGER_QUICK": "1", "PATH": f"{os.environ.get('HOME', '')}/.local/bin:" + os.environ.get("PATH", "")}
    proc = subprocess.run(
        ["bash", str(script)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "stranger pass OK" in proc.stdout
