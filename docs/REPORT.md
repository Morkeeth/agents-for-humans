# Build report · Slice 25–27 · 2026-09-11

## SHIPPED

### Slice 25 — Prediction magnitude honesty
- Claimed fractions checked against measured Δ (+ population).
- `naive_direction_check` is the old lie; `magnet pred-demo` embarrasses it.

### Slice 26 — Stay-at absolute level honesty
- `must stay at N/P` grades latest value/pop; naive flat invents held on wrong level.

### Slice 27 — Screenshot render on Linux + live sidecars
- `scripts/render-screenshot.py` finds DejaVu/Liberation/JetBrains/Cousine on Linux.
- Live sidecars + PNGs: pred-demo, check-docs, pytest, probe-pytest-pass-rate, demo, eval, agent-run.
- `pip install -e ".[screenshots]"` optional Pillow extra.
- STRANGER-PASS pastes pred-demo FINDING.
- **212** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 212 passed |
| pred-demo | `magnet pred-demo` → magnet 10/10 · FINDING |
| wrong magnitude | rises-by-2/5 with Δ +1 → prediction-missed |
| wrong stay-at | must-stay-at 5/5 with latest 4/5 → prediction-missed |
| check_docs | `magnet check-docs` → 13 PASS |
| Linux font | `python3 scripts/render-screenshot.py docs/screenshots/pred-demo.txt …` → PNG |
| Cold clone s26 | `/tmp/magnet-cold-s26` @ `f293b38` → 209 passed · JUDGE DEMO OK |
| Cold clone s27 | `/tmp/magnet-cold-s27` @ `fab2443` → 212 passed · pred-demo FINDING · JUDGE DEMO OK · pred-demo.png present |
| SHIP GATE s25 | `git push origin main` → `8354a7c` |
| SHIP GATE s26 | `git push origin main` → `f293b38` |
| SHIP GATE s27 | `git push origin main` → `fab2443` |

## WRONG

- **Surface arm still 1/2** — helicon science.
- **Bedrock cloud BLOCKED.**
- **one-workflow.png / history.png** not re-captured tonight — still historical sidecars.
- **Stay-at without `/pop`** not parsed.
- **Pillow not in base install** — screenshots extra only; stranger cold path does not need PNGs.
