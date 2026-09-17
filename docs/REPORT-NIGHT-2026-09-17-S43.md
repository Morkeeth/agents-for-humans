# Night report · 2026-09-17 · Slice 43

**branch:** `cursor/negated-rise-shall-b0b0`

## SHIPPED

1. **Negated rise → flat** — `doesn't rise` / `never rises` / `won't improve` / `cannot improve` / `won't increase` no longer invent held on helped.
2. **shall / ought / may not fall → flat** — modal gap Slice 40 left open; hurt no longer invents held.
3. **Bare `no worse` / `no better` / `won't get worse` / `non-regression` → flat.**
4. **pred-demo** — 76/76 · FINDING names Slice 43.
5. Doc claims re-derived **329 → 340**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| doesn't rise | `prediction_intent("doesn't rise")` | flat |
| never rises helped | `check_prediction("never rises","helped",1)` | prediction-missed |
| shall not fall hurt | `check_prediction("shall not fall","hurt",-1)` | prediction-missed |
| no worse hurt | `check_prediction("no worse","hurt",-1)` | prediction-missed |
| no worse than floor | `claimed_floor("no worse than 4/5")` | value=4; grade=floor |
| Suite | `pytest -q` | 339 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 76/76 · embarrassed 26 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- Negation rows still do not embarrass naive (shared intent parser since Slice 35 by design).
- `20% higher` / `up 1` still direction-only — next slices.
- Bedrock BLOCKED on cloud VM.
- Oscar gates remain: film · Devpost paste · submit.
