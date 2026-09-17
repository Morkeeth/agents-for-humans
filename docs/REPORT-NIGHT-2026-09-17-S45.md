# Night report · 2026-09-17 · Slice 45

**branch:** `cursor/negated-rise-shall-b0b0`

## SHIPPED

1. **Bare `up N` / `down N` magnitude** — amount parses; +1 held / +20 missed.
2. **`up 20%` still percent** — never amount=20.
3. **pred-demo** — 85/85 · embarrassed 32.
4. Doc claims re-derived **348 → 354**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| up 1 amount | `claimed_magnitude("up 1")` | amount=1 |
| true +1 | `check_prediction("up 1","helped",1)` | prediction-held |
| absolute lie | Δ=+20 | magnet missed / naive held |
| up 20% | `claimed_percent` / amount | pct=20 / amount=None |
| Suite | `pytest -q` | 353 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 85/85 · embarrassed 32 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- Signed `+1` / `-1` still no-direction (`\b` before `+` fails at string start).
- `from 3/5 to 4/5` / `crashes to 0` still unbound.
- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Oscar gates remain: film · Devpost paste · submit.
