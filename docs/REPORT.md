# Build report · Slice 25–26 · 2026-09-11

## SHIPPED

### Slice 25 — Prediction magnitude honesty
- Claimed fractions (`rises by 1/5`) checked against measured Δ (+ population).
- Direction-only ships as `naive_direction_check` (the lie that invented held).
- `magnet pred-demo` embarrassment arm.
- Flat lexicon: `still pass` / `remain green` / `stay at`.

### Slice 26 — Stay-at absolute level honesty
- `claimed_level("must stay at 5/5")` parses absolute value/pop (not a delta).
- Magnet checks latest reading; naive flat-only invents held when level is wrong.
- pred-demo rows `stay_at_holds` / `stay_at_wrong_level`.
- **209** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 209 passed |
| pred-demo | `magnet pred-demo` → magnet 10/10 · naive 7/10 · FINDING |
| wrong magnitude | `check_prediction("…rises by 2/5", "helped", 1, population=5)` → missed |
| wrong stay-at | `check_prediction("must stay at 5/5", "unchanged", 0, latest_value=4, population=5)` → missed |
| naive invents held | `naive_direction_check` → held on both wrong-magnitude and wrong-level |
| check_docs | `magnet check-docs` → 13 PASS |
| Cold clone s25 | `/tmp/magnet-cold-s25` @ `8354a7c` → 206 passed · pred-demo FINDING · JUDGE DEMO OK |
| SHIP GATE s25 | `git push origin main` → `8354a7c` |

## WRONG

- **Surface arm still 1/2** — helicon science.
- **Bedrock cloud BLOCKED.**
- **Screenshot PNGs not re-rendered** — txt sidecars updated.
- **Cold clone s26 / tip push** — filled after ship gate below.
- **Stay-at without `/pop`** (`stay at 5`) not parsed — require value/pop form.
