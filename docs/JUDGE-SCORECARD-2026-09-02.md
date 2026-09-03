# Judge scorecard · MAGNET · 2026-09-02

Honest self-score against [Devpost criteria](https://agentsforhumans.devpost.com/). Re-run evidence yourself — do not trust this file.

**One-command proof:** `bash scripts/judge-demo.sh`

---

## Summary

| Criterion | Score (1-5) | After tonight | Judge re-runs |
|-----------|-------------:|--------------:|---------------|
| Technical Implementation | 5 | 5 | `magnet agent-run --model bedrock` · `pytest -q` |
| Design | 4 | 4 | `magnet demo` · `magnet history` |
| Potential Impact | 4 | 4 | read Problem below · `magnet adopt` |
| Creativity & Originality | 5 | 5 | `magnet eval` · naive vs magnet |
| Presentation | 3 | 3 | video Oscar films · `docs/FILM-SCOUT-COMMANDS.md` |
| **Weighted avg** | **4.2** | **4.2** | |

Presentation is 3 until 5-min video exists. Live Bedrock demonstrated locally — see `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`.

---

## 1. Technical Implementation

**Judge question:** How thoroughly does the project use Strands Agents? Working, non-trivial? AWS strengthens score?

| Evidence | Command |
|----------|---------|
| Real `strands.Agent` event loop | `magnet agent-run` → `MODE: strands agent loop` |
| 4 `@tool` functions registered | `magnet check-docs` → tool count 4 |
| 133 automated tests | `python3 -m pytest -q` |
| Bedrock path (live) | `magnet agent-run --model bedrock` — see `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md` |
| Stranger verification | `bash scripts/stranger-pass.sh` |
| CI on every push | `.github/workflows/judge-demo.yml` |
| Production adopt | `magnet adopt --probe pytest-pass-rate` in judge-demo step 5/7 |

**Gap:** Live Bedrock verified 2026-09-02 on Oscar local machine — see receipt. CI and cloud VM still use local scripted mode (`NoCredentialsError` on cloud STS check).

**Score: 5/5** — genuine Strands + live Bedrock demonstrated (local). Judges without AWS creds use `magnet agent-run` default.

---

## 2. Design

**Judge question:** Complete product experience, not just PoC?

| Evidence | Command |
|----------|---------|
| One-command demo | `magnet demo` |
| Full adopt → probe → re-probe → receipt | `magnet adopt` + `magnet history` |
| Docs drift as product feature | `magnet check-docs` |
| Probe registry for YOUR stack | `magnet list-probes` · `.magnet/probes.json.example` |
| Architecture diagram | `docs/architecture.md` |

**Score: 4/5** — CLI-complete; no web UI (acceptable for Professional Agents track).

---

## 3. Potential Impact

**Repetitive task eliminated:** After every prompt/model/skill change, developers manually re-run evals and guess if it helped.

**Who:** Professional developers on agentic coding stacks (Claude, Cursor, Strands).

**Demonstrated:** `magnet demo` shows the failure mode (naive `helped` on 1 reading) and the fix (`baseline` until 2 readings).

**Score: 4/5** — credible problem; production probes beyond demo are OPEN in hack.md.

---

## 4. Creativity & Originality

**Non-obvious Strands use:** Agent as **eval re-runner + receipt printer**, not chatbot or marketplace.

**Embarrassment hunt shipped:** `magnet eval` shows `silent_null` beating naive on scenarios.

| Evidence | Command |
|----------|---------|
| Naive baseline arm | `magnet demo` — first block |
| Eval harness | `magnet eval` |
| check_docs anti-Qwen-lesson | README drift → exit 1 |

**Score: 5/5** — we ship the arm that makes us look worse.

---

## 5. Presentation

| Evidence | Status |
|----------|--------|
| `docs/DEVPOST-DESCRIPTION.md` | paste-ready |
| `docs/FILM-SCOUT-COMMANDS.md` | 5-min script |
| `docs/SCREENSHOTS.md` | capture guide |
| Demo video | **Oscar gate** — not recorded |
| Live demo URL | N/A (CLI product) |

**Score: 3/5** — all prep on disk; video is the gap.

---

## What would NOT win (honest)

- Submitting Agent Grinder as primary (no Strands — fails tech gate)
- Claiming Bedrock was demonstrated if only local scripted mode filmed
- Scorecard with all 5s and no commands

---

## Morning path to 4.5+ average

1. Oscar films `bash scripts/judge-demo.sh` + narration from FILM-SCOUT
2. `magnet agent-run --model bedrock` on camera (local receipt proves path works)
3. Paste `docs/DEVPOST-DESCRIPTION.md` into Devpost
4. Publish `docs/BUILDER-AWS-DRAFT.md` on builder.aws (+0.6 bonus)
