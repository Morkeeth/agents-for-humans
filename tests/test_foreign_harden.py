"""Slice 22 — hook control fix + foreign-harden closed loop."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from magnet.foreign_harden import harden_one, run_foreign_harden
from magnet.stack_bind import hook_coverage

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"
GRINDER = ROOT / "fixtures" / "real-stacks" / "agentgrinder"


def test_missing_settings_hook_coverage_is_zero():
    """Green-on-outage control: empty dir must NOT score no-rm-rf-star-allow."""
    d = tempfile.mkdtemp()
    reading = hook_coverage(d)
    assert reading["population"] == 2
    assert reading["value"] == 0
    assert "no-rm-rf-star-allow" in reading["detail"]["missing"]
    assert "dangerous-actions-blocker" in reading["detail"]["missing"]


def test_grinder_fixture_hook_starts_at_zero():
    """Agent Grinder fixture has no settings.json — must be 0/2 after control fix."""
    reading = hook_coverage(str(GRINDER))
    assert reading["value"] == 0
    assert reading["population"] == 2


def test_fixture_with_rm_rf_allow_still_zero_hooks():
    reading = hook_coverage(str(FIXTURE))
    assert reading["value"] == 0
    assert "no-rm-rf-star-allow" in reading["detail"]["missing"]


def test_settings_without_allow_key_does_not_score_clean():
    d = Path(tempfile.mkdtemp())
    (d / "settings.json").write_text('{"permissions": {"deny": []}}\n', encoding="utf-8")
    reading = hook_coverage(str(d))
    assert reading["value"] == 0
    assert "no-rm-rf-star-allow" in reading["detail"]["missing"]


def test_empty_allow_list_with_settings_scores_clean_allow():
    """settings.json present + allow: [] means we opened a clean allow list."""
    d = Path(tempfile.mkdtemp())
    (d / "settings.json").write_text(
        '{"permissions": {"allow": [], "deny": []}}\n', encoding="utf-8"
    )
    reading = hook_coverage(str(d))
    assert reading["value"] == 1
    assert "no-rm-rf-star-allow" in reading["detail"]["present"]
    assert "dangerous-actions-blocker" in reading["detail"]["missing"]


def test_foreign_harden_grinder_closes_loop():
    result = harden_one(str(GRINDER), label="Agent Grinder fixture")
    assert result["naive"]["verdict"] == "complete"
    assert result["before_near_zero"] is True
    assert result["moved"] >= 3
    # Effort must move 0/1 → 1/1 on the working copy.
    assert result["before"]["probes"]["effort-coverage"]["value"] == 0
    assert result["after"]["probes"]["effort-coverage"]["value"] == 1
    # Hook before must be 0/2 (control fix); after apply 2/2.
    assert result["before"]["probes"]["hook-coverage"]["value"] == 0
    assert result["after"]["probes"]["hook-coverage"]["value"] == 2
    # Source untouched.
    assert hook_coverage(str(GRINDER))["value"] == 0


def test_foreign_harden_offline_renders_finding():
    text = run_foreign_harden(repo_root=str(ROOT))
    assert "FINDING" in text
    assert "naive_title=complete" in text
    assert "title never measured" in text or "title→apply→helped" in text
    assert "foreign-harden" in text


def test_cli_foreign_harden_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "foreign-harden"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FINDING" in proc.stdout
    assert "moved=" in proc.stdout


def test_cli_foreign_harden_stack_arg():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "foreign-harden",
            "--stack",
            str(GRINDER),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "agentgrinder" in proc.stdout
    assert "FINDING" in proc.stdout
