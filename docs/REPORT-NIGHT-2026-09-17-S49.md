# Night report · 2026-09-17 · Slice 49

**branch:** `cursor/arrow-perfect-score-aead`

## SHIPPED

1. **`climbs 1` / `slips 1`** — magnitude (closes direction-invented-held on Δ=+20).
2. **`grows by N` / `shrinks by N`** — rise/fall intent (closes no-direction with amount on table).
3. **`5 out of 5` / `score of N/N`** — targets; **`full marks` / `100%`** — perfect→pop; **`tops out at` / `caps at`** — target/ceiling.
4. **pred-demo** — 113/113 · embarrassed 49.
5. Doc claims re-derived **386 → 398**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| climbs 1 | `claimed_magnitude` / `check_prediction(..., 20)` | amount=1 · magnet missed / naive held |
| grows by 1 | `prediction_intent` | rise |
| 5 out of 5 | `claimed_target` | 5/5 · missed@4 |
| 100% | `claimed_target` perfect | missed@4 / naive held |
| Suite | `python3 -m pytest -q` | 397 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 113/113 · embarrassed 49 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- Fat arrows `⬆1` / `▲1` / `▼1` still unbound.
- Word magnitudes (`by one` / `one point`) still unbound.
- Bedrock BLOCKED on cloud VM.
- Oscar gates remain: film · Devpost paste · submit.
- PR auto-create blocked — Oscar UI click; branch pushed.
- SHIP GATE asked for `git push origin main`; this environment ships via feature branch.
