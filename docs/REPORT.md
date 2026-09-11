# Build report · Slice 25–26 · 2026-09-11

## SHIPPED

### Slice 27 — prompt-consistency honesty on foreign CLAUDE.md
- `claude_present` now means the file exists (was `bool(musts)` — lied on live superpowers).
- foreign-bind prints `CLAUDE.md present · 0 UG MUST: lines` + FINDING instead of `object missing`.


### Slice 25 — Prediction stem honesty + marketing-title embarrassment
- Stems `improv`/`increas`/`decreas` now match real English (`improves`/`increases`/`decreases`).
- Bare `\bup\b` removed — `clean up` / `set up` no longer invent rise.
- `magnet adopt … "pass rate improves by 1/5" --demo-bonus` → prediction-held (was no-direction).
- `magnet foreign-hurt` grades marketing rise-speak on the same strip → prediction-missed 4/4.
- `magnet pred-demo` cold path proves stems + marketing at the object.

### Slice 26 — Adopt receipt binding + marketing RED control
- Same-second SECOND adopt printed `change FIRST` — `latest_adoption` tied on `recorded_at`.
- Receipt now binds to THIS adoption's description; `latest_adoption` orders by `id DESC`.
- `magnet foreign-hurt` exits 1 unless marketing rise-speak FINDING is present.
- **201** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 201 passed |
| improves→rise | `prediction_intent("pass rate improves")` → rise |
| clean up≠rise | `prediction_intent("clean up frontmatter")` → unknown |
| adopt improves | `magnet adopt … 'pass rate improves by 1/5' --demo-bonus --reset` → prediction-held |
| pred-demo | `magnet pred-demo` → RESULT PASS · market missed 4/4 |
| foreign-hurt market | `magnet foreign-hurt` → marketing rise-speak prediction-missed 4/4 |
| same-second receipt | two `--no-simulate` adopts → SECOND receipt `change SECOND` |
| check_docs | `magnet check-docs` → 13 PASS |
| Judge | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |
| Cold clone s26 | `/tmp/magnet-cold-s26` @ `9c9d680` → 201 passed · JUDGE DEMO OK |
| Live anthropics | `magnet foreign-hurt --stack /tmp/magnet-foreign/skills` → effort 0/19→19/19→0/19 |

## WRONG

- **Surface arm still 1/2** — helicon science, not papered over.
- **Bedrock cloud BLOCKED** — no AWS creds in this VM.
- **Screenshot PNGs not re-rendered** — txt sidecars updated; PNGs stale.
- **Prediction still lexical** — stems fixed, not semantic.
- **"pass rate up" is now unknown** — bare `up` removed; use rises/improves.
- **SHIP GATE on feature branch** — pushes `cursor/prediction-stem-honesty-441a` + PR; Oscar merges to main.
- Historical s22–s24 cold-clone hashes unchanged; do not carry 201 onto those tips.
