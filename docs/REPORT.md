# Build report · Slice 22 · 2026-09-10

## SHIPPED

### Slice 22 — Hook control fix + foreign-harden closed loop
- **Hook control:** `no-rm-rf-star-allow` no longer scores when `settings.json` is missing or has no `permissions.allow` key (green-on-outage fix). Empty dir and Agent Grinder / anthropics clones now report `hook-coverage 0/2` before harden.
- **`magnet foreign-harden`:** Open foreign stack → BEFORE naive_title=complete at near-zero → APPLY Ultimate Guide hardening on a working copy → AFTER magnet helped with value/pop. Offline fixtures + optional `--stack` / `MAGNET_FOREIGN_BIND`.
- Wired into `scripts/judge-demo.sh` (7g/8) and `scripts/foreign-stack.sh`.
- guide-demo column padding fix (`cannot-measure` no longer concatenates into `cannot-measurehelped`).
- **183** pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 183 passed |
| Hook empty dir | `python3 -c "… hook_coverage(tempdir)"` → 0/2 |
| foreign-harden offline | `magnet foreign-harden` → findings 2/2 · moved=5/5 + 4/5 |
| foreign-harden anthropics | `magnet foreign-harden --stack /tmp/magnet-foreign/anthropics-skills` → effort 0/19→19/19 FINDING |
| foreign-bind hook | `magnet foreign-bind` → hook-coverage 0/2 on both offline stacks |
| check_docs | `magnet check-docs` → 13 claims PASS |
| drift-demo | `magnet drift-demo` → fake exit 1, real exit 0 |

*(Cold clone + SHIP GATE hashes filled after push.)*

## WRONG

- **Surface arm still 1/2** — FINDING only; helicon cross-surface dupe science.
- **prompt-consistency n/a** on foreign stacks without CLAUDE.md — population 0; naive still invents helped (correct embarrassment).
- **Bedrock cloud BLOCKED** — no AWS creds in this VM.
- **Prediction still lexical** — not opened this slice.
- **Screenshot PNGs not re-rendered** — txt sidecars only (counts updated).
- **Naive UG arm invents helped on every title** — same as magnet after a successful apply; the before-lie (complete at 0/N) is the embarrassment, not after-row disagreement.
- **Parallel `magnet recover` branch** cited in prior REPORT — no such remote branch found tonight; left as open trivia.
