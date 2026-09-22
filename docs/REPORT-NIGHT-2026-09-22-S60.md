# REPORT · Slice 60 · 2026-09-22

## SHIPPED

- Readout verbs as targets: `amounts to` / `works out to` / `evaluates to` /
  `turns out` / `totals` / `total of` / `registers` / `comes in at` /
  `checks in at` / `posts` / `yields` / `nets` / `returns` (+ word forms).
- Word ordinals `thirteenth`/`fourteenth`/`thirteen`/`fourteen`
  (digit `13th to 14th` already graded).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `amounts to 4/5` @3 | `check_prediction` | missed; naive held |
| `evaluates to` / `posts` / `yields` / `nets` @3 | same | missed |
| `thirteenth to fourteenth` @13/@14 | same | missed / held |
| Suite | `python3 -m pytest -q` | **486 passed, 1 skipped** (487) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **197/197** · embarrassed **112** |
| Scripts | `judge-demo.sh` · `stranger-pass.sh` | JUDGE DEMO OK · stranger pass OK |

## WRONG

- Soft hedges (`roughly`/`approximately`/`about`/`nearly`/`almost` 4/5)
  still unbound — refused, not graded as exact (honesty choice, not done).
- Word ordinals beyond fourteenth (except twentieth) still unbound.
- PNG sidecars not re-rendered (Pillow missing); `.txt` sidecars re-derived.
- Oscar gates still closed.
