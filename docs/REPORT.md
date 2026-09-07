# Build report · Slice 15–16 · 2026-09-07

## SHIPPED

### Slice 15 — closed loop
- `magnet probe --stack` (CLI accepted the flag the receipt already advertised)
- `install_skill` / `read_skill_source` / `resolve_stack_dir` (+ `MAGNET_STACK`)
- `magnet adopt --install` — working-copy install → coverage delta + naive arm
- `magnet stack-demo` — gap / duplicate / noise + real Agent Grinder object
- `fixtures/candidates/` · `fixtures/real-stacks/agentgrinder/`

### Slice 16 — synonym recovery + receipt
- TAG_VOCAB **1.1** — debug/refactor synonym bridges measured at bakeoff
- Bakeoff synonym primary **3/3** (was 0/3); recall **0.875**; wine-liar False; noise 0
- `magnet receipt` — JSON adoption receipt (schema `magnet.receipt/v1`) for stranger / Grinder verify
- **130** pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| probe --stack | `magnet probe stack-coverage --stack fixtures/real-stacks/agentgrinder` → 1/12 |
| stack-demo | `magnet stack-demo` → gap helped 8→9/12; dupe/noise unchanged vs naive helped |
| bakeoff synonym | `magnet bakeoff --no-write` → synonym 3/3 · wine-liar False · TAG_VOCAB 1.1 |
| fixture coverage unchanged by vocab | `magnet probe stack-coverage` → still 8/12 |
| receipt JSON | `magnet demo && magnet receipt` → verdict helped, value_pop 4/5 |
| Tests | `python3 -m pytest -q` → 130 passed |
| check_docs | `magnet check-docs` → 11 claims PASS |
| Cold clone (s15 branch) | `/tmp/magnet-cold-s15` → demo/stack-demo/pytest/check-docs exit 0 |
| Judge demo | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |

## WRONG

- **Slice 14 "done" was incomplete** — fit fills-gap while coverage stayed 8/12. Found only by running adopt against stack-coverage.
- **Receipt advertised `--stack` while CLI rejected it** — green demos never passed the flag.
- **First synonym expansion draft included `failing`/`moving`/`narrow`** — tightened after measuring; only terms that recover planted synonyms without noise shipped.
- **Agent Grinder is 1/12** — companion product covers writing only. Left as FINDING.
- **Surface arm still 1/2** — reviewer-agent demoted by overlap; not fixed.
- **Bedrock cloud still BLOCKED**.
- **fleet-ops plan still 404**.
- **SHIP GATE asked `git push origin main`** — this run pushes feature branch + PR; merge is Oscar click. PR create requires user approval in this environment.
- **Screenshot sidecars still claim 113** — outside check_docs scan list.
- **Editable install broke mid-session** after cold-clone `pip install -e` into a deleted worktree — reinstall fixed; scripts that mutate global editable remain a footgun (known since 2026-09-03).
