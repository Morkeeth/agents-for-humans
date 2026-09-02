# Devpost description · paste into submission form

Copy sections below into Devpost. Trim if character limits hit.

---

## Project name

MAGNET — know if your agent change helped, or baseline

---

## Elevator pitch (short)

After you change a prompt, model, or skill, MAGNET's Strands agent re-runs your eval and prints `helped`, `hurt`, or **`baseline`** — never a trend from one reading.

---

## About the project

### The problem

Professional developers change agent prompts, models, and skills constantly. After each change, they manually re-run evals and guess whether it helped. Most tools say `helped` after a single reading — that's optimism, not measurement.

### Who it's for

Developers running agentic coding stacks: Claude Code, Cursor, custom Strands agents. **Professional Agents** track.

### Why it matters

Without an adoption log and honest baselines, every "improvement" is vibes. Teams ship regressions with confidence. MAGNET is the eval runner and receipt printer for **your** stack — not a skill marketplace.

### How it works

MAGNET uses the **Strands Agents SDK** with four tools:

1. **run_probe** — execute your eval, return value/pop + repro command  
2. **record_week** — store readings in an in-repo SQLite log  
3. **adopt_change** — log what you changed and what you predicted  
4. **check_docs** — re-derive README numbers; exit non-zero on drift  

After a change, the Strands agent re-runs the probe and prints `helped`, `hurt`, or **`baseline`** (fewer than two readings).

### The embarrassing demo

`magnet demo` deliberately shows naive `helped` on one reading while MAGNET says `baseline`. `magnet eval` includes a silent-null arm that beats naive on some scenarios. We ship what embarrasses us.

### AWS

Default mode uses a local scripted Strands model (no spend, CI-safe). Judges with AWS credentials can run:

```bash
magnet agent-run --model bedrock
```

See `docs/BEDROCK-JUDGE-GUIDE.md`.

### Try it (judges)

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
bash scripts/judge-demo.sh
```

90 pytest tests · MIT license · no keys required for cold demo.

---

## Built with

- Python 3.10+
- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- SQLite (in-repo adoption log)
- Amazon Bedrock (optional live agent path)

---

## Track

Professional Agents

---

## Link to companion work (optional footnote)

Social layer for posting agent sessions (separate product, not this submission): [Agent Grinder](https://agentgrinder.vercel.app)
