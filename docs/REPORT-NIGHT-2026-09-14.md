# Night report · 2026-09-14 · Slices 32–33

**branch tip:** `cursor/rise-lexicon-recover-17b8` · re-derive hash after push

## SHIPPED

1. **Recover/restore rise lexicon** — `pass rate recovers by 1` is rise+magnitude (was `no-direction` while Δ +1). Devpost one-workflow grades its own restore prediction.
2. **`scripts/one-workflow.sh`** — cold path runs the 6-step prompt change loop; exit 0 only when recover grades as rise. Live: `254/254 → 253/254 hurt → 254/254 helped` · prediction-held.
3. **Honest pytest paste** — check_docs accepts `N passed, M skipped` (+ failed) as suite size so sidecars need not invent `N+M passed`.
4. **Grinder receipt `--verify`** — re-probes at the object; exit 1 on drift. `magnet receipt-demo` GREEN then planted RED. `--json` alias restored for stranger docs.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| Suite | `python3 -m pytest -q` | 261 passed, 1 skipped |
| recover intent | `python3 -c "…prediction_intent('pass rate recovers by 1')"` | `rise` |
| one-workflow | `bash scripts/one-workflow.sh` | ONE WORKFLOW OK · recovers prediction-held |
| pred-demo | `magnet pred-demo` | 18/18 · embarrassed 8 · FINDING |
| receipt-demo | `magnet receipt-demo` | GREEN 4/5 · RED 103/5 vs 4/5 · FINDING |
| receipt verify | `magnet receipt --verify` | exit 0 on live; exit 1 on plant |
| check_docs | `magnet check-docs` | 15 PASS |
| push branch | `git push -u origin cursor/rise-lexicon-recover-17b8` | (re-derive after this commit) |

## WRONG

- **PR create** queued for Oscar approval in this cloud environment — not auto-opened. SHIP GATE asked for `git push origin main`; this run ships on feature branch `cursor/rise-lexicon-recover-17b8` pending Oscar merge click.
- **Bedrock** still BLOCKED on cloud VM (no AWS creds) — unchanged.
- **Bakeoff surface 1/2** (helicon cross-surface dupe) still open — not papered over.
- **one-workflow in judge-demo** adds ~20s pytest loops; cold CI may feel it.
- **Oscar gates remain:** film · Devpost paste · submit Sep 14.
- Early Slice 31 sidecar used `rises by 1` and showed Δ +9 under suite noise — tonight's live run restored ±1 and `recovers`; I initially almost trusted the papered synonym before opening the prediction object.

## Product execution checkpoint (observed)

| Dimension | Status | Evidence |
|-----------|--------|----------|
| 1. Promised user value | **observed** | After restore, user gets `helped` + `prediction-held` on `recovers by 1` (`bash scripts/one-workflow.sh`) |
| 2. Independent use | **observed** | `pip install -e ".[dev]"` + `bash scripts/one-workflow.sh` / `magnet receipt-demo` — no builder narration required |
| 3. Distinctive promise | **observed** | Magnet-to-YOUR-stack: re-runs YOUR pytest; refuses no-direction on recover; verify refuses stale SQLite |
| 4. Action and return | **partial** | Next action `magnet history` / `magnet receipt --verify` works; return loop is adopt→probe→grade (no hosted sync) |
| 5. Access | **partial** | Branch pushed; main merge + Devpost submit are Oscar clicks; Bedrock path untested here |
