# REPORT · Slice 64 · 2026-09-23

## SHIPPED

- Soft-hedge refuse extended: `around` / `circa` / `close to` / `~` / `≈`.
- Same refuse path as Slice 62 — never invent exact held under soft language.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `must stay at around 4/5` @3 | `check_prediction` | no-direction; naive held |
| `around equals 4/5` @4 | same | no-direction (target unbound) |
| `must stay at close to 4/5` @3 | same | no-direction; naive held |
| `must stay at ~4/5` @3 | same | no-direction; naive held |
| S62 regression `must stay at roughly 4/5` | same | no-direction |
| Exact `must stay at 4/5` @4 | same | held |
| Suite | `python3 -m pytest -q` | **521 passed, 1 skipped** (522) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **220/220** · embarrassed **132** |
| Judge | `MAGNET_JUDGE_QUICK=1 bash scripts/judge-demo.sh` | JUDGE DEMO OK |

## WRONG

- Thirty-compounds (`thirty-one to thirty-two`) still unbound — same steal risk.
- Other hedges (`more or less`, `or so`, `-ish`) still unbound.
- Oscar gates still closed.
