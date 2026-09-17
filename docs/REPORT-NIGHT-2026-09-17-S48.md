# Night report · 2026-09-17 · Slice 48

**branch:** `cursor/arrow-perfect-score-aead`

## SHIPPED

1. **Arrow glyphs `↑1` / `↓1`** — rise/fall intent + absolute magnitude (and `↑1/5` / `↓1/5`).
2. **Unbound `perfect score` / `perfect` / `full score`** — resolves to `latest == population` at check time; refuses without pop.
3. **Embarrassment arms** — `↑1` @ Δ=+20 magnet missed / naive held; `perfect score` @ latest=4 magnet missed / naive held.
4. **pred-demo** — 101/101 · embarrassed 40.
5. Doc claims re-derived **373 → 386**.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `↑1` intent+amount | `prediction_intent` / `claimed_magnitude` | rise / 1 |
| `↓1/5` frac | `claimed_magnitude("↓1/5")` | amount=1 pop=5 |
| arrow lie | `check_prediction("↑1", helped, 20)` | magnet missed / naive held |
| perfect score flag | `claimed_target("perfect score")` | perfect=True |
| perfect@4 | `check_prediction(..., unchanged, latest=4, pop=5)` | magnet missed / naive held |
| Suite | `python3 -m pytest -q` | 385 passed, 1 skipped |
| pred-demo | `magnet pred-demo` | 101/101 · embarrassed 40 |
| check_docs | `magnet check-docs` | 16 PASS |
| demo | `magnet demo` | exit 0 |

## WRONG

- `climbs 1` / `slips 1` still amount=None (direction invents held on +20).
- `grows by 1` / `shrinks by 1` amount set but intent=unknown → no-direction.
- `5 out of 5` / `score of 5/5` / `full marks` / `100%` still unbound.
- Fat arrows `⬆1` / `▲1` still unbound.
- Bedrock BLOCKED on cloud VM.
- Oscar gates remain: film · Devpost paste · submit.
- SHIP GATE asked for `git push origin main`; this environment ships via feature branch + PR.
