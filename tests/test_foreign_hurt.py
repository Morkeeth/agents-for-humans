"""Slice 23 — foreign-hurt + hooks-layout honesty."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.foreign_hurt import hurt_one, run_foreign_hurt
from magnet.stack_bind import hook_coverage, hooks_layout

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"
GRINDER = ROOT / "fixtures" / "real-stacks" / "agentgrinder"
SP_HOOKS = ROOT / "fixtures" / "real-stacks" / "superpowers-hooks"


def test_superpowers_hooks_layout_opens_hooks_json():
    layout = hooks_layout(str(SP_HOOKS))
    ug = hook_coverage(str(SP_HOOKS))
    assert layout["value"] == 3
    assert layout["population"] == 3
    assert ug["value"] == 0
    assert ug["population"] == 2


def test_cli_probe_hooks_layout():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "probe",
            "hooks-layout",
            "--stack",
            str(SP_HOOKS),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "3/3" in proc.stdout or "hooks-layout" in proc.stdout


def test_foreign_hurt_grinder_naive_helped_on_hurt():
    result = hurt_one(str(GRINDER), label="grinder")
    assert result["magnet_hurt"] >= 3
    assert result["naive_helped_on_hurt"] == result["magnet_hurt"]
    # Source untouched
    assert hook_coverage(str(GRINDER))["value"] == 0


def test_foreign_hurt_offline_finding():
    text = run_foreign_hurt(repo_root=str(ROOT))
    assert "FINDING" in text
    assert "naive invented helped" in text
    assert "magnet-hurt" in text or "hurt" in text
    assert "prediction-held" in text
    assert "pred=" in text


def test_cli_foreign_hurt_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "foreign-hurt"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FINDING" in proc.stdout
    assert "naive invented helped" in proc.stdout
    assert "prediction-held" in proc.stdout


def test_foreign_bind_reports_layout_finding_on_superpowers_hooks():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "foreign-bind",
            "--stack",
            str(SP_HOOKS),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "hooks-layout" in proc.stdout
    assert "UG hook-coverage" in proc.stdout or "hooks/" in proc.stdout
