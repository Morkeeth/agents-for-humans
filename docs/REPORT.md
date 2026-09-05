# Build report · Slice 15–16 · 2026-09-05

## SHIPPED

### Slice 16 — ruling honesty + unmeasured probe exit
- README contradicted EYES: named Agent Grinder as "the Agents for Humans entry"
  and MAGNET as "not itself the submission". Fixed to: MAGNET submits Sep 14;
  Grinder is companion.
- `check_docs` claim `sep14 entry ruling` — control goes RED on the old lie
  (verified in `tests/test_ruling_and_probe_exit.py`).
- `magnet probe` exits **1** when value is None (DEVPOST-DESCRIPTION defect:
  dead pytest printed `None` and exited 0).

### Slice 15 — apply-to-stack
- Defect: adopt --fit on secrets-scanner → fills-gap while coverage stayed 8/12.
- `magnet adopt --apply` · `apply-demo` · `apply-eval` (naive_fit 2/3, magnet 3/3).
- 131 pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 131 passed |
| check_docs | `magnet check-docs` → 12 claims PASS |
| Ruling control RED | plant old README lie → `sep14 entry ruling` ok=False |
| Dead probe exit 1 | `magnet probe dead-eval` (registry `false`) → exit 1 |
| Apply-demo | `magnet apply-demo` → 8/12→9/12 helped; wine unchanged |
| Apply-eval | `magnet apply-eval` → magnet 3/3 |
| Fixture untouched | `magnet probe stack-coverage` → 8/12 |

## WRONG

- **README lied about who submits** for days after EYES — found by opening
  `_NIGHT-SCOPE.md` against README, not by reading one file.
- **Synonym bakeoff primary still 0/3** — EXP-MAGNET-01 unchanged.
- **Bedrock cloud still BLOCKED**.
- **`--apply` is skill-only**.
- **Adopt default still simulates week** without `--apply`.
- **Screenshot sidecars still say 113 / 11 claims** — not in check_docs scan.
- **SHIP GATE `git push origin main`** — cloud agent pushes feature branch + PR;
  merge is Oscar's click.
- **fleet-ops plan still 404**.
- **Agent Grinder VIDEO-SHOTLIST says never show MAGNET** while MAGNET submits —
  contradiction lives in the other repo; not touched (EYES: do not touch grinder).
