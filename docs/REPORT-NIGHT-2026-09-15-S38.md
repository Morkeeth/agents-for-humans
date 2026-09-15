# Night report · 2026-09-15 · Slice 38

**branch:** `cursor/below-bound-floor-94f8` · tip stamped after push

## SHIPPED

1. **Below-bound floors** — `won't fall below 3/5` / `never below` / `no lower than` / `must not drop under` open the floor object.
2. **Exclusive above** — `stays above 3/5` held only when latest > bound.
3. **THE LIE fixed** — unchanged @ latest=2 beneath a named below-bound no longer invents held.
4. **pred-demo** — 41/41 · embarrassed 17 · FINDING.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| floor parses | `claimed_floor("won't fall below 3/5")` | value=3/5 |
| the lie | unchanged @ latest=2 | prediction-missed (naive held) |
| at/above bound | latest 3 or 4 | prediction-held |
| stays above exclusive | latest 3 → miss; 4 → hold | ok |
| no lower than | intent flat (was fall) | ok |
| Suite | `python3 -m pytest -q` | 303 passed |
| pred-demo | `magnet pred-demo` | 41/41 · embarrassed 17 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Bakeoff surface 1/2 still open.
- Percent without `by` (`rises 20%`) still unparsed.
- Triples / Nx still unknown.
- Oscar gates remain.

## Product execution checkpoint

| Dimension | Status | Evidence |
|-----------|--------|----------|
| 1. Promised user value | **observed** | below-bound predictions open the floor |
| 2. Independent use | **observed** | `magnet pred-demo` |
| 3. Distinctive promise | **observed** | open the bound, not the verb |
| 4. Action and return | **partial** | adopt grades floor; no hosted sync |
| 5. Access | **partial** | branch → main ship pending |
