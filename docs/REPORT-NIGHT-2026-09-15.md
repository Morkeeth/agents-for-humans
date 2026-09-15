# Night report · 2026-09-15 · Slice 35

**branch:** `cursor/negation-ceiling-target-94f8` · **tip:** `7495fbadb9d8e5e333007dbc9b701da8ad36033b` (re-derive: `git rev-parse origin/main`)

## SHIPPED

1. **Negation honesty** — `won't fall` / `does not regress` / `should not drop` are **flat**, not fall. Old magnet invented `prediction-held` when the score dropped.
2. **Ceiling claims** — dual of floor: `at most 3/5`, `no better than`, `capped at`, `must not exceed`. Held when latest ≤ ceiling.
3. **Target-level** — `falls to 2/5` / `reaches 5/5` grades latest. Direction alone no longer invents held on the wrong end-state.
4. **Lexicon** — `improves` / `climbs` / `declines` / `worsens` / `slips` (bare `improv` failed word-boundary on "improves").
5. **pred-demo** — 28/28 · naive 17/28 · embarrassed 11 · FINDING.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| THE LIE | `prediction_intent("won't fall")` | `flat` (was `fall`) |
| won't-fall + hurt | `check_prediction(..., "hurt", -1)` | `prediction-missed` |
| ceiling above | `at most 3/5` @ latest 4 | `prediction-missed`; naive held |
| falls-to wrong | `falls to 2/5` @ latest 3 | `prediction-missed`; naive held |
| Suite | `python3 -m pytest -q` | 281 passed |
| pred-demo | `python3 -m magnet.cli pred-demo` | 28/28 · embarrassed 11 · FINDING |
| check_docs | `python3 -m magnet.cli check-docs` | 16 PASS |

## WRONG

- PR auto-create blocked by user settings — Oscar must open/approve the PR UI click.
- Bedrock still BLOCKED on cloud VM (no AWS creds).
- Bakeoff surface 1/2 (helicon cross-surface dupe) still open — FINDING, not papered.
- Negation arm does not embarrass *naive* after the intent fix (both miss on `won't fall`+hurt); ceiling/target still embarrass via direction-only.
- Oscar gates remain: film · Devpost paste · submit.
- Early instinct was to ship another Grinder bridge; the defect only showed when opening the prediction object with `"won't fall"`.

## Product execution checkpoint

| Dimension | Status | Evidence |
|-----------|--------|----------|
| 1. Promised user value | **observed** | prediction check refuses negation/ceiling/target lies |
| 2. Independent use | **observed** | `magnet pred-demo` cold · no keys |
| 3. Distinctive promise | **observed** | magnet-to-YOUR-claim (open the fraction/bound, not the verb) |
| 4. Action and return | **partial** | adopt grades new lexicon; no hosted sync |
| 5. Access | **partial** | feature branch pushed; main ship pending merge/push |
