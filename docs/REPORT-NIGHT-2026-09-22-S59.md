# REPORT · Slice 59 · 2026-09-22

## SHIPPED

- Fixed THE LIE: `same as 4/5` was flat (`same`) with no target → invents
  prediction-held at any latest. Now grades destination.
- Bound level copulas/readouts: `is`/`was`/`are`/`reads`/`reads as`/
  `measures`/`measures at`/`matches`/`identical to`/`lands on`/
  `settles on`/`finishes at`/`comes to`/`comes out to`/`stands at`/
  `sits at`/`clocks in at` (+ word destinations).
- Word ordinals `eleventh`/`twelfth`/`eleven`/`twelve` (digit `11th`/`12th`
  already graded).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `same as 4/5` @4/@3 | `check_prediction` | held / missed; naive held @3 |
| `is 4/5` / `reads 4/5` / `matches 4/5` @3 | same | missed; naive held |
| `eleventh to twelfth` @11 | same | missed; naive held |
| `same as four` @3 | same | missed |
| Suite | `python3 -m pytest -q` | **479 passed, 1 skipped** (480) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **187/187** · embarrassed **102** |
| Scripts | `judge-demo.sh` · `stranger-pass.sh` | JUDGE DEMO OK · stranger pass OK |

## WRONG

- Readout verbs still unbound: `amounts to` / `works out to` / `evaluates to` /
  `totals` / `registers` / `comes in at` / `posts` / `yields` / `nets` —
  left for Slice 60 after re-deriving at the object.
- Word ordinals stop at twelfth (plus twentieth); `thirteenth to fourteenth`
  unbound while `13th to 14th` grades.
- Soft hedges (`roughly`/`approximately`/`about`/`nearly`/`almost` 4/5)
  unbound — refused rather than inventing exact held; not claimed as done.
- Oscar gates still closed.
