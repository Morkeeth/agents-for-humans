# REPORT · Slice 56 · 2026-09-21

## SHIPPED

- Bare digit destinations: `3 to 4`, `3/5 to 4/5`, `goes 3 to 4`, `moves 2 to 0`
  grade latest (no `from` required).
- Mixed word/digit: `three to 4`, `3 to four`, `zero to 4` grade the destination.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `3 to 4` @4/@3 | `check_prediction` | held / missed; naive held @3 |
| `3/5 to 4/5` @4/@5 | same | held / missed; naive held @5 |
| `3 to four` @3 | same | missed; naive held |
| Suite | `python3 -m pytest -q` | **452 passed, 1 skipped** (453) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **162/162** · embarrassed **83** |

## WRONG

- Wrote a failing pytest paste into the screenshot sidecar mid-slice; check_docs
  stayed green on suite size (7+445+1=453) while judge-demo went red. Fixed by
  re-deriving a green paste before the final suite run.
- Landed on main @ `b62c259`. Oscar gates still closed.
