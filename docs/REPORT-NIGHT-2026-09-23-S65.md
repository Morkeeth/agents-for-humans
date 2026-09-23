# REPORT · Slice 65 · 2026-09-23

## SHIPPED

- Decade compounds `thirty`…`ninety` (+ `thirty-one`…`ninety-nine` and ordinals).
- `one hundred` / `a hundred` / `hundred` → 100.
- Builder `_build_word_levels()` generates compounds so we never hardcode drift.
- Fixes THE LIE: `ninety-nine to one hundred` stole `nine→one` dest=1 held @1.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `ninety-nine to one hundred` @1/@100 | `check_prediction` | missed / held; naive held @1 |
| `thirty-one to thirty-two` @30 | same | missed |
| `from thirty to thirty-one` @30/@31 | same | missed / held |
| `twenty-nine to thirty` @29/@30 | same | missed / held |
| S63 regression `twenty-one to twenty-two` | `claimed_target` | dest=22 |
| Suite | `python3 -m pytest -q` | **529 passed, 1 skipped** (530) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **225/225** · embarrassed **136** |

## WRONG

- `more or less` / `or so` / `-ish` soft hedges still unbound.
- Word forms above hundred (`one hundred and one`) still unbound.
- Oscar gates still closed.
