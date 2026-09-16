# Night report · 2026-09-16 · Slice 41

**branch:** `cursor/zero-perfect-quad-ce9a` · `087a110a42883c94e655cb9f038f58fc588fa2e2` (re-derive: `git rev-parse origin/main`)

## SHIPPED

1. **Zero target word** — `falls to zero` / `goes to zero` / `goes to 0` → target 0. Hurt@latest=1 is prediction-missed (was direction-held).
2. **Perfect/full/max targets** — `perfect 5/5` / `full 5/5` / `max 5/5` grade latest.
3. **Quadrupples / N times / Nfold** — `quadruples` / `five times` / `fivefold` grade prior like `4x`.
4. **pred-demo** — 61/61 · embarrassed 23 · FINDING names zero + quadrupples.
5. Doc claims re-derived 317 → 324.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| zero target | `claimed_target("falls to zero")` | value=0 |
| off-zero lie fixed | hurt@latest=1 | prediction-missed (naive held) |
| on-zero | hurt@latest=0 | prediction-held |
| perfect | `claimed_target("perfect 5/5")` | 5/5 |
| quadrupples | `claimed_ratio("quadruples")` | factor=4 |
| five times | `claimed_ratio("five times")` | factor=5 |
| Suite | `python3 -m pytest -q` | 323 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 61/61 · embarrassed 23 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- PR auto-create still Oscar UI click (Slice 40 also).
- Bedrock BLOCKED on cloud VM.
- Bakeoff surface 1/2 still open.
- `50% better` / `gains 20%` / `jumps 20%` still unbound (no-direction).
- `perfect score` without a number still unbound.
- Oscar gates remain: film · Devpost paste · submit.
