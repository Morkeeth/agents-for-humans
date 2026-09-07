# Build report · Slice 15–18 · 2026-09-07

## SHIPPED

### Slice 15 — closed loop
- `magnet probe --stack` · `install_skill` · `magnet adopt --install` · `magnet stack-demo`
- `fixtures/candidates/` · `fixtures/real-stacks/agentgrinder/`

### Slice 16 — synonym recovery + receipt
- TAG_VOCAB **1.1** — bakeoff synonym primary **3/3**; recall **0.875**; wine-liar False
- `magnet receipt` JSON (`magnet.receipt/v1`)

### Slice 17 — external-object honesty + redact-scan
- `extract` → `extract method` (anthropics/skills 8/12→**7/12**)
- `magnet redact-scan` · `magnet external-stack` · `scripts/foreign-stack.sh`
- Real objects: Agent Grinder **1/12**, anthropics **7/12**, obra/superpowers **6/12**

### Slice 18 — prediction check
- `magnet/prediction.py` — intent rise/fall/flat; outcome held/missed/unmeasured/no-direction
- `magnet adopt` prints prediction check; persists in adoption detail
- `magnet history` shows `outcome` (not attribution)
- **148** pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 148 passed |
| check_docs | `magnet check-docs` → 11 claims PASS |
| pytest-pass-rate | `magnet probe pytest-pass-rate` → 147/147 |
| bakeoff synonym | `magnet bakeoff --no-write` → synonym 3/3 · wine-liar False |
| stack-demo | `magnet stack-demo` → gap helped; dupe/noise unchanged vs naive helped |
| anthropics | `magnet probe stack-coverage --stack /tmp/anthropics-skills` → 7/12 |
| real Grinder | `magnet external-stack --stack /tmp/agentgrinder-real` → 1/12 |
| redact-scan | `magnet redact-scan` → findings 0 · exit 0 |
| prediction-held | `magnet adopt … --demo-bonus` → prediction-held |
| prediction-missed | `magnet adopt … --install wine-pairing --probe stack-coverage` → prediction-missed |
| history outcome | `magnet history` → outcome prediction-held |
| Judge demo | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |
| Cold clone s17 | `/tmp/magnet-cold-s17` → 139 passed · JUDGE DEMO OK |

## WRONG

- **Bare `extract` invented refactor** until slice 17 — found only by opening anthropics/skills.
- **redact-scan first RED on our own test file** — assembled plant at runtime.
- **Agent Grinder is 1/12** — companion covers writing only.
- **Surface arm still 1/2** — helicon cross-surface overlap; not rewritten.
- **Bedrock cloud still BLOCKED**.
- **fleet-ops plan still 404**.
- **SHIP GATE asked `git push origin main`** — feature branch + PR; Oscar merges.
- **Screenshot sidecars still claim 113** — outside check_docs.
- **foreign-stack.sh needs network** — offline proof is EXTERNAL-STACK-RECEIPT.md.
- **Prediction is lexical intent only** — "all tests still pass" is `no-direction`, not held. Correct, but easy to misread.
- **Parallel night branches** (bind-demo / sidecars) not merged here.
