# Night report · 2026-09-16 · Slice 42

**branch:** `cursor/pct-better-gains-ce9a` · `62897ca72bae262eda5917f37e728aba68b6377a` (re-derive: `git rev-parse origin/main`)

## SHIPPED

1. **`50% better` / `50% worse` / `N percent better`** — parse as percent-of-pop with rise/fall intent.
2. **`gains 20%` / `jumps 20%` / `boosts by 20%`** — rise + percent (were no-direction even when `%` parsed).
3. **pred-demo** — 67/67 · embarrassed 26 · FINDING.
4. Doc claims re-derived 324 → 329.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| 50% better parses | `claimed_percent("50% better")` | 50 · intent=rise |
| true 50% pop5 | Δ=+2 | prediction-held |
| absolute lie | Δ=+20 | prediction-missed (naive held) |
| 50% worse | intent=fall · Δ=-2 | prediction-held |
| gains 20% | rise + pct=20 | held on Δ=+1; missed on Δ=+20 |
| Suite | `python3 -m pytest -q` | 328 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 67/67 · embarrassed 26 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Bakeoff surface 1/2 still open.
- `perfect score` without a number still unbound.
- Oscar gates remain: film · Devpost paste · submit.

## Night stack (also on main)

- Slice 40 · word-percent + never/cannot · `3df2052` / tip `692cb5b`
- Slice 41 · zero/perfect + quadrupples · `087a110` / tip `a68a770`
- Slice 42 · this commit (tip after stamp)
