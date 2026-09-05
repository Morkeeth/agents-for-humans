# Build report · Slice 15 · 2026-09-05

## SHIPPED

### Slice 15 — apply-to-stack (found by running, not reading)
- Defect: `magnet adopt skill secrets-scanner … --fit --probe stack-coverage`
  printed `fills-gap security` while coverage stayed **8/12** (skill never written).
- `magnet/apply.py` — materialize writable copy; write `skills/<slug>/SKILL.md`;
  never mutate `fixtures/stack`.
- `magnet adopt --apply [--apply-dest]` — write → re-probe → receipt;
  defaults to `--no-simulate` for honest same-sitting readings.
- `magnet apply-demo` — naive-fit invents `helped` from the label; magnet waits
  for coverage `8/12 → 9/12`; wine-pairing apply stays `8/12` + `no-signal`.
- `magnet apply-eval` — naive_fit 2/3 · magnet 3/3 · silent_null 0/3.
- Judge-demo step 7b + stranger-pass wired.
- 124 pytest tests (re-derived from `tests/test_*.py`).

### Prior (slices 13–14)
- Stack inventory / bakeoff / adopt --fit / stack-coverage (see git history).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 124 passed |
| check_docs | `magnet check-docs` → 11 claims PASS |
| Defect still true without --apply | `magnet adopt skill secrets-scanner … --probe stack-coverage --fit --no-simulate --reset` → fills-gap + unchanged + note |
| Apply moves coverage | `magnet adopt … --apply --probe stack-coverage` → helped 9/12; fixture still 8/12 |
| Noise apply honest | wine-pairing --apply → unchanged + no-signal |
| Apply-eval magnet wins | `magnet apply-eval` → magnet 3/3; naive_fit loses fit_without_apply |
| Apply-demo cold | `magnet apply-demo` → exit 0 |
| Fixture untouched | `magnet probe stack-coverage` → 8/12 after apply-demo |
| Demo / bakeoff / eval | `magnet demo` · `magnet bakeoff --no-write` · `magnet eval` → exit 0 |

## WRONG

- **Assumed fit+coverage was already closed.** Slice 14 shipped fit receipts; running
  adopt --fit on a real gap showed coverage never moved. That was tonight's object.
- **Synonym bakeoff primary still 0/3** — EXP-MAGNET-01 finding unchanged; claims
  tier recovers 3/3. Not fixed this slice (vocabulary, not apply).
- **Bedrock cloud still BLOCKED** — NoCredentialsError; local receipt only.
- **`--apply` is skill-only** — hook/setting write-back not shipped; adopt refuses
  non-skill with a clear message.
- **Adopt default still simulates next week** when `--apply` is absent — known
  honesty debt from MAGNET-BUGS; `--apply` flips it off. Oscar call to flip global default.
- **SHIP GATE asked `git push origin main`** — cloud agent pushes feature branch + PR;
  merge is Oscar's click.
- **fleet-ops plan still 404**.
- **Screenshot sidecars still say 113** — not in check_docs scan list; left stale
  rather than re-film (Oscar films). Live CLI numbers re-derived above.
