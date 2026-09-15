# Night report · 2026-09-15 · Slice 39

**branch:** `cursor/percent-syntax-triples-94f8` · tip stamped after push

## SHIPPED

1. **Percent without `by`** — `rises 20%` / `improves 20%` / `20% improvement` / `up 50%` / `+20%`.
2. **Triples / Nx** — `triples` / `3x` / `2x` / `tenfold` grade prior = latest − Δ.
3. **pred-demo** — 46/46 · embarrassed 19 · FINDING.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| rises 20% parses | `claimed_percent("rises 20%")` | 20 |
| true 20% | Δ=+1 pop=5 | prediction-held |
| absolute lie | Δ=+20 pop=5 | prediction-missed (naive held) |
| triples | prior=2 Δ=+4 latest=6 | prediction-held |
| Suite | `python3 -m pytest -q` | 309 passed |
| pred-demo | `magnet pred-demo` | 46/46 · embarrassed 19 |
| check_docs | `magnet check-docs` | 16 PASS |

## WRONG

- PR auto-create blocked — Oscar UI click.
- Bedrock BLOCKED on cloud VM.
- Bakeoff surface 1/2 still open.
- `goes to zero` / `perfect N/N` still weak.
- Oscar gates remain.

## Product execution checkpoint

| Dimension | Status | Evidence |
|-----------|--------|----------|
| 1. Promised user value | **observed** | more prediction phrasings grade at the object |
| 2. Independent use | **observed** | `magnet pred-demo` |
| 3. Distinctive promise | **observed** | open % and prior, not the verb |
| 4. Action and return | **partial** | adopt grades; no hosted sync |
| 5. Access | **partial** | branch → main ship pending |
