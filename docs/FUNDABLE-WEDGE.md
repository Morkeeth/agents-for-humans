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
| **Stack fit** | Inventory YOUR surfaces; rank a local candidates file against YOUR gaps | `magnet stack` · `magnet bakeoff` |
| **Closed loop** | Install a local skill into a working copy → re-measure coverage → magnet vs naive-install | `magnet stack-demo` · `magnet adopt --install` |
| **External honesty** | Open stacks we did not build; refuse title-only complete; redact-scan can go RED | `magnet external-stack` · `magnet redact-scan` · `docs/EXTERNAL-STACK-RECEIPT.md` |
| **Prediction check** | Grade free-text prediction vs measured verdict (held/missed — not attribution) | `magnet adopt` · `magnet history` |
| **Stack-bind** | Probes that open the stack object; bind-demo + guide-demo prove repo-blind stays flat | `magnet bind-demo` · `magnet guide-demo` · `magnet probe effort-coverage` |

**Not the wedge:** skill marketplace crawl, Helicon-only dependency, fabricated metrics.

---

## Moat (why this is hard to copy badly)

1. **Science ported from measurement-bench / helicon.magnet** — value/pop, baseline gate, gap-fit ranking with no name tie-break.
2. **Embarrassment hunt built in** — `magnet eval` and `magnet bakeoff` ship arms that can beat us (silent_null, naive_stars); `magnet redact-scan` can fail this repo; `naive_title` invents complete on foreign stacks.
3. **Doc drift as product** — `check_docs` re-derives README and judge-doc numbers at read time (Qwen lesson).
4. **Stranger path** — `bash scripts/judge-demo.sh` on cold clone, no keys, CI on every push.
5. **Open the object** — foreign-stack / Agent Grinder receipts measured at the clone, not the README.

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
- Bakeoff synonym primary recovered **3/3** under TAG_VOCAB 1.1 (was 0/3); wine-liar still False — re-derive with `magnet bakeoff`.
- Companion product Agent Grinder stack covers **1/12** capabilities when opened as an object (`magnet probe stack-coverage --stack fixtures/real-stacks/agentgrinder`) — writing only.
- Presentation score 3/5 until Oscar films the 5-min video.

---

## Repro

```bash
python3 -m pytest -q
magnet drift-demo
magnet check-docs
```

Numbers re-derived at object — do not trust this file without running the commands above.
