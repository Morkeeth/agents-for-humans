"""scripts/judge-demo.sh — judge kill-bar regression."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "judge-demo.sh"


def test_judge_demo_script_has_path_fix():
    text = SCRIPT.read_text()
    assert ".local/bin" in text, "judge-demo.sh must export ~/.local/bin after pip install"
    assert "magnet demo" in text
    assert "JUDGE DEMO OK" in text


def test_judge_demo_script_exits_zero():
    assert SCRIPT.is_file()
    env = {
        **dict(os.environ),
        "MAGNET_JUDGE_QUICK": "1",
        "PATH": f"{os.environ.get('HOME', '')}/.local/bin:" + os.environ.get("PATH", ""),
    }
    proc = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "JUDGE DEMO OK" in proc.stdout
    assert "quick mode" in proc.stdout or "naive verdict" in proc.stdout
