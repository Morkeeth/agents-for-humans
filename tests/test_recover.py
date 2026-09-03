"""recover demo — thin LOST → covered WIN with 0 noise."""
from __future__ import annotations

from pathlib import Path

from magnet.recover import (
    NOISE_ATTRACTING_CAPS,
    diagnose_noise_caps,
    recover_exit_code,
    render_recover,
    run_recover,
)

ROOT = Path(__file__).resolve().parents[1]
CURSOR = ROOT / "fixtures" / "stack-cursor"


def test_diagnose_noise_caps_are_planning_writing_design():
    """Re-derive the cause — do not carry the prompt's list blindly."""
    d = diagnose_noise_caps(stack_dir=str(CURSOR), noise_n=200)
    assert d["noise_in_top"] > 0
    # Every noise fill on this fixture must be one of the known attractors
    for cap in d["cap_hits"]:
        assert cap in NOISE_ATTRACTING_CAPS, d["cap_hits"]
    # And each attractor must actually appear (otherwise the cover skills are wrong)
    for cap in NOISE_ATTRACTING_CAPS:
        assert d["cap_hits"].get(cap, 0) > 0, d["cap_hits"]


def test_recover_thin_lost_then_covered_wins():
    result = run_recover(repo_root=str(ROOT), noise_n=200)
    assert result["thin_lost"] is True
    assert result["covered_wins"] is True
    assert result["covered_noise_zero"] is True
    assert result["wine_liar_ok"] is True
    assert recover_exit_code(result) == 0
    text = render_recover(result)
    assert "LOST" in text
    assert "WINS" in text or "wins" in text
    assert "0 noise" in text.lower() or "with 0 noise" in text
    # Covered recall must beat thin recall (re-derived)
    assert (
        result["after"]["arms"]["magnet"]["recall_at_k"]
        > result["before"]["arms"]["magnet"]["recall_at_k"]
    )


def test_recover_cli_exit_zero():
    from magnet.cli import main

    assert main(["--repo", str(ROOT), "recover", "--noise", "200"]) == 0
