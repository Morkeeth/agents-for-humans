# Build report · Slice 13–14 · 2026-09-02

## SHIPPED

### Slice 13
- `magnet/stack.py` — inventory / gaps / rank / verify_declaration from
  `Morkeeth/mountain-of-helicon` `helicon/magnet.py`
- `magnet/bakeoff.py` — magnet vs naive_stars vs naive_name vs silent_null
- CLI: `magnet stack`, `magnet fit`, `magnet bakeoff`
- Cold-path `fixtures/stack/`
- Judge-demo step 7 + stranger-pass wired

### Slice 14
- `magnet adopt --fit` — receipt includes fills-gap / duplicate / no-signal
- `stack-coverage` builtin probe — covered/total capabilities (8/12 on fixture)
- `fit_one` / `render_fit` / `stack_coverage` helpers
- 113 pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 113 passed |
| check_docs | `python3 -m magnet.cli check-docs` → 11 claims PASS |
| Stack inventory | `python3 -m magnet.cli stack` → EMPTY agents |
| Bakeoff | `magnet bakeoff --no-write` → magnet best; synonym 0/3; wine-liar False |
| Adopt+fit | `magnet adopt skill pdb-navigator … --fit` → label fills-gap, fills debug |
| Noise adopt honesty | `magnet adopt skill wine-pairing … --fit` → verdict unchanged + fit no-signal |
| Stack coverage | `magnet probe stack-coverage` → 8/12 |
| Demo bonus opt-in | `tests/test_adopt_fit.py::test_demo_bonus_is_opt_in_only` |
| Cold clone (s13/s14) | clone branch → demo/stack/bakeoff/pytest exit 0 |

## WRONG

- **First bakeoff magnet recall 0.0** — uncovered planning/design let noise
  ("plan a wedding", "colour palette") fill top-20. Fixed on fixture; logged.
- **`reproduce` stemmed to debug `repro`** — verify-receipt wording fixed.
- **Surface arm 1/2** — reviewer-agent demoted by overlap with owned critique.
- **Synonym primary still 0/3** — EXP-MAGNET-01 re-derived; claims tier 3/3.
- **Demo-bonus always-on bug** — `tool_adopt_change` applied +1/5 on every
  `demo-pass-rate` adopt regardless of `--demo-bonus`. Found by running
  `magnet adopt … --fit` on wine-pairing (probe said helped, fit said
  no-signal). Fixed; regression tests added.
- **Bedrock cloud still BLOCKED** — NoCredentialsError.
- **fleet-ops plan still 404**.
- **PR create requires user approval** — branch pushed; merge is Oscar/user click.
- **SHIP GATE asked `git push origin main`** — cloud agent policy uses feature
  branch + PR; commits on `cursor/stack-magnet-bakeoff-5608`.
