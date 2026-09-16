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
| **Prediction check** | Grade free-text prediction vs measured verdict + claimed Δ (held/missed — not attribution) | `magnet adopt` · `magnet pred-demo` · `magnet history` |
| **Stack-bind** | Probes that open the stack object; bind-demo + guide-demo prove repo-blind stays flat | `magnet bind-demo` · `magnet guide-demo` · `magnet probe effort-coverage` |
| **Foreign-bind** | Same bind probes on stacks we did not build; embarrasses naive_title=complete | `magnet foreign-bind` · `bash scripts/foreign-stack.sh` |
| **Foreign-harden** | Closed loop: title-complete at near-zero → UG apply on working copy → magnet helped | `magnet foreign-harden` |
| **Foreign-hurt** | Strip hardening → magnet hurt while naive invents helped from the title | `magnet foreign-hurt` |
| **Hooks-layout** | Opens `hooks/hooks.json` (superpowers object); layout ≠ UG hook-coverage | `magnet probe hooks-layout` |
| **Magnitude honesty** | Claimed `rises by 2/5` with measured Δ +1 → magnet missed; naive direction invents held | `magnet pred-demo` |
| **Stay-at honesty** | Claimed `must stay at 5/5` with latest 4/5 → magnet missed; naive flat invents held | `magnet pred-demo` |
| **Absolute-level honesty** | `must stay at 5` (no `/pop`), `remain at` / `hold at`, floor `at least 4/5` — magnet misses wrong levels; naive invents held | `magnet pred-demo` |
| **Real-week default** | Bare `magnet adopt` uses a real `read_at`; `--simulate` is the labelled demo opt-in | `magnet adopt … --demo-bonus --reset` |
| **Vacuous RED** | Empty/missing skills → `n/a` exit 1; `allow:[]` alone ≠ hook 1/2; naive still prints 0/0 success | `magnet vacuous-demo` |
| **Sidecar outcome** | history/one-workflow Devpost shots must carry prediction outcome or check_docs goes RED | `magnet check-docs` |
| **Recover lexicon** | Devpost prediction `pass rate recovers by 1` grades rise+magnitude (was no-direction) | `bash scripts/one-workflow.sh` · `magnet pred-demo` |
| **Honest pytest paste** | Screenshot `N passed, M skipped` sums to suite size — control no longer forces inventing `N+M passed` | `magnet check-docs` |
| **Receipt verify** | `magnet receipt --verify` re-probes; planted SQLite drift goes RED (Grinder bridge) | `magnet receipt-demo` |
| **Grinder evidence** | `magnet receipt --grinder` exports evidence without inventing COUNT_FIELDS; verify RED refuses export | `magnet receipt --grinder` |
| **Negation honesty** | `won't fall` / `does not regress` are flat — NOT fall; old magnet invented held when the score dropped | `magnet pred-demo` |
| **Ceiling honesty** | Dual of floor: `at most 3/5` held when latest ≤ ceiling; naive flat invents held above | `magnet pred-demo` |
| **Target-level honesty** | `falls to 2/5` / `reaches 5/5` grades latest; direction alone invents held on wrong target | `magnet pred-demo` |
| **Percent-of-pop honesty** | `improves by 20%` grades Δ vs round(pop·pct/100) — never absolute points | `magnet pred-demo` |
| **Exactly-level honesty** | `exactly 4/5` grades latest; was no-direction | `magnet pred-demo` |
| **Doubles/halves honesty** | `doubles`/`halves` grade prior=latest−Δ; direction invents held on non-double rise | `magnet pred-demo` |
| **Below-bound floor honesty** | `won't fall below 3/5` opens floor; unchanged@latest=2 no longer invents held | `magnet pred-demo` |
| **Percent syntax + triples** | `rises 20%` parses without `by`; triples/3x grade prior | `magnet pred-demo` |
| **Word-percent + never/cannot** | `20 percent` ≠ absolute 20; `never falls`/`won't decrease` → flat (not fall) | `magnet pred-demo` |

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
