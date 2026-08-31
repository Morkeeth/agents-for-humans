"""Strands agent entry — re-export for docs/tests."""
from magnet.local_model import ScriptedLocalModel
from magnet.tools import SYSTEM_PROMPT, build_strands_tools, create_agent

__all__ = ["build_strands_tools", "create_agent", "ScriptedLocalModel", "SYSTEM_PROMPT"]
