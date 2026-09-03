"""Independent-stack replicate + author must-beat control."""
from __future__ import annotations

from pathlib import Path

from magnet.replicate import (
    render_replicate,
    replicate_exit_code,
    run_replicate,
)

ROOT = Path(__file__).resolve().parents[1]


def test_independent_cursor_stack_fixture_exists():
    stack = ROOT / "fixtures" / "stack-cursor"
    assert stack.is_dir()
    assert (stack / "skills" / "env-setup" / "SKILL.md").is_file()
    assert (stack / "SOURCE.md").is_file()
    # canvas must not have the "metadata:" false description
    text = (stack / "skills" / "canvas" / "SKILL.md").read_text(encoding="utf-8")
    assert "metadata:" not in text.split("---")[1]
    assert "canvas.tsx" in text or "canvas" in text.lower()


def test_replicate_author_must_beat_naive_stars():
    """RED control: on the author fixture, magnet must beat marketplace stars."""
    result = run_replicate(repo_root=str(ROOT), noise_n=200)
    assert result["author_magnet_beats_naive"] is True
    assert result["wine_liar_ok"] is True
    assert replicate_exit_code(result) == 0
    author = result["author"]
    assert (
        author["arms"]["magnet"]["recall_at_k"]
        > author["arms"]["naive_stars"]["recall_at_k"]
    )


def test_replicate_records_independent_loss_without_exiting_red():
    """Independent stack may beat us — that finding exits 0, not 1."""
    result = run_replicate(repo_root=str(ROOT), noise_n=200)
    text = render_replicate(result)
    # Re-derive: if magnet lost, the receipt must say so (do not paper over).
    ind_m = result["independent"]["arms"]["magnet"]["recall_at_k"]
    ind_n = result["independent"]["arms"]["naive_stars"]["recall_at_k"]
    if ind_m < ind_n:
        assert result["independent_magnet_lost"] is True
        assert "LOST" in text
        assert "INDEPENDENT STACK" in " ".join(result["findings"])
    assert replicate_exit_code(result) == 0
    assert "wine-liar quarantined   True" in text


def test_replicate_cli_exit_zero(tmp_path):
    from magnet.cli import main

    code = main(["--repo", str(ROOT), "replicate", "--noise", "50"])
    assert code == 0
