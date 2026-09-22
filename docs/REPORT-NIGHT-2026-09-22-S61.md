# REPORT · Slice 61 · 2026-09-22

## SHIPPED

- Word ordinals `fifteenth`…`nineteenth` and cardinals `fifteen`…`nineteen`.
- Closes the teens pack against digit forms that already graded (`15th`…`19th`).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `fifteenth to sixteenth` @15 | `check_prediction` | missed; naive held |
| `seventeenth to eighteenth` @17 | same | missed |
| `nineteenth to twentieth` @19/@20 | same | missed / held |
| `fifteen to sixteen` @15 | same | missed |
| Suite | `python3 -m pytest -q` | **492 passed, 1 skipped** (493) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **201/201** · embarrassed **116** |
| Scripts | `judge-demo.sh` · `stranger-pass.sh` | JUDGE DEMO OK · stranger pass OK |

## WRONG

- Soft hedges (`roughly`/`about`/`nearly` 4/5) still unbound — refuse, not exact.
- Word ordinals beyond twentieth still unbound.
- Oscar gates still closed.
