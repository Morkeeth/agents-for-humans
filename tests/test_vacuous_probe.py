"""Slice 30 — vacuous probe RED + empty-allow hook honesty."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from magnet.reporter import format_value_pop
from magnet.stack_bind import effort_coverage, hook_coverage, tools_coverage
from magnet.vacuous_demo import run_vacuous_demo

ROOT = Path(__file__).resolve().parents[1]


def test_format_value_pop_vacuous_is_na():
    assert format_value_pop(0, 0) == "n/a"
    assert format_value_pop(None, 0) == "n/a"


def test_empty_skills_effort_is_vacuous_not_zero_over_zero():
    d = Path(tempfile.mkdtemp())
    (d / "skills").mkdir()
    reading = effort_coverage(str(d))
    assert reading["population"] == 0
    assert reading["value"] is None
    assert reading["detail"]["vacuous"] is True
    assert format_value_pop(reading["value"], reading["population"]) == "n/a"


def test_missing_stack_effort_is_vacuous():
    reading = effort_coverage("/tmp/magnet-does-not-exist-vacuous-xyz")
    assert reading["population"] == 0
    assert reading["value"] is None
    assert reading["detail"]["vacuous"] is True


def test_cli_vacuous_effort_exits_nonzero():
    d = Path(tempfile.mkdtemp())
    (d / "skills").mkdir()
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "probe",
            "effort-coverage",
            "--stack",
            str(d),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "n/a" in proc.stdout
    assert "vacuous" in proc.stdout.lower()


def test_empty_allow_alone_does_not_score_hook():
    """THE DEFECT: allow:[] scored no-rm-rf-star-allow → invents 1/2."""
    d = Path(tempfile.mkdtemp())
    (d / "settings.json").write_text(
        json.dumps({"permissions": {"allow": [], "deny": []}}) + "\n",
        encoding="utf-8",
    )
    reading = hook_coverage(str(d))
    assert reading["value"] == 0
    assert "no-rm-rf-star-allow" in reading["detail"]["missing"]


def test_empty_allow_with_blocker_scores_both():
    d = Path(tempfile.mkdtemp())
    hooks = d / "hooks"
    hooks.mkdir()
    (hooks / "dangerous-actions-blocker.sh").write_text("#!/bin/bash\nexit 0\n")
    (d / "settings.json").write_text(
        json.dumps(
            {
                "permissions": {"allow": [], "deny": []},
                "hooks": {
                    "PreToolUse": [
                        {
                            "matcher": "Bash",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "hooks/dangerous-actions-blocker.sh",
                                }
                            ],
                        }
                    ]
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    reading = hook_coverage(str(d))
    assert reading["value"] == 2
    assert "no-rm-rf-star-allow" in reading["detail"]["present"]
    assert "dangerous-actions-blocker" in reading["detail"]["present"]


def test_nonempty_clean_allow_still_scores_without_blocker():
    d = Path(tempfile.mkdtemp())
    (d / "settings.json").write_text(
        json.dumps({"permissions": {"allow": ["Read"], "deny": []}}) + "\n",
        encoding="utf-8",
    )
    reading = hook_coverage(str(d))
    assert reading["value"] == 1
    assert "no-rm-rf-star-allow" in reading["detail"]["present"]


def test_vacuous_demo_finding():
    text = run_vacuous_demo(repo_root=str(ROOT))
    assert "FINDING  vacuous/missing objects go RED" in text
    assert "n/a" in text
    assert "empty-allow" in text


def test_cli_vacuous_demo_exit_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "vacuous-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FINDING" in proc.stdout


def test_tools_vacuous_too():
    d = Path(tempfile.mkdtemp())
    (d / "skills").mkdir()
    reading = tools_coverage(str(d))
    assert reading["detail"]["vacuous"] is True
    assert reading["value"] is None
