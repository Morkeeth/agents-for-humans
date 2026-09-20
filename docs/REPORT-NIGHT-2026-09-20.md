# REPORT · Night 2026-09-20 · MAGNET S55–S59

## SHIPPED

1. **S55** bare `three to four` / `3 to 4` · bare `twenty percent` / `20%` rise.
2. **S56** `-twenty percent` fall · word arrows `three → four`.
3. **S57** `exactly four` / `falls to four` / `exactly twenty` word targets.
4. **S58** teen `fifteen percent` · `must be four` / `must be 4`.
5. **S59** compound `twenty-five percent` / `seventy five percent`.
6. Suite **477** tests · pred-demo **182/182** · embarrassed **92**.

Branch: `cursor/bare-to-percent-a57b` · tip stamped after push.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| Suite | `python3 -m pytest -q` | **476 passed, 1 skipped** |
| Docs | `magnet check-docs` | **15 PASS** (435→477) |
| Pred-demo | `magnet pred-demo` | **182/182** · embarrassed **92** · FINDING |
| Judge | `bash scripts/judge-demo.sh` | JUDGE DEMO OK |
| Objects | `check_prediction(...)` on each claim | held/missed vs naive as shipped |

## WRONG

- First bare-`%` draft stole `100%` into percent — caught at `@latest=4`.
- Proxies lied: assumed `from three to four` closed destinations; bare/arrow/exactly/must-be/compounds still unbound.
- Could not `git push origin main` — cloud agent ships feature branch + PR; PR create pending Oscar approval.
- Bedrock still blocked; film / Devpost / submit are Oscar gates.
