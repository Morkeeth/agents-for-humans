---
doc: hack
project: MAGNET · Agents for Humans
phase: BUILD
event: AWS Strands · Devpost · Sun 14 Sep 2026 17:00 PDT · $40K
track: Professional Agents
ruling: Option A · MAGNET · Oscar 29 Aug 2026
---

# MAGNET — hack.md

> **Magnet to YOUR stack** — not a skill marketplace. After you change a prompt, model, or skill,
> a background agent re-runs **your** eval and prints helped/hurt/baseline.

## ⭐ NORTH STAR

The field has too many skills and no memory of what they did. MAGNET is the adoption log +
eval runner for **your** agent stack.

## PROMISE LINE

After you change a prompt, model, or skill, a background agent re-runs your eval and tells you
whether it helped — or prints **`baseline`** instead of inventing a trend.

## CONSTRAINT

No number without the command that produced it, the population it is out of, and when it was read.
(`3/5`, never `3`.)

## OPEN QUESTIONS

- Which real eval probes ship for Devpost demo beyond `demo-pass-rate`? (blocking for production, not for cold path)
- Bedrock model ID for live Strands agent run? (Oscar click — not resolved here)

## CONSTITUTION

1. Promise line before code.
2. Port science from `measurement-bench` — do not rewrite.
3. In-repo SQLite adapter — NOT Helicon-only.
4. MIT licence.
5. No AWS spend beyond free tier without Oscar click.
6. No register/submit/video — Oscar only.

## PLAN (risk-first)

| # | Slice | Done when |
|---|-------|-----------|
| 0 | Repo + README + architecture diagram | clone works |
| 1 | Strands agent · 4 tools | `magnet demo` cold-runs |
| 2 | Port kernel from measurement-bench/magnet.py | tests green |
| 3 | Core loop: adopt → re-run → delta receipt | demo end-to-end |
| 4 | Stranger pass doc | STRANGER-PASS.md with command output |
| 5 | Eval harness + agent-run + check_docs pytest drift | `magnet eval` + `magnet agent-run` exit 0 |
| 6 | Real pytest probe + registry + history | `magnet probe pytest-pass-rate` + `magnet list-probes` + `magnet history` exit 0 |
| 7 | `magnet adopt` + stranger-pass script | `bash scripts/stranger-pass.sh` exit 0 |
| 8 | Devpost pack + film scout | DEVPOST-READY + FILM-SCOUT + OSCAR-CLICK-LIST on disk |
| 9 | Judge-winning path | `scripts/judge-demo.sh` + JUDGE-SCORECARD + DEVPOST-DESCRIPTION |

## NOW

**Slice 10 (shipped):** Judge path verified · `judge-demo.sh` PATH fix for cold clone · `test_judge_demo.py` regression · Bedrock live on Oscar local (5 tools) · cloud VM Bedrock BLOCKED (`NoCredentialsError`) · `_NIGHT-SCOPE.md` · `_HACK-CONTRACT.md` · 63 pytest · Technical 5/5.

**Oscar gates:** film video (lifts Presentation to 5) · Devpost paste · submit Sep 14.

## LOG

- 2026-08-29 · Repo created · cloud ambitious lane launched.
- 2026-08-29 · `fleet-ops/plans/agents-for-humans-hack.md` not accessible (404) · reporter science from `helicon/measure.py` (mountain-of-helicon).
- 2026-08-29 · Merged scaffold from `cursor/magnet-adoption-ledger-080a` into main worktree.
- 2026-08-29 · Demo enhanced: 1-reading embarrassing case (naive `helped` vs magnet `baseline`) · `python3 -m pytest -q` → 17 passed · `magnet demo` → exit 0.
- 2026-08-29 · `test_check_docs_drift.py` added · drift on fake `99 tools` claim exits 1.
- 2026-08-29 · Strands Bedrock agent loop not run — no AWS credentials in cloud VM.
- 2026-08-29 · `git push origin main` → `e798729` · GitHub cold clone `/tmp/magnet-github-cold` → `magnet demo` exit 0 · `pytest -q` → 17 passed.
- 2026-08-30 · Slice 5: `magnet/eval.py` (naive 3/5, magnet 5/5, silent_null 1/5) · `magnet/agent_run.py` (4-tool chain no Bedrock) · check_docs re-derives pytest count from `tests/test_*.py` · `python3 -m pytest -q` → 26 passed · `python3 -m magnet.cli eval` → exit 0 · `python3 -m magnet.cli agent-run` → exit 0 · `python3 -m magnet.cli check-docs` → exit 0 (after doc counts updated).
- 2026-08-30 · `git push origin main` → `f74799d` · GitHub cold clone `/tmp/magnet-cold-post` → 26 passed · demo/eval/agent-run/check-docs exit 0.
- 2026-09-01 · Slice 6-7 shipped · `git push origin main` → `2d38525` · cold clone `/tmp/magnet-cold-final` → 61 passed · `bash scripts/stranger-pass.sh` → exit 0 · `magnet demo` → helped receipt.
- 2026-09-02 · Slice 8: Devpost pack (EYES ruling: MAGNET submits, Grinder product) · `bash scripts/stranger-pass.sh` → OK · docs/DEVPOST-READY, FILM-SCOUT, OSCAR-CLICK-LIST, BUILDER-AWS-DRAFT, MOONSHOT-MEMO · architecture AWS section.
- 2026-09-02 · Slice 9: Judge path · `bash scripts/judge-demo.sh` → JUDGE DEMO OK · JUDGE-SCORECARD (4.0/5 honest) · DEVPOST-DESCRIPTION paste · BEDROCK-JUDGE-GUIDE · pushed main.
- 2026-09-02 · **Live Bedrock (local)** · `magnet agent-run --model bedrock` exit 0 · 5 tools dispatched · `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md` · Technical 5/5.
- 2026-09-02 · Slice 10: Cloud VM · `bash scripts/judge-demo.sh` → JUDGE DEMO OK · `python3 -m pytest -q` → 63 passed · STS → `NoCredentialsError` · cloud Bedrock BLOCKED.
- 2026-09-02 · Slice 10 fix: `judge-demo.sh` PATH (`~/.local/bin`) — cold clone was failing `magnet: command not found` · `tests/test_judge_demo.py` (2 tests) · cold clone `/tmp/magnet-cold-judge-post-push` → JUDGE DEMO OK.
