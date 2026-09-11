# Build report · Slice 25 · 2026-09-11

## SHIPPED

### Slice 25 — Prediction stem honesty + marketing-title embarrassment
- Stems `improv`/`increas`/`decreas` now match real English (`improves`/`increases`/`decreases`).
- Bare `\bup\b` removed — `clean up` / `set up` no longer invent rise.
- `magnet adopt … "pass rate improves by 1/5" --demo-bonus` → prediction-held (was no-direction).
- `magnet foreign-hurt` grades marketing rise-speak on the same strip → prediction-missed 4/4.
- `magnet pred-demo` cold path proves stems + marketing at the object.
- **196** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 196 passed |
| improves→rise | `prediction_intent("pass rate improves")` → rise |
| clean up≠rise | `prediction_intent("clean up frontmatter")` → unknown |
| adopt improves | `magnet adopt skill x 'pass rate improves by 1/5' --demo-bonus --reset` → prediction-held |
| pred-demo | `magnet pred-demo` → RESULT PASS · market missed 4/4 |
| foreign-hurt market | `magnet foreign-hurt` → marketing rise-speak prediction-missed 4/4 |
| check_docs | `magnet check-docs` → 13 PASS |
| Live anthropics | `magnet foreign-hurt --stack /tmp/magnet-foreign/skills` → effort 0/19→19/19→0/19 hurt |
| Live superpowers | hooks-layout 3/3 · foreign-hurt 4/4 |

## WRONG

- **Surface arm still 1/2** — helicon science, not papered over.
- **Bedrock cloud BLOCKED** — no AWS creds in this VM.
- **Screenshot PNGs not re-rendered** — txt sidecars updated; PNGs stale.
- **Prediction still lexical** — stems fixed, not semantic understanding.
- **"pass rate up" is now unknown** — bare `up` removed; use rises/improves.
- **SHIP GATE on feature branch** — cloud agent pushes `cursor/prediction-stem-honesty-441a` + PR; Oscar merges to main.
- Historical s22–s24 cold-clone hashes unchanged; do not carry 196 onto those tips.
