# Night report · 2026-09-15 · Slice 36

**branch:** `cursor/percent-exactly-honesty-94f8` · tip stamped after push

## SHIPPED

1. **Percent-of-pop** — `improves by 20%` no longer strips `%` into absolute 20. Expected Δ = round(pop · pct / 100).
2. **Exactly-level** — `exactly 4/5` / `must be exactly 4/5` grades latest (was no-direction).
3. **pred-demo** — 32/32 · embarrassed 13 · FINDING names percent honesty.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| not absolute | `claimed_magnitude("improves by 20%")` | amount=None; claimed_percent=20 |
| true 20% | Δ=+1 pop=5 | prediction-held |
| absolute lie | Δ=+20 pop=5 | prediction-missed; naive held |
| exactly | latest 3 vs 4/5 | prediction-missed |
| Suite | `python3 -m pytest -q` | 288 passed |
| pred-demo | `magnet pred-demo` | 32/32 · embarrassed 13 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- PR auto-create blocked — Oscar UI click.
- Bedrock still BLOCKED on cloud VM.
- Bakeoff surface 1/2 still open (helicon FINDING).
- Percent-of-*prior* (relative to previous reading, not population) not graded — pop·pct is the object we opened tonight.
- Doubles/halves still unknown.
- Oscar gates remain.

## Product execution checkpoint

| Dimension | Status | Evidence |
|-----------|--------|----------|
| 1. Promised user value | **observed** | percent/exactly predictions grade at the object |
| 2. Independent use | **observed** | `magnet pred-demo` |
| 3. Distinctive promise | **observed** | refuse absolute invent on `%` |
| 4. Action and return | **partial** | adopt prints percent grade; no hosted sync |
| 5. Access | **partial** | branch push; main ship pending |
