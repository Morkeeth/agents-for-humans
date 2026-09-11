"""Slice 25 — pred-demo proves stems + marketing miss at the object."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.pred_demo import run_pred_demo

ROOT = Path(__file__).resolve().parents[1]


def test_pred_demo_pass_at_object():
    text = run_pred_demo(repo_root=str(ROOT))
    assert "RESULT    PASS" in text
    assert "prediction-held" in text
    assert "marketing rise-speak" in text or "prediction-missed" in text
    assert "improves" in text


def test_cli_pred_demo_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT    PASS" in proc.stdout
    assert "stem" in proc.stdout
