# Build report · Slice 28 · 2026-09-12

## SHIPPED

### Slice 28 — Absolute-level honesty (no-slash stay-at + remain/hold/keep + floor)
- `must stay at 5` (no `/pop`) grades latest value — no longer invents held @ 4/5.
- `remain at` / `hold at` / `keep at` / `unchanged at` are flat + level (no more no-direction while a level sits on the table).
- Floor claims: `at least 4/5` / `no worse than 4/5` — held when latest ≥ floor.
- `magnet pred-demo` → **15/15** magnet · **7** embarrassment rows vs naive direction-only.
- **227** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 227 passed |
| stay-at no slash | `check_prediction("must stay at 5", "unchanged", 0, population=5, latest_value=4)` → prediction-missed |
| remain-at | `prediction_intent("must remain at 5/5")` → flat · wrong level → missed |
| floor | `check_prediction("pass rate at least 4/5", …, latest_value=3)` → prediction-missed |
| pred-demo | `magnet pred-demo` → magnet 15/15 · embarrassed 7 · FINDING |
| check_docs | `magnet check-docs` → 13 PASS |
| Naive arm | direction-only still invents held on wrong level/floor (embarrassment) |
| Cold clone s28 | `/tmp/magnet-cold-s28` @ `ecc179f` → 227 passed · pred-demo FINDING · JUDGE DEMO OK |
| SHIP GATE s28 | `git push origin main` → `bc7a58b` |

## WRONG

- **Surface arm still 1/2** — helicon science; not papered over.
- **Bedrock cloud BLOCKED.**
- **`adopt` still fabricates next week by default** — MAGNET-BUGS left open; Slice 29 candidate.
- **Vacuous `0/0` probes exit 0** — empty stack invents a green control; Slice 30 candidate.
- **history/one-workflow sidecars still stale** (pre–outcome lines); check_docs blind to them.
- **Pillow not in base install** — screenshots extra only.
- Historical cold-clone rows in older LOG entries keep their then-true counts; do not rewrite them to 227.
