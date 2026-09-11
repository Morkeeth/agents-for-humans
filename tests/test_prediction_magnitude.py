"""Slice 25 — prediction magnitude honesty + naive direction arm."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.pred_demo import SCENARIOS, run_pred_demo
from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    naive_direction_check,
    prediction_intent,
)

ROOT = Path(__file__).resolve().parents[1]


def test_still_pass_is_flat():
    assert prediction_intent("all tests still pass") == "flat"
    assert prediction_intent("tests remain green") == "flat"
    assert prediction_intent("must stay at 190/190") == "flat"


def test_claimed_magnitude_parses_fraction():
    c = claimed_magnitude("pass rate rises by 2/5")
    assert c["amount"] == 2
    assert c["population"] == 5


def test_claimed_magnitude_parses_absolute():
    c = claimed_magnitude("coverage rises by 1")
    assert c["amount"] == 1
    assert c["population"] is None


def test_wrong_magnitude_magnet_misses_naive_holds():
    """THE DEFECT: Slice 24 printed held on rises-by-2/5 with Δ +1."""
    pred = "pass rate rises by 2/5"
    magnet = check_prediction(pred, "helped", 1, population=5)
    naive = naive_direction_check(pred, "helped", 1)
    assert magnet["outcome"] == "prediction-missed"
    assert magnet["grade"] == "direction+magnitude"
    assert magnet["magnitude_ok"] is False
    assert naive["outcome"] == "prediction-held"
    assert naive["grade"] == "direction-only"


def test_correct_fraction_holds():
    c = check_prediction("pass rate rises by 1/5", "helped", 1, population=5)
    assert c["outcome"] == "prediction-held"
    assert c["expected_delta"] == 1
    assert c["grade"] == "direction+magnitude"


def test_wrong_population_misses():
    c = check_prediction("coverage rises by 1/5", "helped", 1, population=12)
    assert c["outcome"] == "prediction-missed"
    assert c["population_ok"] is False


def test_vague_rise_direction_only_holds():
    c = check_prediction("coverage rises", "helped", 1, population=12)
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction"
    assert c["expected_delta"] is None


def test_fall_fraction_holds():
    c = check_prediction("pass rate falls by 2/5", "hurt", -2, population=5)
    assert c["outcome"] == "prediction-held"
    assert c["expected_delta"] == -2


def test_strip_title_still_grades_without_fraction():
    c = check_prediction("simplify skill frontmatter", "hurt", -7, population=7)
    assert c["outcome"] == "prediction-held"
    assert c["grade"] == "direction"


def test_pred_demo_embarrasses_naive():
    text = run_pred_demo()
    assert "FINDING  naive direction-only invents" in text
    assert "wrong_magnitude" in text
    magnet_line = next(ln for ln in text.splitlines() if ln.strip().startswith("magnet"))
    score = magnet_line.split()[1]
    n, t = score.split("/")
    assert n == t == str(len(SCENARIOS))


def test_adopt_misses_on_wrong_magnitude_claim(tmp_path):
    out = run_adopt(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 2/5",
        "demo-pass-rate",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    assert "prediction-missed" in out
    assert "direction+magnitude" in out or "grade      direction+magnitude" in out
    assert "claimed Δ" in out


def test_adopt_holds_on_correct_magnitude(tmp_path):
    out = run_adopt(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 1/5",
        "demo-pass-rate",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    assert "prediction-held" in out
    assert "claimed Δ" in out


def test_adopt_still_pass_flat_against_helped_is_missed(tmp_path):
    out = run_adopt(
        "skill",
        "demo-verification-skill",
        "all tests still pass",
        "demo-pass-rate",
        log_path=str(tmp_path / "log.db"),
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    assert "intent     flat" in out
    assert "prediction-missed" in out


def test_cli_pred_demo_exit_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "pred-demo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FINDING" in proc.stdout


def test_history_shows_claimed_delta(tmp_path):
    log = str(tmp_path / "log.db")
    run_adopt(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 2/5",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "history"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "claimed Δ" in proc.stdout
    assert "prediction-missed" in proc.stdout


def test_receipt_json_includes_prediction_check(tmp_path):
    log = str(tmp_path / "log.db")
    run_adopt(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 2/5",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "--log", log, "receipt"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["prediction_check"]["outcome"] == "prediction-missed"
    assert data["claimed_magnitude"]["amount"] == 2
    assert data["claimed_magnitude"]["population"] == 5
    assert data["delta"] == 1
