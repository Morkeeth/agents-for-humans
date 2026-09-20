# REPORT · Slice 55 · 2026-09-20

## SHIPPED

- Bare word destinations: `three to four`, `goes three to four`, `one to zero`
  grade latest against the named end-state (no `from` required).
- Bare digit destinations: `3 to 4`, `goes 3 to 4`, `3/5 to 4/5`, `zero to one`.
- Bare percent-of-pop: `twenty percent`, `20%`, and `by twenty percent` /
  `by 20%` without a rise word — intent rises; grades Δ vs round(pop·pct/100).
- Perfect `100%` / `100 percent` still refuse percent-of-pop (perfect owns target).
- THE LIE closed: unbound left no-direction while a destination/percent sat on
  the table; absolute Δ=+20 invented held while 20% of pop 5 is +1.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `three to four` @4/@3 | `check_prediction` | held / missed; naive held @3 |
| `3 to 4` / `3/5 to 4/5` | same | destination grades |
| `twenty percent` Δ+20/+1 | same | missed / held; naive held on +20 |
| `by twenty percent` intent | `prediction_intent` | rise (was unknown) |
| `100%` @5/@4 | same | held / missed; pct=None |
| Suite | `python3 -m pytest -q` | re-derived at ship |
| Docs | `magnet check-docs` | re-derived at ship |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **158/158** · embarrassed **79** |

## WRONG

- First bare-`%` draft stole `100%` into percent=100 → flat Δ=0 invents held off
  perfect; caught by running the `100%` @latest=4 object before shipping.
- `exactly twenty percent` still unbound as a target (digit `exactly 20%` grades)
  — left for a later slice; not claimed tonight.
- Curly-apostrophe `won't` still breaks negation (straight `won't` is fine).
- Oscar gates (film · Devpost · submit) untouched; Bedrock still blocked here.
