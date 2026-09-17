# Night report · 2026-09-17 · Slice 47

**branch:** `cursor/negated-rise-shall-b0b0`

## SHIPPED

1. **Crash/collapse/dive/plunge → targets**; soar/spike/balloon → targets.
2. **`from A to B` / `A → B`** — destination is the target.
3. **Embarrassment** — crashes@latest=1 magnet missed / naive held.
4. **pred-demo** — 95/95 · embarrassed 37.
5. Doc claims re-derived **362 → 373**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| crashes to zero | `claimed_target` | 0 |
| soars to 5/5 | value=5 pop=5 | ok |
| from 3/5 to 4/5 | target 4/5 | ok |
| lie off-zero | magnet missed / naive held | ok |
| Suite | `pytest -q` | 372 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 95/95 · embarrassed 37 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- `↑1` / `↓1` still unbound.
- `perfect score` (no number) still unbound.
- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Oscar gates remain: film · Devpost paste · submit.
