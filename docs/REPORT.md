# Build report · Slice 25 · 2026-09-11

## SHIPPED

### Slice 25 — Prediction magnitude honesty
- `check_prediction` grades claimed fractions (`rises by 1/5`) against measured Δ (+ population when both known).
- Direction-only grading ships as `naive_direction_check` — the Slice 24 behaviour that invented held on wrong magnitude.
- `magnet pred-demo` — embarrassment arm: naive held / magnet missed on rises-by-2/5 with Δ +1.
- Flat lexicon: `still pass` / `remain green` / `stay at` so judge-demo predictions are checkable.
- `magnet adopt` / `history` / `receipt` wire claimed Δ + grade.
- stranger-pass + judge-demo call `pred-demo`.
- **206** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 206 passed (re-run after docs) |
| pred-demo | `magnet pred-demo` → magnet 8/8 · naive 6/8 · FINDING |
| wrong magnitude | `check_prediction("pass rate rises by 2/5", "helped", 1, population=5)` → prediction-missed |
| naive invents held | `naive_direction_check(...)` → prediction-held on same case |
| adopt miss | `magnet adopt … 'pass rate rises by 2/5' --demo-bonus --reset` → prediction-missed |
| still pass flat | `prediction_intent("all tests still pass")` → flat |
| foreign-hurt | `magnet foreign-hurt` → prediction-held 4/4 hurt rows |
| check_docs | `magnet check-docs` → 13 PASS |

## WRONG

- **Surface arm still 1/2** — helicon science.
- **Bedrock cloud BLOCKED.**
- **Screenshot PNGs not re-rendered** — txt sidecars updated; PNGs may still show 190.
- **Absolute stay-at value not graded** — `must stay at 190/190` is flat + optional Δ 0; does not check latest value==190.
- **Cold clone / push** — filled after ship gate below.
