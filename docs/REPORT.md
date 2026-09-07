# Build report · Slice 15–19 · 2026-09-07

## SHIPPED

### Slice 15–16
- Closed-loop `stack-demo` · TAG_VOCAB 1.1 synonym 3/3 · `magnet receipt` JSON

### Slice 17
- `extract`→`extract method` · redact-scan · external-stack · foreign-stack.sh
- Real objects: Grinder 1/12 · anthropics 7/12 · superpowers 6/12

### Slice 18
- Prediction-held/missed on adopt + history outcome (not attribution)

### Slice 19
- `magnet/stack_bind.py` · `effort-coverage` + `deny-coverage` probes
- `magnet bind-demo` — repo-blind check-docs flat; stack-bind probes move
- Adopt receipts say `measures stack` for bind probes
- **159** pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 159 passed |
| check_docs | `magnet check-docs` → 11 claims PASS |
| bind-demo FINDING | `magnet bind-demo` → effort 0/7→7/7 · deny 0/4→4/4 · check-docs unchanged |
| Fixture untouched | `magnet probe effort-coverage` → 0/7 after bind-demo |
| list-probes | `magnet list-probes` → total 6 |
| prediction-held | `magnet adopt … --demo-bonus` → prediction-held |
| redact-scan | `magnet redact-scan` → findings 0 |
| anthropics | `magnet probe stack-coverage --stack /tmp/anthropics-skills` → 7/12 |
| Judge demo | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |
| Cold clone s18 | `/tmp/magnet-cold-s18` → 148 passed @ 655014d |
| Cold clone s19 | `/tmp/magnet-cold-s19` → 159 passed · bind-demo FINDING @ 03d289a |
| Cold clone main | `/tmp/magnet-main-cold` @ `d902156` (docs tip `0df0ba7`) → 159 passed · bind-demo FINDING |

## WRONG

- **Bare `extract` invented refactor** until slice 17.
- **redact-scan first RED on our own test file**.
- **Agent Grinder is 1/12**.
- **Surface arm still 1/2** (helicon science).
- **Bedrock cloud BLOCKED**.
- **SHIP GATE `git push origin main`** — succeeded @ `0df0ba7` (tip; product @ `d902156`) (also on `cursor/magnet-fundable-wedge-9126`).
- **Screenshot sidecars still claim 113**.
- **bind-demo mid-slice showed check-docs 5/11** while docs lagged new tests — control went RED correctly; re-derived to 159.
- **Prediction is lexical** — "all tests still pass" → no-direction.
- Parallel night branches' sidecar-capture not merged.
