# Night report · 2026-09-17 · Ambition wave S48–S50

**branch:** `cursor/arrow-perfect-score-aead`  
**tip:** `321003b154d6349d8f0540eecc8f51ee327e49ba`

## SHIPPED

What exists now that did not at the start of this night wave:

1. **Slice 48** — arrow glyphs `↑1`/`↓1` intent+magnitude; unbound `perfect score`→population.
2. **Slice 49** — `climbs 1`/`slips 1` magnitude; `grows`/`shrinks` intent; `5 out of 5`/`score of`/`full marks`/`100%`/`tops out`/`caps at`.
3. **Slice 50** — fat arrows `⬆▲▼`; word magnitudes `by one`/`one point`; `all green`/`all passing`.
4. Embarrassment arms throughout: naive invents held; magnet misses (pred-demo embarrassed 56/123).
5. Doc claims re-derived at source: **373 → 406**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| ↑1 / ↓1 | ran `prediction_intent` / `claimed_magnitude` | rise/fall · amount=1 |
| perfect score@4 | `check_prediction(..., pop=5, latest=4)` | magnet missed / naive held |
| climbs 1 @+20 | same | magnet missed / naive held |
| 5 out of 5 | `claimed_target` | 5/5 |
| ⬆1 / up by one | objects + pred-demo rows | missed on absolute lie |
| Suite | `python3 -m pytest -q` | 405 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 123/123 · embarrassed 56 · FINDING |
| check_docs | `magnet check-docs` | 16 PASS |
| demo | `magnet demo` | exit 0 |
| judge-demo | `bash scripts/judge-demo.sh` | JUDGE DEMO OK |

## WRONG

1. Assumed early that `↑1/5` already had intent — it had amount only; intent was the real gap.
2. First check-docs sidecar write via `tee` truncated mid-scan (15 PASS vs 16) — had to lock after a completed run.
3. Cold clone of dirty worktree showed S49 numbers before S50 commit — always push then clone the tip.
4. Could not `git push origin main` — cloud agent ships feature branch; PR auto-create blocked for Oscar click.
5. Bedrock still BLOCKED (no AWS creds on cloud VM).
6. Oscar gates untouched: film · Devpost paste · submit.
7. Fat-arrow double forms `⇈`/`⇊` shipped but less common in the wild — may be overfit.
8. Bare `by one` still intent=unknown (amount grades only when rise/fall word present) — left as-is; not a lie inventing held.
