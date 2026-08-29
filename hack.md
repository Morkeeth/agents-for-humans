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

The field has too many skills and no memory of what they did. MAGNET is the adoption ledger +
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

| # | Slice | Done when | Status |
|---|-------|-----------|--------|
| 0 | Repo + README + architecture diagram | clone works | ✅ `docs/architecture.md` |
| 1 | Strands agent · 4 tools | `magnet demo` cold-runs | ✅ exit 0 |
| 2 | Port kernel from measurement-bench/magnet.py | tests green | ✅ 14 pytest (via helicon.measure science) |
| 3 | Core loop: adopt → re-run → delta receipt | demo end-to-end | ✅ helped ↑ +1 |
| 4 | Stranger pass doc | STRANGER-PASS.md with command output | ✅ |

## NOW

**Slice 4 (done):** Stranger pass — `docs/STRANGER-PASS.md` filled from cold run.

## LOG

- 2026-08-29 · Repo created · cloud ambitious lane launched.
- 2026-08-29 · `fleet-ops/plans/agents-for-humans-hack.md` not accessible (404) · used mountain-of-helicon `helicon/measure.py` for reporter science instead of `measurement-bench/magnet.py`.
- 2026-08-29 · First `tools.py` edit corrupted import line · fixed before commit.
- 2026-08-29 · `pytest -q` → 15 passed · `magnet demo` → exit 0 · cold copy in `/tmp/magnet-cold` → exit 0.
- 2026-08-29 · Strands Bedrock agent loop not run — no AWS credentials in cloud VM.
