"""Slice 34 — Grinder evidence export never invents COUNT_FIELDS."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from magnet.demo import run_demo
from magnet.log import connect
from magnet.probes import check_docs
from magnet.receipt import (
    _GRINDER_COUNT_FIELDS,
    build_grinder_evidence,
    render_grinder_evidence_json,
)

ROOT = Path(__file__).resolve().parents[1]


def test_grinder_evidence_has_no_count_fields(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    conn = connect(log, announce=False)
    evidence = build_grinder_evidence(conn, repo_root=str(ROOT))
    assert evidence["schema"] == "magnet.grinder-evidence/v1"
    assert evidence["exportable"] is True
    assert evidence["verify_ok"] is True
    for banned in _GRINDER_COUNT_FIELDS:
        assert banned not in evidence
        assert banned not in json.dumps(evidence)
    assert evidence["prediction_outcome"] in (
        "prediction-held",
        "prediction-missed",
        "unmeasured",
        "no-direction",
    )


def test_grinder_evidence_refuses_when_verify_red(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    conn = connect(log, announce=False)
    rid, old = conn.execute(
        "SELECT id, value FROM probe_readings ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.execute(
        "UPDATE probe_readings SET value = ? WHERE id = ?",
        (int(old) + 77, rid),
    )
    conn.commit()
    text, code = render_grinder_evidence_json(log_path=log, repo_root=str(ROOT))
    assert code == 1
    data = json.loads(text)
    assert data["exportable"] is False
    assert data["verify_ok"] is False


def test_cli_receipt_grinder(tmp_path):
    log = str(tmp_path / "log.db")
    run_demo(log_path=log, repo_root=str(ROOT))
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "receipt", "--grinder"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["schema"] == "magnet.grinder-evidence/v1"
    assert "turns_typed" not in data


def test_check_docs_red_without_receipt_demo_finding(tmp_path):
    (tmp_path / "README.md").write_text(
        "MAGNET has 4 tools: run_probe record_week adopt_change check_docs\n"
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_a.py").write_text("def test_a():\n    assert True\n")
    shots = tmp_path / "docs" / "screenshots"
    shots.mkdir(parents=True)
    (shots / "history.txt").write_text(
        "outcome    prediction-held\nclaimed Δ  amount=1\n"
    )
    (shots / "one-workflow.txt").write_text("outcome    prediction-held\n")
    (shots / "receipt-demo.txt").write_text("receipt demo without finding line\n")
    results = {r["claim"]: r for r in check_docs(str(tmp_path))}
    assert results["screenshot receipt-demo finding"]["ok"] is False


def test_repo_receipt_demo_sidecar_has_finding():
    text = (ROOT / "docs" / "screenshots" / "receipt-demo.txt").read_text(
        encoding="utf-8"
    )
    assert "FINDING" in text
    assert "GREEN" in text
    assert "RED" in text
