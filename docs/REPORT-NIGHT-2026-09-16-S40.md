# Night report · 2026-09-16 · Slice 40

**branch:** `cursor/percent-word-negation-ce9a` · `3df2052c23c952b6f8e97dd6aa14d9ba9041670c` (re-derive: `git rev-parse origin/cursor/percent-word-negation-ce9a`)

## SHIPPED

1. **Word-percent** — `improves by 20 percent` / `per cent` / `pct` / `rises 20 percent` / `20 percent improvement` / `+20 percent` parse as percent-of-pop, never absolute 20.
2. **never/cannot/won't-decrease negation** — `never falls` / `cannot fall` / `won't decrease` / `no decrease` / `without decreasing` → flat (not fall). Hurt no longer invents held.
3. **pred-demo** — 52/52 · embarrassed 20 · FINDING names word-percent + never-falls.
4. Doc claims re-derived 309 → 317 (`def test_` count).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| word percent parses | `claimed_percent("improves by 20 percent")` | 20 |
| not absolute | `claimed_magnitude("improves by 20 percent")` | amount=None |
| true 20% | Δ=+1 pop=5 | prediction-held |
| absolute lie | Δ=+20 pop=5 | prediction-missed (naive held) |
| `%` still works | `claimed_percent("improves by 20%")` | 20 |
| never falls flat | `prediction_intent("never falls")` | flat |
| never falls + hurt | `check_prediction(..., "hurt")` | prediction-missed |
| won't decrease + hurt | same | prediction-missed |
| Suite | `python3 -m pytest -q` | 316 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 52/52 · embarrassed 20 |
| check_docs | `magnet check-docs` | 16 PASS |
| demo | `magnet demo` | exit 0 · helped receipt |

## WRONG

- PR / main merge is Oscar's click if auto-create is blocked.
- Bedrock BLOCKED on cloud VM (no credentials).
- Bakeoff surface 1/2 still open.
- `quadruples` / `N times` / `goes to zero` / `perfect N/N` still unbound (no-direction — safer than inventing held, but unfinished).
- Negation rows no longer embarrass the naive arm (naive shares the fixed intent parser by design since Slice 35) — embarrassment is the word-percent absolute lie.
- Oscar gates remain: film · Devpost paste · submit.
