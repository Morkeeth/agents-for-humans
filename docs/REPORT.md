# Build report · Slice 28–29 · 2026-09-12

## SHIPPED

### Slice 28 — Absolute-level honesty
- `must stay at 5` (no `/pop`) grades latest value.
- `remain at` / `hold at` / `keep at` / `unchanged at` are flat + level.
- Floor: `at least 4/5` / `no worse than 4/5`.
- `magnet pred-demo` → **15/15** · **7** embarrassment rows.

### Slice 29 — Adopt default real week
- Bare `magnet adopt` no longer prints `SIMULATED week`.
- `--simulate` is the demo opt-in; `--no-simulate` kept as deprecated no-op for old docs.
- `magnet demo` / `agent-run` still label simulated weeks explicitly.
- **232** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 232 passed |
| stay-at no slash | `check_prediction("must stay at 5", …, latest_value=4)` → prediction-missed |
| pred-demo | `magnet pred-demo` → magnet 15/15 · embarrassed 7 · FINDING |
| bare adopt | `magnet adopt skill x '…' --probe demo-pass-rate --demo-bonus --reset` → no SIMULATED · helped · real `read_at` |
| `--simulate` | same + `--simulate` → SIMULATED labelled |
| demo still simulated | `magnet demo` → SIMULATED week note |
| check_docs | `magnet check-docs` → 13 PASS |
| Cold clone s28 | `/tmp/magnet-cold-s28` @ `ecc179f` → 227 passed · JUDGE DEMO OK |
| SHIP GATE s28 | `git push origin main` → `bc7a58b` |
| Cold clone s29 | `/tmp/magnet-cold-s29` @ `4504e44` → 232 passed · bare adopt no SIMULATED · JUDGE DEMO OK |
| SHIP GATE s29 | `git push origin main` → pending |

## WRONG

- **Surface arm still 1/2** — helicon science.
- **Bedrock cloud BLOCKED.**
- **Vacuous `0/0` probes exit 0** — empty stack invents a green control; Slice 30.
- **history/one-workflow sidecars still stale**; check_docs blind to them.
- **Pillow not in base install.**
- Flipping adopt default changes stranger receipts that previously showed SIMULATED without `--no-simulate` — intentional honesty.
