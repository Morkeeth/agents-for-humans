# Foreign stack receipt · anthropics/skills · 2026-09-03

Independent replication (helicon S4 spirit): run MAGNET against a stack **we did
not author**. Command that produced every number below:

```bash
bash scripts/foreign-stack.sh
# or: MAGNET_FOREIGN_STACK=/tmp/foreign-skills bash scripts/foreign-stack.sh
```

Clone object: `https://github.com/anthropics/skills.git` (public, depth 1).

## Inventory (re-derived)

```
INVENTORY   19 skills · 0 commands · 0 agents · 0 hooks · ? mcp
EMPTY       commands, agents, hooks
UNCOVERED   data, planning, refactor, review, security
coverage    7/12
```

(Before fixing the `extract`→`extract method` false positive, coverage falsely
read **8/12** because docx/pdf descriptions contain the word "extracting".)

## Fit against THEIR gaps (not fixtures/stack)

| candidate | label on fixtures/stack | label on anthropics/skills | fills |
|-----------|-------------------------|----------------------------|-------|
| sql-migrator | fills-gap (data) | fills-gap | data |
| secrets-gate | fills-gap (security) | fills-gap | security |
| plan-slicer | fills-gap / owned | fills-gap | planning |
| code-reviewer | fills-gap / owned | fills-gap | review |
| pdb-navigator | **fills-gap (debug)** | **no-signal** | — |
| wine-pairing | no-signal | no-signal | — |

## FINDINGS

1. **Fixture gaps ≠ foreign gaps.** `pdb-navigator` is the demo filler on
   `fixtures/stack` and is **no-signal** on anthropics/skills because their
   `webapp-testing` skill already covers debug. Ranking by our fixture would
   have lied about their stack.
2. **Noise stays noise.** wine-pairing is no-signal on both.
3. **Vocabulary false positive caught by opening the object.** Bare capability
   term `extract` matched "extracting content from .docx". Fixed to
   `extract method`. Coverage on foreign stack moved 8/12 → 7/12.

## Repro

```bash
bash scripts/foreign-stack.sh
```

Requires network once to clone. No AWS keys. Not run in CI (network).
Numbers above re-derived 2026-09-03 — do not carry them forward without re-running.
