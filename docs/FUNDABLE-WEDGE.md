# Fundable wedge · MAGNET · Sep 14 2026

**One sentence:** MAGNET is the adoption log + eval runner that tells professional developers whether their last agent change actually helped — or prints `baseline` instead of inventing a trend.

---

## Problem (pain worth paying for)

Developers on agentic stacks (Cursor, Claude Code, Strands) adopt prompts, models, and skills weekly. Nobody remembers what worked. Naive tooling says `helped` after one reading. Teams ship regressions because eval is manual and memoryless.

**Who pays:** engineering leads running agent evals on production codebases.

**Why now:** Strands Agents hackathon ($40K) validates the category; Agent Grinder (companion product) handles social proof — MAGNET handles measurement.

---

## Wedge (what we ship Sep 14)

| Layer | What | Proof |
|-------|------|-------|
| **Log** | In-repo SQLite (`.magnet/log.db`) — probe readings + adoptions | `magnet history` |
| **Agent** | Strands `@tool` loop: run_probe, record_week, adopt_change, check_docs | `magnet agent-run` |
| **Eval** | Real probes (`pytest-pass-rate`) + registry (`.magnet/probes.json`) | `magnet probe pytest-pass-rate` |
| **Honesty** | baseline when n<2; naive arm in eval; drift gate on docs | `magnet demo` · `magnet eval` · `magnet drift-demo` |

**Not the wedge:** skill marketplace, Helicon-only dependency, fabricated metrics.

---

## Moat (why this is hard to copy badly)

1. **Science ported from measurement-bench** — value/pop, baseline gate, simulated-week flagging.
2. **Embarrassment hunt built in** — `magnet eval` ships the naive and silent_null arms that beat us on scenarios.
3. **Doc drift as product** — `check_docs` re-derives README and judge-doc numbers at read time (Qwen lesson).
4. **Stranger path** — `bash scripts/judge-demo.sh` on cold clone, no keys, CI on every push.

---

## Business model (post-hackathon sketch)

- **Open core:** MIT CLI + SQLite log + 3 built-in probes.
- **Paid:** hosted log sync, team adoption timeline, custom probe templates, Bedrock agent-run in CI.
- **Companion:** Agent Grinder for public receipts (separate repo — not this submission).

---

## Kill bar (investor / judge re-runs this)

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
bash scripts/judge-demo.sh   # must print JUDGE DEMO OK
```

---

## Honest gaps (see hack.md OPEN QUESTIONS)

- Bedrock live path verified on Oscar local only — cloud VM has no AWS creds.
- Demo probe is synthetic; production eval is `pytest-pass-rate` (whole suite, slow on large repos).
- Presentation score 3/5 until Oscar films the 5-min video.

---

## Repro

```bash
python3 -m pytest -q
magnet drift-demo
magnet check-docs
```

Numbers re-derived at object — do not trust this file without running the commands above.
