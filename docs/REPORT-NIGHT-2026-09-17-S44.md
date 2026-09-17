# Night report · 2026-09-17 · Slice 44

**branch:** `cursor/negated-rise-shall-b0b0`

## SHIPPED

1. **`20% higher` / `lower` / `more` / `less` / `up` / `down`** — trailing comparator percents parse as percent-of-pop.
2. **Word forms** — `20 percent higher`, `20 pct less`.
3. **`20% more` / `less` intent** — bound from trailing comparator (not in rise/fall lexicon).
4. **Embarrassment arm** — magnet misses on Δ=+20; naive direction invents held.
5. **pred-demo** — 82/82 · embarrassed 30.
6. Doc claims re-derived **340 → 348**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| 20% higher pct | `claimed_percent("20% higher")` | 20 |
| true 20% pop5 | Δ=+1 | prediction-held |
| absolute lie | Δ=+20 | magnet missed / naive held |
| 20% more intent | `prediction_intent("20% more")` | rise |
| Suite | `pytest -q` | 347 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 82/82 · embarrassed 30 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- `up 1` / `down 1` still direction-only (Slice 45).
- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Oscar gates remain: film · Devpost paste · submit.
