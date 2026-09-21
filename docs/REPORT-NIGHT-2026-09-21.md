# REPORT · Night 2026-09-21 · Slices 55–57

Branch: `cursor/bare-to-percent-4005` · tip below after push.

## SHIPPED

1. **Slice 55** — bare word destinations (`three to four`) + bare percent
   (`twenty percent` / `20%`) + `by twenty percent` rise intent.
2. **Slice 56** — bare digit / slash destinations (`3 to 4`, `3/5 to 4/5`)
   + mixed word/digit (`3 to four`).
3. **Slice 57** — decimal truncation refuse (`2.5%` was inventing 5) +
   `up to N` ceiling + `down to N` target.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| Bare `three to four` @3 | `check_prediction` | missed; naive held |
| Bare `twenty percent` Δ+20 | same | missed; naive held |
| Bare `3 to 4` @3 | same | missed; naive held |
| `2.5%` not truncated | `claimed_percent("2.5%")` | None (was 5) |
| `up to 4` @5 | `check_prediction` | missed; naive held |
| Suite | `python3 -m pytest -q` | **460 passed, 1 skipped** |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `magnet pred-demo` | **167/167** · embarrassed **85** |
| Cold clone | `git clone … && pip install -e ".[dev]" && magnet demo` | exit 0 |
| Cold suite | same clone `pytest -q` | 460 passed, 1 skipped |

## WRONG

- Assumed `by twenty percent` already graded once pct parsed — intent was
  still unknown → no-direction until S55 forced unsigned percent → rise.
- Mid-slice wrote a failing pytest paste into the screenshot sidecar;
  suite-size math stayed green (7+445+1) while judge-demo went red.
- Decimal percents are refused, not graded — `improves 2.5%` with a rise
  word is still direction-only.
- Ship gate: `git push origin main` → `b62c25906d3d41827c76eeffbe0fc02ef51be63b`.
- Oscar gates (film · Devpost paste · submit) untouched.
- Ordinals / `equals 4/5` named next — not started.
