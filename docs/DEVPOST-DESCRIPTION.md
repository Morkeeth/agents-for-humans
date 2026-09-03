# Devpost description · paste-ready

Every number below comes from a command run on 2026-09-03 on `main` @ f690fd0, unless dated otherwise. The command is next to the number. Re-derive any of them with the command shown.

---

## Project name

MAGNET

## Tagline

Change a prompt. MAGNET re-runs your eval: helped or hurt.

(58 characters, under the 60 limit.) Longer form for the description header: Change a prompt, model, or skill. MAGNET re-runs your eval and prints helped, hurt, or baseline.

## Track

Professional Agents

---

## The problem

Developers who run agents change their stack every day: a prompt line, a model, a skill, a hook. Nobody writes down what each change did. The number that would tell them (the eval score before and after) lives in a terminal that scrolled away.

Two measured facts from this repo:

1. The naive rule most people apply ("the score went up after my change, so it helped") is wrong on 2 of 5 scored scenarios. Command: `magnet eval`. Naive scores 3/5, MAGNET 5/5, a do-nothing baseline 1/5.
2. Our own docs drifted within 13 hours. At 00:27 on 3 Sep the screenshot pack said 86 tests (source: `git show f690fd0:docs/screenshots/README.md`). At 13:57 the same day the suite had 113 (source: `magnet check-docs`, which re-derives the count from `tests/test_*.py`). The drift gate did not catch this one: it scans six named docs and that README is not one of them. It was caught by re-running the capture.

A team lead who changed a prompt and has to justify it needs the before number, the after number, the command that produced both, and the prediction they made before looking. That is the whole product.

## What MAGNET does

MAGNET is an adoption log and eval runner for your own agent stack. You tell it what you changed and what you predict. It re-runs your eval (your pytest suite, your own probe command, or a built-in probe), stores the reading in a SQLite file inside the repo, and prints one of three words: `helped`, `hurt`, or `baseline`. It prints `baseline` when it has only one reading, because one reading is not a trend. Every reading carries the command that produced it, the population it is out of (`111/112`, never `111`), and the time it was read. A `check_docs` tool re-derives every number your README claims and exits non-zero when a doc and the source disagree. It is not a skill marketplace and it never ranks a change by its name.

## The one workflow, real output

Your eval is this repo's test suite. Two tests pin one rule in MAGNET's own system prompt: "never invent a trend from one reading". Drop the rule, the eval drops by one, MAGNET says `hurt`. Put it back, MAGNET says `helped`. Six commands, nothing simulated (`--no-simulate` on every call). Run on 2026-09-03 13:58 CEST, main @ f690fd0, 21 seconds wall clock. Full transcript: `docs/screenshots/one-workflow.txt`.

```bash
M="python3 -m magnet.cli --log .magnet/demo-one.db"

# 1  baseline: run your eval once, unchanged
$M record pytest-pass-rate
#    recorded pytest-pass-rate: verdict=baseline readings=1

# 2  the one prompt change: drop the rule from SYSTEM_PROMPT in magnet/tools.py
sed -i '' 's/ — never invent a trend from one reading//' magnet/tools.py

# 3  adopt the change, predict "unchanged": MAGNET re-runs the eval
$M adopt prompt 'drop the never-invent rule from SYSTEM_PROMPT' 'pass rate unchanged' --probe pytest-pass-rate --no-simulate
#    latest     111/112  (python3 -m pytest -q --tb=no -m "not slow")
#    verdict    hurt  ↓ -1 vs prior

# 4  put the rule back
git checkout -- magnet/tools.py

# 5  adopt the restore, predict "recovers by 1"
$M adopt prompt 'restore the never-invent rule' 'pass rate recovers by 1' --probe pytest-pass-rate --no-simulate
#    latest     112/112  (python3 -m pytest -q --tb=no -m "not slow")
#    verdict    helped  ↑ +1 vs prior

# 6  the log
$M history
```

The three rows in the log, straight from SQLite (`select id, recorded_at, value, population, change_id from probe_readings`):

```
1|2026-09-03T11:58:00+00:00|112|112|
2|2026-09-03T11:58:07+00:00|111|112|1
3|2026-09-03T11:58:14+00:00|112|112|2
```

132 rather than 133 because one integration test is marked `slow` and the advertised probe command deselects it.

## The A/B: helped, hurt, baseline

| Step | Prediction made before looking | Reading | Verdict | Command |
|---|---|---|---|---|
| baseline | none | 112/112 | `baseline` (1 reading) | `magnet record pytest-pass-rate` |
| drop the rule | "unchanged" | 111/112 | `hurt`, -1 vs prior | `magnet adopt prompt ... --probe pytest-pass-rate --no-simulate` |
| restore the rule | "recovers by 1" | 112/112 | `helped`, +1 vs prior | same, second call |

The first prediction was wrong. The log keeps the prediction next to what happened. That is the point: the author's guess and the measurement sit in the same row.

Scored against ground truth on five scenarios (`magnet eval`): naive 3/5, MAGNET 5/5, silent baseline arm 1/5. The two naive misses are "one reading" (naive says `helped`, truth is `baseline`) and "unchanged" (naive says `helped`, truth is `unchanged`). We ship the arm that embarrasses us.

## How it uses Strands Agents and Amazon Bedrock

- Four tools carry the Strands `@tool` decorator: `run_probe_tool`, `record_week_tool`, `adopt_change_tool`, `check_docs_tool`. File: `magnet/tools.py`, function `build_strands_tools` (lines 115 to 171).
- The agent is a real `strands.Agent` built in `magnet/tools.py`, function `create_agent` (lines 174 to 197): `Agent(tools=..., system_prompt=SYSTEM_PROMPT, callback_handler=None, model=...)`. The system prompt is the one the demo above edits.
- `magnet agent-run` drives that agent. File: `magnet/agent_run.py`, function `run_strands_agent` (lines 106 to 165), which calls `create_agent(...)` and then `agent(AGENT_TASK)`. The SDK's own event loop builds the tool specs from the decorators, dispatches the tools, and feeds the results back until the turn ends. Today's run on main: 12 agent turns, 5 tool dispatches (run_probe, record_week, adopt_change, record_week, check_docs). Command: `magnet agent-run`.
- Three model modes, and the mode is printed at the top of every run:
  - `local` (default): a scripted provider, `magnet/local_model.py`, class `ScriptedLocalModel`, a real implementation of the Strands `Model` base class. No network, no credentials, no spend. The loop, tool registry and dispatch are the SDK's; the token generation is a fixed plan, not a language model.
  - `bedrock`: the same agent with the Strands default model provider, Amazon Bedrock. A language model chooses the tools. Run live on 2026-09-02 from a developer machine in us-east-1: exit 0, 6 agent turns, 5 tool dispatches by the Strands event loop. Receipt: `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`. The receipt does not record the model id; the code passes none, so the SDK default applies, which in the installed `strands-agents` 1.54.0 is the constant `DEFAULT_BEDROCK_MODEL_ID = "global.anthropic.claude-sonnet-4-6"` (command: `python3 -c "from strands.models.bedrock import DEFAULT_BEDROCK_MODEL_ID; print(DEFAULT_BEDROCK_MODEL_ID)"`). Judge guide: `docs/BEDROCK-JUDGE-GUIDE.md`.
  - `none`: the four Python functions called in a fixed order, no agent. The fallback when no model is reachable. A failed agent mode prints a loud banner and marks the result `DEGRADED`; it never swaps silently.
- Installed SDK: `strands-agents` 1.54.0 (`pip show strands-agents`). Dependency declared in `pyproject.toml`.

Which commands go through the agent: `magnet agent-run` only. `magnet record`, `magnet adopt`, `magnet history`, `magnet probe` and `magnet check-docs` call the same four tool functions directly from the CLI, without a model in the loop. The six-command workflow above is therefore deterministic and reproducible; the agent path is the same tools with a model choosing the order.

## Honest limits

- The default agent mode does not prove a language model chose the tool sequence. Only `--model bedrock` does, and that needs AWS credentials and costs money, so it never runs in CI. It was run once, on 2026-09-02, and the receipt is in the repo.
- In that Bedrock run, `check_docs_tool` logged `failed to parse tool input json` once. The run still completed with exit 0. Recorded in the receipt under "WRONG".
- `magnet demo` and `magnet agent-run` place their second reading in a simulated following week so a single run can show a two-reading verdict. Every such reading is labelled `SIMULATED` on screen. The six-command workflow above uses no simulation.
- `pytest` is in the `[dev]` extra, not in the base install. A fresh clone that runs `pip install -e .` and then `pytest` has no pytest in its virtualenv: on a clean machine the command is not found, and on a machine with a system pytest on the path the tests that spawn the verification scripts fail. `pip install -e ".[dev]"` first, then the suite is green: 133 passed (command: `python3 -m pytest -q`, re-derived from tests/test_*.py).
- If pytest is missing, `magnet probe pytest-pass-rate` prints `pytest-pass-rate: None` and exits 0. It should exit non-zero. Not fixed before submission.
- The stack inventory (`magnet stack`, `magnet bakeoff`) runs against a fixture stack shipped in the repo, not against a live machine, so a judge sees the same numbers we do.
- One user so far: the author. The log format and the probe registry are the only surfaces designed for a second team.

## Try it (no keys, about 60 seconds)

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/judge-demo.sh
```

Fresh-clone test, 2026-09-03, main @ f690fd0 in a Python 3.12.5 virtualenv: 24 commands, 23 exit 0, 1 exit 1 (the `pytest` before the dev extra, above). `bash scripts/judge-demo.sh` printed `JUDGE DEMO OK`.

## Built with

- Python 3.10+
- Strands Agents SDK (`strands-agents` 1.54.0)
- Amazon Bedrock (optional live model path)
- SQLite (in-repo log at `.magnet/log.db`)
- pytest (the eval in the demo)

## Links

- Repo: https://github.com/Morkeeth/agents-for-humans (MIT)
- Architecture diagram: `docs/architecture.md`
- One-workflow transcript and screenshots: `docs/screenshots/`
