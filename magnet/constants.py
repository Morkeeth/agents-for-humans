"""Shared constants."""
TOOL_NAMES = ("run_probe", "record_week", "adopt_change", "check_docs")

#: Anything that changes the stack is an adoption. The first three live in a repo
#: and a repo probe can see them; a hook or a setting lives in the agent config
#: (~/.claude, .claude/settings.json) and only a probe that reads the stack can.
CHANGE_TYPES = ("skill", "prompt", "model", "hook", "setting")
STACK_CHANGE_TYPES = ("hook", "setting")

#: Days the demo/agent-run advance their clock so the second reading lands in the
#: next ISO week and a helped/hurt verdict is possible from one run. EVERY reading
#: written with this offset must be flagged `simulated=True` so no surface prints
#: it in a `read_at` field. See tests/test_no_fabricated_clock.py.
SIMULATED_WEEK_OFFSET_DAYS = 8
