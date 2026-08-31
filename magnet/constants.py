"""Shared constants."""
TOOL_NAMES = ("run_probe", "record_week", "adopt_change", "check_docs")

#: Days the demo/agent-run advance their clock so the second reading lands in the
#: next ISO week and a helped/hurt verdict is possible from one run. EVERY reading
#: written with this offset must be flagged `simulated=True` so no surface prints
#: it in a `read_at` field. See tests/test_no_fabricated_clock.py.
SIMULATED_WEEK_OFFSET_DAYS = 8
