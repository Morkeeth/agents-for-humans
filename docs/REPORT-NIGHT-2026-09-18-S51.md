# REPORT · Slice 51 · 2026-09-18

## SHIPPED

- Landed S48–S50 (arrow glyphs / climbs-out-of / fat-arrow+word magnitudes) onto
  `cursor/arrow-perfect-night-92a3` from the stalled `arrow-perfect-score-aead` tip.
- **Slice 51:** `gains one` / `gains 1` / `up a point` / `rises a point` /
  `loses one` / `plus 1` / `minus 1` / `adds 1` / `subtracts 1` /
  `regresses by one` now own intent + magnitude.
- THE LIE fixed: rise-with-no-amount invented `prediction-held` on Δ=+20 while
  the claim said magnitude 1. Magnet now misses; naive still holds (embarrassment arm).
- `tests/test_gains_loses_plus_minus.py` · pred-demo scenarios · docs 406→415.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `gains one` amount=1, Δ+20 missed | `python3 -c "…check_prediction('gains one',…20…)"` | prediction-missed; naive held |
| `up a point` amount=1, Δ+20 missed | same pattern | prediction-missed; naive held |
| `plus 1` / `loses one` grade | same | missed on Δ±20; held on Δ±1 |
| Suite green | `python3 -m pytest -q` | **414 passed, 1 skipped** (415 collected) |
| Docs drift | `magnet check-docs` | **16 PASS** |
| Pred-demo FINDING | `magnet pred-demo` | **132/132** magnet · embarrassed **62** |

## WRONG

- Assumed S50 closed the parser surface; running objects after land found
  `gains one` / `up a point` still inventing held — the prior night stopped one
  family too early.
- First `plus 1` intent check looked green in a stale import; only a reload
  showed the truth. Reloaded before trusting.
- Did not yet cold-clone verify this tip (pending push). Bedrock still blocked
  on this VM (no AWS creds) — Oscar gate unchanged.
- `100 percent` / `5 of 5` / `stays green` / `scores 5/5` still unbound — S52+.
