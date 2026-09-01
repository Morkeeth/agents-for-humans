# Builder.aws draft · MAGNET · do not publish until Oscar edits

**Title:** Agents for Humans: MAGNET — know if your agent change helped, or baseline

**Tags:** #AgentsForHumans #StrandsAgents #AgenticCoding #Evals

---

## Hook

I changed a Cursor skill on Tuesday. My agent felt faster. Was it real?

Most adoption stories stop at "felt better." MAGNET stops at **`baseline`** until two measured readings exist.

---

## The problem

Professional developers run agent stacks — Claude, Cursor, custom Strands agents — and adopt prompts, models, and skills weekly. The field has no adoption memory. Worse: naive evaluators say `helped` after a single probe run. That's how you ship regressions with confidence.

---

## What we built

**MAGNET** (Magnet to YOUR stack) is a Strands Agents SDK agent with four tools:

- `run_probe` — run your eval, return value/pop + repro command
- `record_week` — store readings in an in-repo SQLite log
- `adopt_change` — record what you changed and what you predicted
- `check_docs` — re-derive README numbers; exit non-zero on drift

After a change, the agent re-runs your probe and prints `helped`, `hurt`, or **`baseline`**.

---

## The lesson we had to ship

Our demo deliberately shows the embarrassing case: after one reading, a naive arm says `helped` while MAGNET says `baseline`. Our eval harness includes a silent-null baseline that beats naive on some scenarios. If we can't embarrass ourselves, we're not measuring anything.

---

## Strands + AWS

`magnet agent-run` uses a real Strands event loop — tool specs from `@tool` decorators, dispatch, results fed back until the turn ends. Default mode uses a local scripted model (no AWS spend, CI-safe). For a language model genuinely choosing tools:

```bash
magnet agent-run --model bedrock
```

Requires AWS credentials and Bedrock access. We document both paths honestly.

---

## Try it

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
pip install -e .
magnet demo
```

No keys for the cold path. `bash scripts/stranger-pass.sh` verifies the full loop.

---

## What's next

Social distribution for agent sessions ships separately as [Agent Grinder](https://agentgrinder.vercel.app) — Strava-shaped, human-publish-only. MAGNET is the measurement wedge; Grinder is where you post the run.

---

*Oscar: edit voice, add Bedrock screenshot if you run live path, publish before Sep 14.*
