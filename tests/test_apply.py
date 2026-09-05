"""Slice 15 — adopt --apply writes the skill; coverage moves only when measured."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from magnet.apply import apply_skill_to_stack, materialize_working_stack, write_skill
from magnet.adopt import run_adopt
from magnet.probes import run_stack_coverage_probe
from magnet.stack import CAPABILITIES, fit_one, stack_coverage

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"


def test_fixture_coverage_leaves_security_uncovered():
    reading = stack_coverage(str(FIXTURE))
    assert reading["population"] == len(CAPABILITIES)
    assert "security" in reading["detail"]["uncovered"]
    assert reading["value"] == reading["population"] - len(reading["detail"]["uncovered"])


def test_fit_fills_security_without_writing_skill():
    """The defect: fit predicts fills-gap while the stack object is untouched."""
    before = stack_coverage(str(FIXTURE))["value"]
    fit = fit_one(
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
        str(FIXTURE),
    )
    after = stack_coverage(str(FIXTURE))["value"]
    assert fit["label"] == "fills-gap"
    assert "security" in fit["fills"]
    assert after == before, "fit must not mutate the stack"


def test_write_skill_raises_coverage_on_working_copy(tmp_path):
    dest = tmp_path / "stack"
    materialize_working_stack(str(FIXTURE), str(dest))
    before = stack_coverage(str(dest))
    assert "security" in before["detail"]["uncovered"]
    written = write_skill(
        str(dest),
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
    )
    assert Path(written["path"]).is_file()
    after = stack_coverage(str(dest))
    assert after["value"] == before["value"] + 1
    assert "security" not in after["detail"]["uncovered"]
    # Fixture must stay untouched
    assert "security" in stack_coverage(str(FIXTURE))["detail"]["uncovered"]


def test_apply_skill_to_stack_does_not_mutate_source(tmp_path):
    dest = tmp_path / "applied"
    result = apply_skill_to_stack(
        str(FIXTURE),
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
        dest=str(dest),
    )
    assert result["written"] is True
    assert Path(result["skill_path"]).is_file()
    assert "security" not in stack_coverage(str(dest))["detail"]["uncovered"]
    assert "security" in stack_coverage(str(FIXTURE))["detail"]["uncovered"]


def test_wine_pairing_apply_does_not_raise_coverage(tmp_path):
    dest = tmp_path / "applied"
    before = stack_coverage(str(FIXTURE))["value"]
    apply_skill_to_stack(
        str(FIXTURE),
        "wine-pairing",
        "suggest a bottle for dinner",
        dest=str(dest),
    )
    after = stack_coverage(str(dest))
    assert after["value"] == before
    fit = fit_one("wine-pairing", "suggest a bottle for dinner", str(FIXTURE))
    assert fit["label"] == "no-signal"


def test_adopt_apply_helped_on_security_fill(tmp_path):
    log = str(tmp_path / "log.db")
    work = str(tmp_path / "work-stack")
    out = run_adopt(
        "skill",
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
        "stack-coverage",
        log_path=log,
        reset=True,
        apply=True,
        simulate_next_week=False,
        fit=True,
        stack_dir=str(FIXTURE),
        apply_dest=work,
        fit_description="blocks leaking .env and finds credential patterns",
    )
    assert "verdict    helped" in out or "verdict=helped" in out
    assert "fills-gap" in out
    assert "security" in out
    assert "APPLIED" in out or "applied" in out.lower()
    # Working copy moved; fixture untouched
    assert "security" not in stack_coverage(work)["detail"]["uncovered"]
    assert "security" in stack_coverage(str(FIXTURE))["detail"]["uncovered"]


def test_adopt_apply_unchanged_on_noise(tmp_path):
    log = str(tmp_path / "log.db")
    work = str(tmp_path / "work-stack")
    out = run_adopt(
        "skill",
        "wine-pairing",
        "suggest a bottle for dinner",
        "stack-coverage",
        log_path=log,
        reset=True,
        apply=True,
        simulate_next_week=False,
        fit=True,
        stack_dir=str(FIXTURE),
        apply_dest=work,
        fit_description="suggest a bottle for dinner",
    )
    assert "unchanged" in out
    assert "no-signal" in out
    assert "helped" not in out.split("verdict")[-1] if "verdict" in out else True


def test_adopt_without_apply_stays_unchanged_even_when_fit_fills(tmp_path):
    """Without --apply, coverage cannot move — magnet must not invent helped."""
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
        "stack-coverage",
        log_path=log,
        reset=True,
        apply=False,
        simulate_next_week=False,
        fit=True,
        stack_dir=str(FIXTURE),
        fit_description="blocks leaking .env and finds credential patterns",
    )
    assert "fills-gap" in out
    assert "unchanged" in out
    assert "--apply" in out or "not written" in out.lower() or "was not applied" in out.lower()


def test_cli_adopt_apply_exit_0(tmp_path):
    log = tmp_path / "log.db"
    work = tmp_path / "work"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "--log",
            str(log),
            "adopt",
            "skill",
            "secrets-scanner",
            "blocks leaking .env and finds credential patterns",
            "--probe",
            "stack-coverage",
            "--apply",
            "--apply-dest",
            str(work),
            "--fit",
            "--no-simulate",
            "--reset",
            "--stack",
            str(FIXTURE),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "helped" in proc.stdout
    assert (work / "skills" / "secrets-scanner" / "SKILL.md").is_file()


def test_apply_demo_cold_path_exit_0():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "apply-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "naive-fit" in proc.stdout.lower() or "naive_fit" in proc.stdout.lower()
    assert "helped" in proc.stdout
    assert "unchanged" in proc.stdout
    assert "wine" in proc.stdout.lower() or "no-signal" in proc.stdout


def test_apply_eval_magnet_beats_naive_fit():
    from magnet.apply_eval import run_apply_eval, score_arms

    text = run_apply_eval(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    scores = score_arms(repo_root=str(ROOT), stack_dir=str(FIXTURE))
    assert scores["magnet"]["correct"] == scores["magnet"]["total"]
    assert scores["naive_fit"]["correct"] < scores["magnet"]["correct"]
    assert "best arm" in text.lower() or "best arm" in text
    assert scores["magnet"]["correct"] > scores["silent_null"]["correct"]
