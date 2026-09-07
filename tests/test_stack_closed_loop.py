"""Slice 15 — stack-coverage closed loop + probe --stack + real-stack object."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.probes import run_stack_coverage_probe
from magnet.stack import install_skill, read_skill_source, stack_coverage
from magnet.stack_demo import naive_install_verdict, run_stack_demo

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"
CANDIDATES = ROOT / "fixtures" / "candidates"
REAL_AG = ROOT / "fixtures" / "real-stacks" / "agentgrinder"


def test_probe_stack_flag_accepted():
    """Receipt used to advertise --stack while CLI rejected it (found by running)."""
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "magnet.cli",
            "probe",
            "stack-coverage",
            "--stack",
            str(REAL_AG),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "1/12" in proc.stdout
    assert "--stack" in proc.stdout


def test_real_agentgrinder_coverage_is_one_of_twelve():
    """Open the object — companion product covers writing only."""
    cov = stack_coverage(str(REAL_AG))
    assert cov["value"] == 1
    assert cov["population"] == 12
    assert "writing" in cov["detail"]["covered_caps"]
    assert "debug" in cov["detail"]["uncovered"]


def test_install_skill_raises_coverage(tmp_path):
    import shutil

    work = tmp_path / "stack"
    shutil.copytree(FIXTURE, work)
    before = stack_coverage(str(work))
    src = read_skill_source(str(CANDIDATES / "pdb-navigator"))
    install_skill(
        str(work),
        name=src["name"],
        description=src["description"],
        body=src["body"],
    )
    after = stack_coverage(str(work))
    assert after["value"] == before["value"] + 1
    assert "debug" not in after["detail"]["uncovered"]


def test_duplicate_install_does_not_raise_coverage(tmp_path):
    import shutil

    work = tmp_path / "stack"
    shutil.copytree(FIXTURE, work)
    before = stack_coverage(str(work))
    src = read_skill_source(str(CANDIDATES / "writing-coach-pro"))
    install_skill(
        str(work),
        name=src["name"],
        description=src["description"],
        body=src["body"],
    )
    after = stack_coverage(str(work))
    assert after["value"] == before["value"]


def test_naive_install_always_helped():
    assert naive_install_verdict(installed=True) == "helped"
    assert naive_install_verdict(installed=False) == "unchanged"


def test_stack_demo_prints_embarrassment_and_real_object(tmp_path):
    out = run_stack_demo(log_path=str(tmp_path / "s.db"), repo_root=str(ROOT))
    assert "MAGNET stack-demo" in out
    assert "naive" in out.lower()
    assert "helped" in out
    assert "unchanged" in out  # duplicate/noise magnet arm
    assert "1/12" in out
    assert "agentgrinder" in out.lower() or "Agent Grinder" in out
    assert "FINDING" in out


def test_adopt_install_closes_coverage_loop(tmp_path):
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "pdb-navigator",
        "coverage rises",
        "stack-coverage",
        log_path=log,
        reset=True,
        fit=True,
        stack_dir=str(FIXTURE),
        install_from=str(CANDIDATES / "pdb-navigator"),
    )
    assert "installed" in out
    assert "helped" in out
    assert "fills-gap" in out or "fills" in out.lower()
    assert "naive" in out.lower()
    # Fixture itself must be untouched
    still = stack_coverage(str(FIXTURE))
    assert still["value"] == 8


def test_adopt_install_noise_magnet_unchanged_naive_helped(tmp_path):
    log = str(tmp_path / "log.db")
    out = run_adopt(
        "skill",
        "wine-pairing",
        "more wine",
        "stack-coverage",
        log_path=log,
        reset=True,
        fit=True,
        stack_dir=str(FIXTURE),
        install_from=str(CANDIDATES / "wine-pairing"),
    )
    assert "unchanged" in out
    assert "naive" in out.lower() and "helped" in out
    assert "no-signal" in out


def test_cli_stack_demo_exit_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "stack-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "stack-demo" in proc.stdout.lower() or "FINDING" in proc.stdout


def test_run_stack_coverage_probe_honours_stack_dir():
    cov = run_stack_coverage_probe(repo_root=str(ROOT), stack_dir=str(REAL_AG))
    assert cov["value"] == 1
    assert cov["population"] == 12
