"""Slice 30 — commit hash must not poison pytest-count claims across newlines."""
from magnet.probes import _first_int_any, _PYTEST_COUNT_PATTERNS


def test_commit_hash_above_pytest_does_not_claim_898():
    text = "# run 2026-09-12T17:29:19Z @ c1ed898\npytest-pass-rate: 241/241\n"
    claimed = _first_int_any(text, _PYTEST_COUNT_PATTERNS + (r"(\d+)[ \t]+tests",))
    assert claimed is None
