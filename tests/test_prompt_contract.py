"""Prompt contract — the eval a prompt change is measured against.

MAGNET's system prompt carries the product's one rule. If a prompt edit drops
it, this test fails and `magnet probe pytest-pass-rate` falls by one, which is
what `docs/DEMO-ONE-WORKFLOW.md` shows on camera: change one prompt, re-run
YOUR eval, read helped / hurt / baseline.
"""
from magnet.tools import SYSTEM_PROMPT


def test_system_prompt_keeps_the_never_invent_rule():
    assert "never invent a trend from one reading" in SYSTEM_PROMPT


def test_system_prompt_forces_tool_use():
    assert "Always use the tools" in SYSTEM_PROMPT
