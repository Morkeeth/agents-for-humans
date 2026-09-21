# REPORT · Slice 57 · 2026-09-21

## SHIPPED

- Decimal truncation refuse: `2.5%` / `50.5%` / `by 1.5` / `+1.5` no longer
  invent pct=5 or amount=1 from a fractional digit — unbound instead.
- `up to N` is a ceiling (not rise); `down to N` is a target (not fall-only).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `2.5%` / `50.5%` | `claimed_percent` | pct=None (was 5) |
| `by 1.5` / `rises by 1.5` | `claimed_magnitude` | amount=None (was 1) |
| `20%` / `rises by 1` | same | still grade (regression) |
| `up to 4` @4/@5 | `check_prediction` | held / missed; naive held @5 |
| `down to 2` @2/@3 | same | held / missed; naive held @3 |
| Suite | `python3 -m pytest -q` | **460 passed, 1 skipped** (461) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **167/167** · embarrassed **85** |

## WRONG

- Found the decimal lie by probing after S56 — it was not in hack.md NOW;
  carrying only the named next slice would have missed it.
- Decimals are refused, not graded; a stranger claiming `improves 2.5%`
  still gets direction-only if a rise word is present — we do not yet
  parse real fractional percents.
- Landed on main @ `b62c259`. Oscar gates (film · Devpost · submit) still closed.
