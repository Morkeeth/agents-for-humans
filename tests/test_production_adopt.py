"""Production adopt path — real probe, not synthetic demo-pass-rate."""
from pathlib import Path

from magnet.adopt import run_adopt

ROOT = Path(__file__).resolve().parents[1]


def test_adopt_with_check_docs_probe_baseline_then_unchanged(tmp_path):
    """check-docs is a real eval (re-derived from source) and runs fast in tests."""
    out = run_adopt(
        "prompt",
        "docs-stay-valid",
        "all README claims still match source",
        "check-docs",
        log_path=str(tmp_path / "prod.db"),
        reset=True,
        simulate_next_week=False,
    )
    assert "MAGNET adopt" in out
    assert "docs-stay-valid" in out
    assert "MAGNET receipt" in out
    # Two identical readings on check-docs → unchanged (not helped)
    assert "unchanged" in out or "baseline" in out


def test_judge_demo_includes_production_adopt_step():
    script = ROOT / "scripts" / "judge-demo.sh"
    text = script.read_text()
    assert "pytest-pass-rate adopt" in text
    assert "production-eval-demo" in text
