# Build report · Slice 20–21 · 2026-09-08

## SHIPPED

### Slice 20 — Ultimate Guide closed loop
- `tools-coverage`, `hook-coverage`, `prompt-consistency` bind probes
- `magnet guide-demo` — 5-row UG table vs naive title; moved=5/5; repo-blind flat
- `check_docs` scans screenshot sidecars (closed the 113 control gap)
- Bakeoff surface 1/2 FINDING (helicon cross-surface dupe)

### Slice 21 — Foreign-bind
- `magnet foreign-bind` — bind probes on stacks we did not build
- Offline: fixtures/stack + Agent Grinder fixture both FINDING (naive=complete, hardening 0)
- Live objects (re-derived tonight): anthropics effort **0/19** · tools **0/19** · deny **0/4**; superpowers effort **0/14** · tools **0/14** · deny **0/4**; both naive_title=complete
- **174** pytest tests

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 174 passed (re-derive) |
| guide-demo | `magnet guide-demo` → moved=5/5 FINDING |
| foreign-bind offline | `magnet foreign-bind` → findings 2/2 |
| foreign-bind anthropics | `magnet foreign-bind --stack /tmp/anthropics-skills` → effort 0/19 FINDING |
| foreign-bind superpowers | `magnet foreign-bind --stack /tmp/superpowers` → effort 0/14 FINDING |
| check_docs | `magnet check-docs` → claims PASS |
| Slice 20 cold clone | `/tmp/magnet-cold-s20` @ `68991cc` JUDGE DEMO OK |
| SHIP GATE s20 | `git push origin main` → `dabe8c7` (tip `8d80ba0`) |

## WRONG

- **Surface arm still 1/2** — FINDING only; helicon science.
- **Screenshot PNGs not re-rendered** — txt sidecars only.
- **Bedrock cloud BLOCKED**.
- **Prediction still lexical**.
- **hook-coverage 1/2 on foreign stacks** — `no-rm-rf-star-allow` is true when allow is empty (correct); blocker still missing. Not a full 0.
- **prompt-consistency n/a** on foreign stacks without CLAUDE.md — population 0, cannot invent a score.
- **Parallel `magnet recover` branch still unmerged**.
