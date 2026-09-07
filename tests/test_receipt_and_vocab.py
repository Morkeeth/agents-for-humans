"""Slice 16 — synonym vocab 1.1 + machine-readable receipt."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from magnet.bakeoff import run_bakeoff
from magnet.demo import run_demo
from magnet.log import connect
from magnet.receipt import build_receipt, render_receipt_json
from magnet.stack import TAG_VOCAB_VERSION, stack_coverage

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "stack"
REAL_AG = ROOT / "fixtures" / "real-stacks" / "agentgrinder"


def test_tag_vocab_version_is_1_1():
    assert TAG_VOCAB_VERSION == "1.1"


def test_synonym_primary_recovered_without_wine_liar():
    result = run_bakeoff(
        stack_dir=str(FIXTURE),
        repo_root=str(ROOT),
        noise_n=80,
        write_candidates=False,
    )
    magnet = result["arms"]["magnet"]
    assert magnet["per_kind"]["synonym"]["found"] == 3
    assert magnet["per_kind"]["synonym"]["of"] == 3
    assert result["wine_liar_in_magnet_primary"] is False
    assert magnet["noise_in_top"] == 0
    assert magnet["liars_in_top"] == 0
    assert magnet["recall_at_k"] >= 0.875


def test_vocab_bump_does_not_inflate_fixture_or_agentgrinder_coverage():
    """False-positive guard — new terms must not invent coverage on owned text."""
    assert stack_coverage(str(FIXTURE))["value"] == 8
    assert stack_coverage(str(REAL_AG))["value"] == 1


def test_receipt_json_after_demo(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    raw = render_receipt_json(log_path=log)
    data = json.loads(raw)
    assert data["schema"] == "magnet.receipt/v1"
    assert data["verdict"] == "helped"
    assert data["latest"]["value_pop"] == "4/5"
    assert data["latest"]["command"]
    assert data["readings"] == 2


def test_cli_receipt_exit_zero(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "receipt", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # --json is not a flag; receipt always prints JSON. Keep CLI simple.
    # If someone passes --json as unknown, argparse fails — use bare receipt.
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "receipt"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["verdict"] in ("helped", "hurt", "unchanged", "baseline")


def test_build_receipt_binds_to_adoption_readings(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    conn = connect(log, announce=False)
    data = build_receipt(conn)
    assert data["change"]["description"] == "demo-verification-skill"
    assert data["delta"] == 1
