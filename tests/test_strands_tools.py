"""Strands tool wiring — imports only, no Bedrock call."""
from magnet.tools import build_strands_tools


def test_build_strands_tools_returns_four():
    tools = build_strands_tools()
    names = sorted(getattr(t, "__name__", str(t)) for t in tools)
    assert len(tools) == 4
    assert any("run_probe" in n for n in names)
    assert any("check_docs" in n for n in names)
