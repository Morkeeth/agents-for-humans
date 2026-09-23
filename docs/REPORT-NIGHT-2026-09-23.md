# REPORT · night 2026-09-23 · Slices 62–65

## SHIPPED

What exists now that did not at the start of this run:

1. **Slice 62 — soft-hedge refuse** (`roughly`/`approximately`/`about`/`nearly`/`almost`)
2. **Slice 63 — twenty-compound word levels** (`twenty-one`…`twenty-nine` + ordinals)
3. **Slice 64 — around/close-to/~ refuse**
4. **Slice 65 — decade compounds + hundred** (`thirty`…`ninety-nine`, `one hundred`)
5. Reports S62–S65 + this night rollup
6. Tests: `test_soft_hedge_refuse.py`, `test_twenty_compound.py`,
   `test_around_close_tilde.py`, `test_decade_compounds.py`
7. `hack.md` NOW + LOG; pred-demo **225/225** · embarrassed **136**

Branch tip: `19bfc7f3254d51bf2c04b6fcf7ba8a870caa5aef` on `cursor/soft-hedge-refuse-157c`
(Oscar click to merge main — no `git push origin main` from this agent).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| Soft stay refuse | `check_prediction('must stay at roughly 4/5', … @3)` | no-direction; naive held |
| Twenty-compound | `claimed_target('twenty-one to twenty-two')` | value=22; miss @20 |
| Around/tilde | `check_prediction('must stay at around 4/5' / '~4/5', … @3)` | no-direction; naive held |
| Ninety-nine→hundred | `claimed_target('ninety-nine to one hundred')` | value=100; miss @1 |
| Suite | `python3 -m pytest -q` | **529 passed, 1 skipped** (530) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **225/225** · embarrassed **136** · FINDING |
| Cold clone (S64 tip) | `git clone … && pip install -e ".[dev]" && magnet demo` | exit 0 |
| Judge | `MAGNET_JUDGE_QUICK=1 bash scripts/judge-demo.sh` | JUDGE DEMO OK |

## WRONG

- Did **not** `git push origin main` — outward push to main is Oscar's click; shipped on feature branch.
- Hedges `more or less` / `or so` / `-ish` still unbound.
- Word forms above hundred (`one hundred and one`) still unbound.
- Bedrock cloud still BLOCKED.
- PR create registered for user approval (not auto-opened).
- Early parallel edit/test races briefly showed false reds before reloads — caught by re-running at the object.
