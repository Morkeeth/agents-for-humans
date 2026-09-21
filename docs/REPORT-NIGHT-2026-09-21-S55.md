# REPORT · Slice 55 · 2026-09-21

## SHIPPED

- Bare word destinations: `three to four`, `goes three to five`, `one to zero`
  grade latest against the named end-state (no `from` required).
- Bare percent-of-pop: `twenty percent`, `20 percent`, `20%` parse and grade
  as rise; `by twenty percent` no longer stuck at no-direction.
- Signed word percent: `+twenty percent` / `-twenty percent` own rise/fall.
- Perfect unbound (`100%` / `100 percent`) guarded — not stolen as percent.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `three to four` @4/@3 | `check_prediction` | held / missed; naive held @3 |
| `twenty percent` Δ+1/+20 | same | held / missed; naive held on +20 |
| `20%` Δ+20 | same | missed; naive held |
| `100%` perfect not stolen | `claimed_percent` / `claimed_target` | pct=None · perfect=True |
| Suite | `python3 -m pytest -q` | **445 passed, 1 skipped** (446) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **157/157** · embarrassed **79** |

## WRONG

- First assumed `by twenty percent` already graded once pct parsed — wrong;
  intent stayed unknown → no-direction until Slice 55 forced unsigned percent → rise.
- Bare digit `3 to 4` / `3/5 to 4/5` still unbound — next slice, not claimed tonight.
- Landed on main @ `b62c259`. Oscar gates (film · Devpost paste · submit) still closed.
