# Build report · Slice 28–31 · 2026-09-12

## SHIPPED

### Slice 28 — Absolute-level honesty
- stay-at without `/pop`, remain/hold/keep, floor `at least`
- `magnet pred-demo` → 15/15 · 7 embarrassment rows

### Slice 29 — Adopt default real week
- Bare adopt → real `read_at`; `--simulate` opt-in

### Slice 30 — Vacuous RED + empty-allow + newline poison fix
- Empty skills → `n/a` exit 1; `allow:[]` alone ≠ hook 1/2
- `magnet vacuous-demo`; check_docs `[ \t]` not `\s`

### Slice 31 — Stale Devpost sidecar refresh + check_docs RED
- Re-derived `history.txt` / `one-workflow.txt` with prediction `outcome`
- check_docs fails if history lacks outcome/claimed or one-workflow lacks outcome
- **406** pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 406 passed |
| check_docs | `magnet check-docs` → 15 PASS (incl. history + one-workflow outcome) |
| history sidecar | `docs/screenshots/history.txt` contains `outcome` + `claimed` |
| one-workflow | `docs/screenshots/one-workflow.txt` contains `outcome` |
| RED control | tmp history without outcome → check_docs FAIL |
| vacuous-demo | `magnet vacuous-demo` → FINDING |
| Cold clone s30 | `/tmp/magnet-cold-s30` @ `7da6b5f` → 373 passed |
| Cold clone s31 | `/tmp/magnet-cold-s31` @ `1e57c56` → 373 passed · check-docs 15 PASS · JUDGE DEMO OK |
| SHIP GATE s31 | `git push origin main` → `c697a29` |
| SHIP GATE s30 | `git push origin main` → `c00bd87` |

## WRONG

- **Surface arm still 1/2** — helicon.
- **Bedrock cloud BLOCKED.**
- **one-workflow live paste** shows hurt then helped with outcome, but pass-rate swing was larger than −1/+1 while other suite noise ran — classic camera story still needs a quiet tree; numbers in the sidecar are the object, not the old 112 paste.
- **"pass rate recovers by 1"** is still no-direction (recover ∉ rise lexicon) — used `rises by 1` in the refresh.
- **Pillow not in base install.**
