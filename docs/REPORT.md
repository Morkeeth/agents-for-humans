# Build report · Slice 22–23 · 2026-09-10

## SHIPPED

### Slice 22 — Hook control fix + foreign-harden
- **Hook control:** missing `settings.json` no longer scores `no-rm-rf-star-allow` (green-on-outage fix) → `0/2`.
- **`magnet foreign-harden`:** title-complete at near-zero → UG apply on working copy → helped with value/pop.

### Slice 23 — Foreign-hurt + hooks-layout
- **`magnet foreign-hurt`:** harden then strip; magnet prints **hurt** while naive invents **helped** from the strip title (4/4 on fixture + Grinder; anthropics 0/19→19/19→0/19).
- **`hooks-layout` probe:** opens `hooks/hooks.json` (obra/superpowers extract offline). Layout 3/3 while UG hook-coverage 0/2 — FINDING.
- Offline fixture: `fixtures/real-stacks/superpowers-hooks/` (extracted from live clone).
- list-probes total **10**. Pytest **189** (re-derived).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 189 passed |
| Hook empty dir | hook_coverage(temp) → 0/2 |
| foreign-harden | `magnet foreign-harden` → findings 2/2 |
| foreign-hurt | `magnet foreign-hurt` → naive invented helped on 4/4 magnet-hurt |
| foreign-hurt anthropics | `--stack /tmp/magnet-foreign/anthropics-skills` → effort hurt 19→0 |
| hooks-layout | `magnet probe hooks-layout --stack fixtures/real-stacks/superpowers-hooks` → 3/3 |
| foreign-bind | `magnet foreign-bind` → findings across 3/3 stacks |
| check_docs | `magnet check-docs` → claims PASS |

*(Cold clone + SHIP GATE hashes filled after push.)*

## WRONG

- **Surface arm still 1/2** — helicon science; FINDING only.
- **prompt-consistency n/a** on foreign stacks without CLAUDE.md.
- **Bedrock cloud BLOCKED.**
- **Prediction still lexical.**
- **Screenshot PNGs not re-rendered** — txt sidecars only.
- **fixtures/stack hooks-layout 1/3** via settings.json hooks, not hooks/hooks.json — message now says "hooks object present".
- **superpowers-hooks has no skills** — effort/tools n/a; harden/hurt skip it by default.
- **No `magnet recover` remote branch** found (prior REPORT trivia).
