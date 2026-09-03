# Build report · Slice 15 · 2026-09-03

## SHIPPED

### Prior (slices 13–14, this branch lineage)
- Stack inventory + bakeoff vs marketplace proxies
- `magnet adopt --fit` + `stack-coverage` probe

### Slice 15 (tonight)
- **`fixtures/stack-cursor/`** — sanitized copy of live Cursor skills (independent stack; filter author did not design it)
- **`magnet replicate`** — bakeoff on author fixture AND independent Cursor stack side-by-side
- **Author must-beat CI control** — magnet recall must beat `naive_stars` on `fixtures/stack` or exit RED
- **Independent-stack loss shipped as finding** — magnet loses to `naive_stars` on the thin Cursor stack; printed, not papered over
- **`magnet coverage-delta`** — temp-install a candidate; check predicted caps vs newly-covered (attributed / coincident / nothing-moved)
- **Frontmatter body fallback** — empty YAML `description:` no longer captures the next key (`metadata:`) — found by opening live `canvas/SKILL.md`
- Judge-demo step 7b + stranger-pass wired
- 109 pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 109 passed |
| check_docs | `python3 -m magnet.cli check-docs` → 11 claims PASS |
| Replicate | `magnet replicate` → author 0.5>0.375; independent LOST 0.25<0.375; wine-liar False |
| Coverage-delta attributed | `magnet coverage-delta … --stack fixtures/stack-cursor` → 2/12→3/12 debug attributed |
| Noise coverage | wine-pairing on fixtures/stack → nothing-moved |
| Frontmatter fix | `tests/test_coverage_delta.py::test_frontmatter_empty_description_falls_back_to_body` |
| Author must-beat | `tests/test_replicate.py::test_replicate_author_must_beat_naive_stars` |
| Judge demo | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |

## WRONG

- **Independent-stack magnet LOST** — recall 0.25 vs naive_stars 0.375 on `fixtures/stack-cursor`. Thin real stacks leave most caps uncovered; noise that mentions planning/design/etc. floods top-k. EXP-MAGNET-01 caveat re-derived on a stack we did not author. Shipped as the finding.
- **Synonym primary still 0/3** on both stacks — deaf to paraphrase; claims tier 3/3.
- **Planted flood still authored** — S4 partial only (independent stack, not independent planted set). Stated limit.
- **Bedrock cloud still BLOCKED** — NoCredentialsError.
- **fleet-ops plan still 404**.
- **SHIP GATE asked `git push origin main`** — this cloud agent pushes a feature branch + PR; merge is Oscar's click.
- **Canvas skill had empty YAML description** — body fallback fixed; live Cursor skills remain unevenly tagged.
