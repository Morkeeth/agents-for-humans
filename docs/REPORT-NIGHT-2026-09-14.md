# Night report · 2026-09-14 · Slices 32–34

**main tip:** `PENDING` · **branch:** `cursor/rise-lexicon-recover-17b8`

## SHIPPED

1. **Recover/restore rise lexicon** — `pass rate recovers by 1` is rise+magnitude (was `no-direction` while Δ +1). Devpost one-workflow grades its own restore prediction.
2. **`scripts/one-workflow.sh`** — cold path; exit 0 only when recover grades as rise. Live: `254/254 → 253/254 hurt → 254/254 helped` · prediction-held.
3. **Honest pytest paste** — check_docs accepts `N passed, M skipped` (+ failed) as suite size.
4. **Grinder receipt `--verify`** — re-probes; exit 1 on drift. `magnet receipt-demo` GREEN then planted RED.
5. **Grinder evidence `--grinder`** — `magnet.grinder-evidence/v1` with verify + prediction; never invents COUNT_FIELDS; verify RED refuses export. check_docs RED without receipt-demo FINDING.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| Suite | `python3 -m pytest -q` | 266 passed, 1 skipped |
| recover intent | object call | `rise` |
| one-workflow | `bash scripts/one-workflow.sh` | ONE WORKFLOW OK |
| pred-demo | `magnet pred-demo` | 18/18 · embarrassed 8 |
| receipt-demo | `magnet receipt-demo` | GREEN 4/5 · RED planted · FINDING |
| receipt --grinder | `magnet receipt --grinder` | exportable True · no COUNT_FIELDS |
| check_docs | `magnet check-docs` | 15 PASS |
| cold clone s33 | `/tmp/magnet-cold-s33` @ 37d3014 | 261 passed · OW OK · receipt-demo FINDING |
| push main | `git push origin …:main` | tip `PENDING` |

## WRONG

- PR auto-create blocked by user settings — Oscar must open/approve the PR UI click.
- Bedrock still BLOCKED on cloud VM.
- Bakeoff surface 1/2 (helicon dupe) still open.
- Grinder evidence is a sidecar, not a full grind run — by design (inventing turns_typed would be the lie).
- Oscar gates remain: film · Devpost paste · submit Sep 14.
- Early instinct was to trust Slice 31's `rises by 1` papering; the defect only showed when opening the DEMO prediction text itself.

## Product execution checkpoint

| Dimension | Status | Evidence |
|-----------|--------|----------|
| 1. Promised user value | **observed** | helped + prediction-held on recovers; verify refuses stale receipt |
| 2. Independent use | **observed** | one-workflow.sh · receipt-demo · receipt --grinder |
| 3. Distinctive promise | **observed** | magnet-to-YOUR-stack + Grinder evidence without invented counts |
| 4. Action and return | **partial** | history / receipt --verify / --grinder work; no hosted sync |
| 5. Access | **observed** | pushed to `main` @ prior tip; re-derive after this commit |
