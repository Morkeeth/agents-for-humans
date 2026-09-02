"""scripts/cold-clone-verify.sh — post-push GitHub clone kill-bar."""
import os
import subprocess

import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cold-clone-verify.sh"


def test_cold_clone_script_exists_and_executable():
    assert SCRIPT.is_file()
    text = SCRIPT.read_text()
    assert "git clone" in text
    assert "judge-demo.sh" in text
    assert "COLD CLONE OK" in text


@pytest.mark.slow
def test_cold_clone_local_repo_exits_zero():
    """Clone this working tree (file://) — quick judge-demo avoids nested full-suite recursion."""
    env = {
        **dict(os.environ),
        "MAGNET_JUDGE_QUICK": "1",
        "PATH": f"{os.environ.get('HOME', '')}/.local/bin:" + os.environ.get("PATH", ""),
    }
    proc = subprocess.run(
        ["bash", str(SCRIPT), f"file://{ROOT}"],
        capture_output=True,
        text=True,
        timeout=300,
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "COLD CLONE OK" in proc.stdout
    assert "JUDGE DEMO OK" in proc.stdout
