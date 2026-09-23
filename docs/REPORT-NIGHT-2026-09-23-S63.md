# REPORT · Slice 63 · 2026-09-23

## SHIPPED

- Twenty-compound word levels `twenty-one`…`twenty-nine` (+ ordinals
  `twenty-first`…`twenty-ninth`), hyphen or space.
- Compounds match before bare `twenty` / `one` / `first` so
  `twenty-one to twenty-two` grades dest=22 — never steals `one to twenty`.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `twenty-one to twenty-two` @20/@22 | `check_prediction` | missed / held; naive held @20 |
| `twenty-first to twenty-second` @20 | same | missed |
| `from twenty to twenty-one` @20/@21 | same | missed / held |
| `twenty-eight to twenty-nine` @28/@29 | same | missed / held |
| Digit contrast `21st to 22nd` | `claimed_target` | dest=22 |
| Teens regression `fifteenth to sixteenth` | same | dest=16 |
| Suite | `python3 -m pytest -q` | **513 passed, 1 skipped** (514) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **216/216** · embarrassed **129** |
| Judge | `MAGNET_JUDGE_QUICK=1 bash scripts/judge-demo.sh` | JUDGE DEMO OK |

## WRONG

- `around` / `close to` / `~` soft hedges still invent held (named for Slice 64).
- Thirty-compounds (`thirty-one`) still unbound — same steal pattern likely.
- Oscar gates still closed.
