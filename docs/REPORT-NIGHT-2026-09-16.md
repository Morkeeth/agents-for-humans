# Night report · 2026-09-16 · MAGNET honesty stack

**main tip:** `49094a7fc04207ab5b9555f991ce295fc73c88c5` (re-derive: `git rev-parse origin/main`)

## SHIPPED

Three honesty slices on main, each found by running prediction objects (not reading titles):

1. **Slice 40** — word `percent`/`pct` ≠ absolute points; `never falls`/`won't decrease` → flat  
   Commit: `3df2052` · report: `docs/REPORT-NIGHT-2026-09-16-S40.md`
2. **Slice 41** — `falls to zero` grades latest; `perfect N/N`; `quadruples`/`N times`  
   Commit: `087a110` · report: `docs/REPORT-NIGHT-2026-09-16-S41.md`
3. **Slice 42** — `50% better`/`worse`; `gains`/`jumps`/`boosts` rise+percent  
   Commit: `62897ca` · report: `docs/REPORT-NIGHT-2026-09-16-S42.md`

**pred-demo:** 67/67 · embarrassed 26 · FINDING  
**Suite:** 328 passed, 1 skipped · check-docs 16 PASS

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| word percent | `claimed_percent("improves by 20 percent")` | 20 (not amount=20) |
| never falls | `prediction_intent("never falls")` | flat; hurt→missed |
| falls to zero | hurt@latest=1 | magnet missed / naive held |
| quadrupples | `claimed_ratio("quadruples")` | factor=4 |
| 50% better | Δ=+2 held; Δ=+20 missed | naive held on lie |
| Suite | `python3 -m pytest -q` | 328 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 67/67 · embarrassed 26 |
| check_docs | `magnet check-docs` | 16 PASS |
| Ship gate | `git push origin main` | tip on origin/main |

## WRONG

- PR auto-create blocked for all three branches — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Bakeoff surface 1/2 still open.
- `perfect score` (no number) still unbound.
- Oscar gates remain: film · Devpost paste · submit.
- Negation rows no longer embarrass naive (shares fixed intent parser since Slice 35 by design).
