# Night report · 2026-09-17 · Slice 46

**branch:** `cursor/negated-rise-shall-b0b0`

## SHIPPED

1. **Bare `+1` / `-1` / `pass rate +1` intent** — sign owns rise/fall (word-boundary gap).
2. **`(?!\\d)` on signed parser** — `-20%` no longer backtracks into amount=-2.
3. **Embarrassment** — magnet misses on Δ=+20; naive holds.
4. **pred-demo** — 89/89 · embarrassed 35.
5. Doc claims re-derived **354 → 362**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| +1 intent | `prediction_intent("+1")` | rise |
| -1 intent | `prediction_intent("-1")` | fall |
| true +1 | held · grade=direction+magnitude | ok |
| lie +20 | magnet missed / naive held | ok |
| -20% not stolen | amt=None · pct=20 · intent=fall | ok |
| Suite | `pytest -q` | 361 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 89/89 · embarrassed 35 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- `from 3/5 to 4/5` / `crashes to 0` still unbound (Slice 47).
- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Oscar gates remain: film · Devpost paste · submit.
