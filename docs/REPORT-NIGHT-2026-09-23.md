# REPORT · night 2026-09-23 · Slices 62–64

## SHIPPED

What exists now that did not at the start of this run:

1. **Slice 62 — soft-hedge refuse** (`roughly`/`approximately`/`about`/`nearly`/`almost`)
   — never invent exact held under soft language.
2. **Slice 63 — twenty-compound word levels** (`twenty-one`…`twenty-nine` + ordinals)
   — never steal `one→twenty` and invent dest=20 held @20.
3. **Slice 64 — around/close-to/~ refuse** — extends the soft-hedge pack.
4. Reports: `docs/REPORT-NIGHT-2026-09-23-S62.md` … `S64.md`
5. Tests: `test_soft_hedge_refuse.py`, `test_twenty_compound.py`, `test_around_close_tilde.py`
6. `hack.md` NOW + LOG updated; pred-demo 220/220 · embarrassed 132.

Branch: `cursor/soft-hedge-refuse-157c` (not pushed to main — Oscar click for merge).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| Soft stay refuse | `check_prediction('must stay at roughly 4/5', … @3)` | no-direction; naive held |
| Soft exact refuse | `check_prediction('almost exactly 4/5', … @4)` | no-direction; naive held |
| Twenty-compound | `claimed_target('twenty-one to twenty-two')` | value=22; miss @20; hold @22 |
| Around stay | `check_prediction('must stay at around 4/5', … @3)` | no-direction; naive held |
| Tilde stay | `check_prediction('must stay at ~4/5', … @3)` | no-direction; naive held |
| Suite | `python3 -m pytest -q` | **521 passed, 1 skipped** (522) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **220/220** · embarrassed **132** · FINDING |
| Demo | `magnet demo` | exit 0 |
| Judge | `MAGNET_JUDGE_QUICK=1 bash scripts/judge-demo.sh` | JUDGE DEMO OK |

## WRONG

- Did **not** `git push origin main` — outward push to main is Oscar's click; shipped on feature branch `cursor/soft-hedge-refuse-157c` instead (cloud agent contract).
- Thirty-compounds (`thirty-one to thirty-two`) still unbound — same steal pattern likely.
- Hedges `more or less` / `or so` / `-ish` still unbound.
- Bedrock cloud still BLOCKED (no AWS creds).
- PR create registered for user approval (not auto-opened).
- Early in the run, a parallel edit/test race briefly showed soft-hedge checks failing before the `check_prediction` early-exit landed — caught by re-running at the object.
