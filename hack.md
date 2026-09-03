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

- Which real eval probes ship for Devpost demo beyond `demo-pass-rate` + `pytest-pass-rate` + stack/bakeoff? (blocking for production, not for cold path)
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
| 10 | Judge path verified + Bedrock local receipt | `judge-demo.sh` cold clone · cloud Bedrock BLOCKED |
| 11 | CI + production adopt + cold-clone verify | `.github/workflows/judge-demo.yml` green · `cold-clone-verify.sh` exit 0 |
| 12 | Drift demo + judge-doc scan + fundable wedge | `magnet drift-demo` exit 0 · check_docs scans 6 judge docs · `docs/FUNDABLE-WEDGE.md` |
| 13 | Stack-magnet + bakeoff vs naive stars/name | `magnet stack` · `magnet fit` · `magnet bakeoff` exit 0 · pytest green |
| 14 | Adopt+fit receipt + stack-coverage probe | `magnet adopt … --fit` prints fills/dupes · `magnet probe stack-coverage` · tests green |
| 15 | Independent-stack replicate + coverage-delta | `magnet replicate` exit 0 · cursor stack loss recorded · `magnet coverage-delta` · CI must-beat on author fixture |
| 16 | Recover demo — cover noise-attracting caps | `magnet recover` shows thin LOST → covered WIN with 0 noise · pytest green |

## NOW

**Slice 16:** Open the independent-stack loss at its object (noise fills planning/writing/design only) · `magnet recover` temp-covers those caps on `fixtures/stack-cursor` · re-runs bakeoff · prints LOST→WIN receipt with 0 noise · must not invent a win on the thin stack.

**Oscar gates:** film video · Devpost paste · submit Sep 14.

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
- 2026-09-02 · Slice 11 fix: pytest-pass-rate excludes `@pytest.mark.slow` · cold-clone test uses `MAGNET_JUDGE_QUICK` · fixes 300s timeout on GitHub cold clone.
- 2026-09-02 · Slice 11 verified: CI green (run 33575676849) · `bash scripts/judge-demo.sh` → JUDGE DEMO OK · `python3 -m pytest -q` → 69 passed.
- 2026-09-02 · Slice 12: check_docs scans 6 judge/devpost docs · found 63→69 drift in 4 files · `magnet drift-demo` · CI cold-clone step · `docs/FUNDABLE-WEDGE.md` · `python3 -m pytest -q` → 73 passed · `magnet check-docs` → 11 claims PASS · `magnet drift-demo` → fake exit 1, real exit 0.
- 2026-09-02 · CI FAIL run 33610787132: `test_log.py` banned word `ledger` in FUNDABLE-WEDGE.md · fixed · `git push origin main` → `024d611`.
- 2026-09-02 · Slice 13 START · opened real object `Morkeeth/mountain-of-helicon` `helicon/magnet.py` (previously cited measurement-bench 404) · EXP-MAGNET-01: name-tiebreak invented 0.875 recall; synonym arm fails; claims must not buy score.
- 2026-09-02 · Slice 13 FAIL then FIX · first `magnet bakeoff` → magnet recall 0.0 (planning/design uncovered; noise "plan a wedding" / "colour palette" filled top-20) · covered those caps on fixtures/stack · `reproduce` stemmed to debug `repro` — rewritten · re-run: magnet 0.5 recall p@3=1.0 noise=0; naive_stars 0.375 with dupes+liar; synonym primary 0/3 claims 3/3 · `python3 -m pytest -q` → 90 passed · check-docs 11 PASS.
- 2026-09-02 · Slice 13 cold clone `/tmp/magnet-cold-s13` (branch) → demo/stack/bakeoff/pytest exit 0 · push `8027d79`.
- 2026-09-02 · Slice 14: `magnet adopt --fit` · `stack-coverage` probe 8/12 · judge-demo step extended · `python3 -m pytest -q` → 98 passed · check-docs 11 PASS.
- 2026-09-02 · **DEFECT found by running:** `tool_adopt_change` applied demo +1/5 whenever probe was `demo-pass-rate`, ignoring `apply_demo_bonus=False` — wine-pairing noise got `helped` while fit said `no-signal`. Fixed: bonus is opt-in only; scripted agent plan passes `apply_demo_bonus=True` explicitly · `python3 -m pytest -q` → 100 passed.
- 2026-09-03 · Slice 14 closed by RUN: `magnet adopt … --fit` → fills-gap/no-signal · `magnet probe stack-coverage` → 8/12 · `bash scripts/judge-demo.sh` → JUDGE DEMO OK · 100 passed on bakeoff branch tip.
- 2026-09-03 · Slice 15 START · opened real objects: `helicon/magnet.py` + `bench/magnet-experiment/RESULTS*.md` + live `~/.cursor/skills-cursor` · canvas skill empty YAML `description:` captured as `metadata:` — frontmatter body fallback fixed.
- 2026-09-03 · Slice 15 FINDING by RUN: `magnet bakeoff --stack fixtures/stack-cursor` → magnet LOST 0.25 vs naive_stars 0.375 (18 noise) · shipped as `magnet replicate` finding, not papered over.
- 2026-09-03 · Slice 15: `magnet replicate` · `magnet coverage-delta` (pdb → attributed 2/12→3/12 debug; wine → nothing-moved) · author must-beat CI · `python3 -m pytest -q` → 109 passed · `magnet check-docs` → 11 PASS.
- 2026-09-03 · Slice 16 START · opened failure object: magnet top-20 on stack-cursor = 18 noise all filling planning/writing/design only.
- 2026-09-03 · Slice 16: `magnet recover` thin LOST 0.25 → covered WIN 0.625 with 0 noise · `python3 -m pytest -q` → 112 passed.
- 2026-09-03 · CI fix: `.github/workflows/judge-demo.yml` now triggers on `cursor/**` pushes — a control that only ran after merge to main was not watching the work · 113 passed.
