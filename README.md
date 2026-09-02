# MAGNET · Agents for Humans

**Professional Agents track · AWS Strands · Devpost Sep 14 2026**

> **Judges — start here:** `bash scripts/judge-demo.sh` (60s, no keys) · scorecard: `docs/JUDGE-SCORECARD-2026-09-02.md` · Bedrock receipt: `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`

> After you change a prompt, model, or skill, a background agent re-runs your eval and tells you
> whether it helped — or prints **`baseline`** instead of inventing a trend.

**Constraint:** No number without the command, population, and timestamp (`3/5`, never `3`).

## Quick start

```bash
pip install -e .
magnet init
magnet demo
magnet list-probes    # built-in + your .magnet/probes.json
magnet history        # adoption timeline from SQLite
magnet stack          # inventory YOUR agent surfaces (fixtures/stack cold path)
magnet bakeoff        # magnet vs naive_stars vs naive_name vs silent_null
```

Cold path — no keys, no network:

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
pip install -e .
magnet demo
magnet stack
magnet bakeoff
magnet adopt skill my-skill "pass rate rises by 1/5" --demo-bonus --reset
magnet history
```

## Probes

| Probe | What it measures |
|-------|------------------|
| `demo-pass-rate` | Synthetic 3/5→4/5 demo (skill_bonus in SQLite) |
| `check-docs` | README claims vs source (re-derived at read time) |
| `pytest-pass-rate` | **Real eval** — runs `pytest -q`, counts passed/total |
| `stack-coverage` | YOUR stack: covered/total capability vocabulary |

Add your own via `.magnet/probes.json` (copy from `docs/probes.json.example`):

```bash
magnet probe my-custom-eval
magnet list-probes
```

## Strands agent · 4 tools

`magnet agent-run` drives these four tools with a **real `strands.Agent` event loop**:
the SDK builds the tool specs from the `@tool` decorators, dispatches the tools, and
feeds the results back until the turn ends.

| Tool | Job |
|------|-----|
| `run_probe` | Run your eval; return value/pop + repro command |
| `record_week` | Store this week's reading in the SQLite log |
| `adopt_change` | Record a prompt/model/skill change + prediction |
| `check_docs` | Re-derive README numbers; exit non-zero on drift |

The log lives in-repo at `.magnet/log.db` — not Helicon-only.
(A `.magnet/ledger.db` from an earlier build is migrated in place on first run.)

## Verify

```bash
pytest
magnet check-docs
magnet drift-demo   # live Qwen lesson: fake repo fails, real repo passes
magnet eval          # naive vs magnet vs silent_null on 5 scenarios
magnet bakeoff       # magnet vs naive_stars vs naive_name vs silent_null on fixtures
magnet stack         # inventory YOUR surfaces + gaps
magnet agent-run     # real Strands agent loop, local model, no network, no spend
magnet list-probes   # built-in + registry probes
magnet history       # adoption timeline from .magnet/log.db
magnet probe pytest-pass-rate   # real eval (run from CLI, not inside pytest)
```

### Which model runs the agent

| `--model` | What runs | Needs credentials | Costs money |
|---|---|---|---|
| `local` *(default)* | Real Strands agent loop; the model is a **local scripted provider**, not an LLM — it replays a fixed plan | no | no |
| `bedrock` | Real Strands agent loop with **Amazon Bedrock** — a language model genuinely choosing the tools | **yes** (AWS creds + region + Bedrock model access) | **yes** |
| `none` | Deterministic chain, no agent at all — the fallback when no model is reachable | no | no |

The mode is printed at the top of every run, and a failed agent mode prints a loud
banner and marks the result `DEGRADED`. It never swaps silently.

**Honest scope:** `--model local` proves the loop, the tool registry and the tool
dispatch are real Strands. It does **not** prove an LLM chose the sequence. To see
that, run `magnet agent-run --model bedrock` with your own AWS credentials. That path
has never been run in this repo's CI.

See `hack.md` for the build contract and `docs/architecture.md` for the flow diagram.
