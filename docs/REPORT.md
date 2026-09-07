# Build report · Slice 15 · 2026-09-07

## SHIPPED

- **`magnet probe --stack`** — CLI accepts the flag the receipt already advertised (was exit 2)
- **`magnet/stack.py`**: `install_skill`, `read_skill_source`, `resolve_stack_dir` (+ `MAGNET_STACK` env)
- **`magnet adopt --install <SKILL_PATH>`** — copies stack → baseline coverage → installs skill into working copy → re-probes → receipt + naive install arm + fit
- **`magnet stack-demo`** — three arms (gap fill / duplicate / noise) + real Agent Grinder object
- **`fixtures/candidates/`** — pdb-navigator, writing-coach-pro, wine-pairing
- **`fixtures/real-stacks/agentgrinder/`** — vendored snapshot of the companion product's skill surface
- Architecture diagram for the closed loop; judge-demo step 7b; README quick start
- 123 pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| probe --stack works | `magnet probe stack-coverage --stack fixtures/real-stacks/agentgrinder` → `1/12` exit 0 |
| stack-demo exit 0 | `magnet stack-demo` → gap 8→9/12 helped; dupe/noise unchanged vs naive helped; AG 1/12 |
| adopt --install closes loop | `magnet adopt skill pdb-navigator … --probe stack-coverage --install fixtures/candidates/pdb-navigator --reset` → helped; fixture still 8/12 |
| Tests green | `python3 -m pytest -q` → 123 passed |
| check_docs | `magnet check-docs` → 11 claims PASS |
| Real object coverage | opened `Morkeeth/agentgrinder` clone then vendored fixture → writing only, 1/12 |

## WRONG

- **First diagnosis of Slice 14 "done" was incomplete** — fit said fills-gap while coverage stayed 8/12 because nothing landed in the stack. Found only by running `magnet adopt … --probe stack-coverage --fit`, not by reading the LOG.
- **Receipt advertised `magnet probe … --stack` while CLI rejected it** for weeks of green demos that never passed `--stack`. Same class as the 2026-09-03 advertised-command defect.
- **`fit_one` after install would erase fills-gap** — fixed by scoring fit against the pre-install stack; almost shipped the bug.
- **Agent Grinder is 1/12** — MAGNET's companion product covers writing only. Embarrassing; measured at the object; left as FINDING, not papered over.
- **Synonym arm still 0/3** on bakeoff primary — not fixed tonight; claims tier still recovers 3/3.
- **Bedrock cloud still BLOCKED** — NoCredentialsError.
- **fleet-ops plan still 404**.
- **SHIP GATE asked `git push origin main`** — this run uses feature branch + PR per cloud agent policy; merge is Oscar click.
- **Screenshot sidecars still say 113** — not in check_docs scan list; left stale on purpose rather than re-film.
