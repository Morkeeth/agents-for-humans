# Build report · Slice 15 · 2026-09-03

## SHIPPED

### Slice 15 — apply-to-stack so coverage can move
- `magnet/apply.py` — write / remove `skills/<slug>/SKILL.md` into a measured stack
- `magnet adopt --apply` — applies the skill to the stack the probe opens, then re-measures
- `magnet adopt --capabilities` — frontmatter tags; claimed never buys coverage
- Inventory parses `capabilities:`; gaps count **verified** declarations only
- `magnet stack-demo` — cold path: filler → helped · wine noise → unchanged · liar claimed → unchanged · naive helped on noise
- Judge-demo step 7 + stranger-pass run `stack-demo` (real object), not `demo-pass-rate --demo-bonus`
- Fit runs **before** apply (post-apply fit scored the skill as a duplicate of itself)
- Honesty NOTE when fit says fills-gap but `--apply` was omitted and coverage stayed flat
- 124 pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 124 passed |
| check_docs | `python3 -m magnet.cli check-docs` → 11 claims PASS |
| stack-demo | `python3 -m magnet.cli stack-demo` → exit 0; magnet unchanged on wine; naive helped |
| apply filler helped | `magnet adopt skill pdb-navigator … --probe stack-coverage --apply --stack <copy>` → helped 8/12→9/12 |
| apply noise unchanged | same path with wine-pairing → unchanged |
| claimed no buy | apply flashcard-guard `capabilities:[security]` → coverage flat; claimed_only=security |
| fixtures unmutated | `magnet probe stack-coverage` on fixtures/stack still 8/12 after stack-demo |
| Fit-before-apply | `tests/test_stack_apply.py::test_adopt_apply_prints_helped_on_filler` |
| Judge path | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |
| Cold clone | see LOG after push |

## WRONG

- **First adopt --apply --fit run:** fit ran after apply → label=`duplicate` at 100% self-overlap. Fixed: fit before apply. Logged.
- **Synonym deafness remains for text-free declarations:** a skill that only *claims* a cap (no supporting words) still does not cover it — by design. stack-demo D prints this. Primary synonym bakeoff arm still 0/3.
- **`--apply` is skill-only:** hook/setting apply into settings.json not built; OPEN for a later slice.
- **Default `simulate_next_week=True` on adopt** still fabricates a week — Oscar call; not flipped tonight.
- **Bedrock cloud still BLOCKED** — NoCredentialsError.
- **fleet-ops plan still 404**.
- **SHIP GATE asked `git push origin main`** — cloud agent policy uses feature branch + PR; commit hash on `cursor/stack-apply-coverage-2b9b`.
- **Screenshot sidecars still say 113** — not in check_docs scan set; left stale on purpose (re-capture is Oscar/film lane). Do not trust `docs/screenshots/*.txt` numbers without re-running.
