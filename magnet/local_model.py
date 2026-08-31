"""A local, scripted Strands model provider — no network, no credentials, no spend.

WHY THIS EXISTS
---------------
MAGNET's four tools carry Strands `@tool` decorators, but until now nothing ever
ran a Strands `Agent` over them: `create_agent()` had zero call sites, and
`agent_run.py` hand-called the plain Python functions in a fixed order. The
decorators were decoration.

`ScriptedLocalModel` is a real implementation of the Strands `Model` ABC. Plugged
into a real `strands.Agent`, the SDK's own event loop runs unmodified: it builds
the tool specs from the `@tool` decorators, receives `toolUse` blocks from this
provider, dispatches the actual MAGNET tool functions, feeds the `toolResult`
blocks back, and loops until `end_turn`.

WHAT IS REAL AND WHAT IS NOT — read this before quoting the demo
----------------------------------------------------------------
REAL: the Strands Agent, its event loop, the tool registry built from the four
      `@tool` functions, tool dispatch, tool results, and the message history.
NOT REAL: the token generation. This provider does not reason. It replays a
      fixed plan of tool calls. It proves the loop is wired; it does not prove a
      language model chose the sequence.

To see a model actually choose the tools, run with a Bedrock model — see
`magnet agent-run --model bedrock` and the README. That path needs AWS
credentials and costs money, so it is never the default and is never run in CI.
"""
from __future__ import annotations

import json
import threading
from collections.abc import AsyncGenerator, AsyncIterable
from typing import Any

from strands.models.model import Model
from strands.types.content import Messages, SystemContentBlock
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolChoice, ToolSpec

# The plan the scripted provider replays: (tool_name, input). This mirrors what a
# competent agent would do after a stack change — measure, record, adopt, re-check.
DEFAULT_PLAN: list[tuple[str, dict]] = [
    ("run_probe_tool", {"probe_name": "demo-pass-rate"}),
    ("record_week_tool", {"probe_name": "demo-pass-rate"}),
    (
        "adopt_change_tool",
        {
            "change_type": "skill",
            "description": "agent-run-verification-skill",
            "prediction": "pass rate rises by 1/5",
            "probe_name": "demo-pass-rate",
        },
    ),
    ("record_week_tool", {"probe_name": "demo-pass-rate", "simulate_next_week": True}),
    ("check_docs_tool", {}),
]

FINAL_TEXT = (
    "Adoption recorded. I ran the probe, stored a reading, adopted the change, "
    "re-read the probe and re-checked the docs. The verdict comes from the "
    "readings in the log — I did not invent a trend."
)


class ScriptedLocalModel(Model):
    """Replays a fixed tool-call plan through the real Strands event loop.

    Not a language model. See the module docstring for exactly what this does and
    does not prove.
    """

    #: Printed by any surface that runs this provider, so the mode is never silent.
    MODE_LABEL = "strands agent loop · local scripted model (no network, no spend)"

    def __init__(self, plan: list[tuple[str, dict]] | None = None, **config: Any) -> None:
        self.plan = list(plan if plan is not None else DEFAULT_PLAN)
        self._config: dict[str, Any] = {"model_id": "magnet-scripted-local", **config}
        self.calls: list[str] = []  # tool names actually emitted, for assertions

    # -- Model ABC ---------------------------------------------------------
    def update_config(self, **model_config: Any) -> None:
        self._config.update(model_config)

    def get_config(self) -> dict[str, Any]:
        return dict(self._config)

    async def structured_output(
        self, output_model, prompt: Messages, system_prompt: str | None = None, **kwargs: Any
    ) -> AsyncGenerator[dict[str, Any], None]:
        raise NotImplementedError("ScriptedLocalModel does not support structured_output()")

    async def stream(
        self,
        messages: Messages,
        tool_specs: list[ToolSpec] | None = None,
        system_prompt: str | None = None,
        *,
        tool_choice: ToolChoice | None = None,
        system_prompt_content: list[SystemContentBlock] | None = None,
        invocation_state: dict[str, Any] | None = None,
        cancel_signal: threading.Event | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[StreamEvent]:
        """Emit the next step of the plan as Bedrock-shaped stream events."""
        step = self._completed_tool_turns(messages)

        yield {"messageStart": {"role": "assistant"}}

        if step >= len(self.plan):
            yield {"contentBlockDelta": {"delta": {"text": FINAL_TEXT}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "end_turn"}}
            return

        name, tool_input = self.plan[step]
        self._guard_tool_exists(name, tool_specs)
        self.calls.append(name)

        yield {
            "contentBlockStart": {
                "start": {"toolUse": {"name": name, "toolUseId": f"magnet-{step}-{name}"}}
            }
        }
        yield {"contentBlockDelta": {"delta": {"toolUse": {"input": json.dumps(tool_input)}}}}
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "tool_use"}}

    # -- helpers -----------------------------------------------------------
    @staticmethod
    def _completed_tool_turns(messages: Messages) -> int:
        """How many tool calls the loop has already executed.

        Counted from toolResult blocks the SDK fed back, so the provider stays
        correct no matter how the caller assembled the history.
        """
        return sum(
            1
            for message in messages
            for block in message.get("content", [])
            if "toolResult" in block
        )

    @staticmethod
    def _guard_tool_exists(name: str, tool_specs: list[ToolSpec] | None) -> None:
        """Fail loudly if the plan names a tool the agent was never given.

        Without this a typo would look like a model that chose not to call
        anything — a silent pass where the loop did nothing.
        """
        if not tool_specs:
            raise RuntimeError(
                f"ScriptedLocalModel planned {name!r} but the agent was given no tools."
            )
        available = {spec["name"] for spec in tool_specs}
        if name not in available:
            raise RuntimeError(
                f"ScriptedLocalModel planned {name!r}, which is not a registered tool. "
                f"Registered: {sorted(available)}"
            )
