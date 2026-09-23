# REPORT · Slice 62 · 2026-09-23

## SHIPPED

- Soft-hedge refuse: `roughly` / `approximately` / `about` / `nearly` / `almost`
  that modify a numeric/ratio claim → `no-direction` (never invent exact held).
- Wired through `claimed_level` / `claimed_target` / `claimed_floor` /
  `claimed_ceiling` / `claimed_percent` / `claimed_magnitude` / `claimed_ratio`
  + early refuse in `check_prediction`.
- Non-hedge `about` preserved: `about to rise`, `talk about skills`,
  `bring about a rise`.
- `magnet pred-demo` +10 soft-hedge scenarios; embarrassment counts
  no-direction refuse vs naive held.
- `tests/test_soft_hedge_refuse.py` (14 tests).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `must stay at roughly 4/5` @3 | `check_prediction` | no-direction; naive held |
| `almost exactly 4/5` @4 | same | no-direction; naive held |
| `roughly equals 4/5` @4 | same | no-direction (target unbound) |
| `same as about 4/5` @3 | same | no-direction; naive held |
| `roughly stay at 4/5` @4 | same | no-direction; naive held |
| `roughly at least 4/5` | same | no-direction (floor unbound) |
| `won't fall below about 3/5` @2 | same | no-direction; naive held |
| `improves by roughly 20%` | same | no-direction; naive held |
| `roughly doubles` / `almost doubles` | same | no-direction |
| Exact contrast `must stay at 4/5` @4/@3 | same | held / missed |
| Non-hedge `about to rise by 1` | `is_soft_hedged` + check | False; grades rise |
| Suite | `python3 -m pytest -q` | **506 passed, 1 skipped** (507) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **211/211** · embarrassed **125** |
| Demo | `magnet demo` | exit 0 · helped |
| Judge | `MAGNET_JUDGE_QUICK=1 bash scripts/judge-demo.sh` | JUDGE DEMO OK |

## WRONG

- Soft hedges on word levels (`roughly four`, `about four out of five`) not
  exhaustively exercised beyond digit forms — word-level claimable is in the
  detector but not separately embarrassment-rowed.
- Other hedges (`around`, `circa`, `close to`, `something like`) still unbound.
- Word ordinals beyond twentieth still unbound.
- Bedrock cloud still BLOCKED (no AWS creds in this VM).
- Oscar gates still closed (film · Devpost · submit) — no outward acts.
