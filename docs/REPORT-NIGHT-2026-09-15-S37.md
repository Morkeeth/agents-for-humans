# Night report · 2026-09-15 · Slice 37

**branch:** `cursor/doubles-halves-honesty-94f8` · tip stamped after push

## SHIPPED

1. **Doubles/halves vs prior** — `pass rate doubles` / `halves` grade prior = latest − Δ. Direction-only invents held on a non-double rise.
2. **pred-demo** — 36/36 · embarrassed 15 · FINDING.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| intent | `prediction_intent("doubles")` | rise |
| double held | prior=2 Δ=+2 latest=4 | prediction-held |
| double miss | prior=3 Δ=+1 latest=4 | prediction-missed; naive held |
| Suite | `python3 -m pytest -q` | 295 passed |
| pred-demo | `magnet pred-demo` | 36/36 · embarrassed 15 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Bakeoff surface 1/2 still open.
- Percent-of-prior (relative to previous value, not pop) still not graded.
- Oscar gates remain.

## Product execution checkpoint

| Dimension | Status | Evidence |
|-----------|--------|----------|
| 1. Promised user value | **observed** | doubles/halves predictions check prior |
| 2. Independent use | **observed** | `magnet pred-demo` |
| 3. Distinctive promise | **observed** | open prior object, not the verb |
| 4. Action and return | **partial** | adopt grades ratio; no hosted sync |
| 5. Access | **partial** | branch → main ship pending |
