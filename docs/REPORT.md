# Build report · Slice 15–16 · 2026-09-03

## SHIPPED

### Slice 15 — apply-to-stack so coverage can move
- `magnet/apply.py` — write / remove `skills/<slug>/SKILL.md` into a measured stack
- `magnet adopt --apply [--capabilities]` — apply then re-measure
- Inventory parses `capabilities:`; **verified** declarations count; **claimed never buys coverage**
- `magnet stack-demo` — filler helped · wine unchanged · liar claimed unchanged · naive helped on noise
- Judge-demo / stranger-pass run the real object (not demo-pass-rate+bonus)
- Fit runs **before** apply (post-apply was self-duplicate)

### Slice 16 — prediction check + foreign stack object
- `magnet/prediction.py` — grade prediction intent vs verdict (`held` / `missed` / `unmeasured` / `no-direction`); always "not attribution"
- Adopt receipt + history show `outcome`
- `scripts/foreign-stack.sh` + `docs/FOREIGN-STACK-RECEIPT-2026-09-03.md` — anthropics/skills
- Capability term `extract` → `extract method` (docx/pdf false positive)
- 133 pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 133 passed |
| check_docs | `python3 -m magnet.cli check-docs` → 11 claims PASS |
| stack-demo | `python3 -m magnet.cli stack-demo` → exit 0; magnet unchanged on wine; naive helped |
| apply filler helped | adopt --apply --probe stack-coverage → helped 8/12→9/12 |
| prediction-held | adopt filler "coverage rises" → prediction-held |
| prediction-missed | adopt wine "coverage rises" → prediction-missed |
| foreign stack | `MAGNET_FOREIGN_STACK=/tmp/foreign-skills bash scripts/foreign-stack.sh` → exit 0; coverage 7/12; pdb no-signal |
| extract-method fix | `tests/test_stack_apply.py::test_document_extracting_does_not_cover_refactor` |
| Judge path | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |
| Cold clone s15 | `/tmp/magnet-cold-s15` → demo/stack-demo/pytest/check-docs exit 0 |
| fixtures unmutated | `magnet probe stack-coverage` → 8/12 on fixtures/stack |

## WRONG

- **First adopt --apply --fit:** fit after apply → duplicate@100% self-overlap. Fixed: fit before apply.
- **docx/pdf falsely covered refactor** until extract→extract method; found only by opening anthropics/skills.
- **Synonym primary bakeoff still 0/3** — claimed never buys rank or coverage; by design.
- **`--apply` is skill-only** — hook/setting write into settings.json not built.
- **Default `simulate_next_week=True`** still fabricates a week — Oscar call.
- **Bedrock cloud still BLOCKED** — NoCredentialsError.
- **fleet-ops plan still 404**.
- **foreign-stack needs network** — not in CI; receipt is the offline proof.
- **SHIP GATE asked `git push origin main`** — cloud agent policy uses feature branch + PR (`cursor/stack-apply-coverage-2b9b` @ `cdd5a7a`). Merge is Oscar click.
- **Screenshot sidecars still say 113** — outside check_docs scan set; left stale.
- **PR create requires user approval** — branch pushed; ManagePullRequest registered draft.
