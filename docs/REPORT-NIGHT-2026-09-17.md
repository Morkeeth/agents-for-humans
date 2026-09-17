# Night report · 2026-09-17 · MAGNET honesty stack (Slices 43–47)

**branch:** `cursor/negated-rise-shall-b0b0`  
**main tip:** `574de6caf77a8bd285b2aa7651d5aa9a26d33c63` (re-derive: `git rev-parse origin/main`)

## SHIPPED

Five honesty slices found by running prediction objects (not titles):

1. **Slice 43** — negated rise (`doesn't rise` / `never rises` / `won't improve`) + shall/ought/may not fall + bare `no worse`/`no better` → flat
2. **Slice 44** — `20% higher`/`lower`/`more`/`less`/`up`/`down` percent-of-pop (embarrassment vs naive)
3. **Slice 45** — bare `up N` / `down N` magnitude
4. **Slice 46** — signed `+1`/`-1` intent; `(?!\\d)` blocks `-20%` steal
5. **Slice 47** — `crashes to zero` / `soars to N` / `from A to B` / `A → B` targets

**pred-demo:** 95/95 · embarrassed 37 · FINDING  
**Suite:** 372 passed, 1 skipped · check-docs 16 PASS  
**Doc claims:** 329 → 373 (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| doesn't rise | `prediction_intent` | flat; helped→missed |
| 20% higher | `claimed_percent` · +1 held / +20 missed | naive held on lie |
| up 1 | `claimed_magnitude` amount=1 · +20 missed | ok |
| +1 intent | rise + magnitude · -20% not stolen | ok |
| crashes to zero | target=0 · latest=1 missed / naive held | ok |
| from 3/5 to 4/5 | target=4/5 | ok |
| Suite | `pytest -q` | 372 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 95/95 · embarrassed 37 |
| check_docs | `magnet check-docs` | 16 PASS |
| demo | `magnet demo` | exit 0 · helped receipt |

## WRONG

- PR auto-create blocked — Oscar UI click (branch pushed: `cursor/negated-rise-shall-b0b0`).
- Bedrock BLOCKED on cloud VM (no AWS credentials).
- Bakeoff surface 1/2 still open (helicon cross-surface dupe).
- `perfect score` (no number) still unbound.
- `↑1` / `↓1` arrows still unbound.
- Oscar gates remain: film · Devpost paste · submit.
- Negation rows still do not embarrass naive (shared intent parser by design since Slice 35).
